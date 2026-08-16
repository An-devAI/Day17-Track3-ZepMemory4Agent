"""Generate a colorful, self-contained HTML report from a benchmark run.

Sources:
  * a benchmark JSON produced by `src.evaluate` (structured results), and
  * (optionally) the raw run log captured while the benchmark executed.

Usage:
    python -m src.report_html                         # reports/benchmark.json -> .html
    python -m src.report_html --input reports/golden_benchmark.json
    python -m src.report_html --input reports/benchmark.json \\
        --log reports/run.log --output reports/benchmark.html
    python -m src.report_html --all                   # every reports/*benchmark*.json

The HTML is fully inline (no external CSS/JS) so it opens anywhere.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import glob
import html
import json
from pathlib import Path
from typing import Any

from .config import ROOT

REPORT_DIR = ROOT / "reports"

LAYER_COLORS = {
    "short_term": "#2563eb",
    "long_term": "#059669",
    "episodic": "#d97706",
    "semantic": "#7c3aed",
    "mixed": "#0891b2",
}


def _esc(text: Any) -> str:
    return html.escape(str(text if text is not None else ""))


def _pct(x: float) -> str:
    return f"{x * 100:.1f}%"


def _card(label: str, value: str, *, accent: str = "#334155", sub: str = "") -> str:
    sub_html = f'<div class="sub">{_esc(sub)}</div>' if sub else ""
    return (
        f'<div class="card" style="border-top:4px solid {accent}">'
        f'<div class="label">{_esc(label)}</div>'
        f'<div class="value">{_esc(value)}</div>{sub_html}</div>'
    )


def _layer_pill(layer: str) -> str:
    color = LAYER_COLORS.get(layer, "#475569")
    return f'<span class="pill" style="background:{color}">{_esc(layer)}</span>'


def build_html(payload: dict[str, Any], log_text: str | None, *, source_name: str) -> str:
    impl = payload.get("implementation", "unknown")
    kind = payload.get("kind", "practice")
    summary = payload.get("summary", {})
    results = payload.get("results", [])

    total = summary.get("cases", len(results))
    passed = summary.get("passed", sum(1 for r in results if r.get("passed")))
    hit_rate = summary.get("memory_hit_rate", (passed / total) if total else 0.0)
    avg_latency = summary.get("avg_latency_ms", 0.0)
    avg_reduction = summary.get("avg_token_reduction", 0.0)
    perfect = summary.get("perfect", total > 0 and passed == total)
    golden_pts = summary.get("golden_points", 0)
    fail = total - passed
    now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pass_pct = (passed / total * 100) if total else 0.0

    # --- summary cards ----------------------------------------------------
    cards = [
        _card("Implementation", str(impl), accent="#0ea5e9", sub=f"kind: {kind}"),
        _card("Passed", f"{passed}/{total}",
              accent="#16a34a" if perfect else ("#dc2626" if fail else "#334155")),
        _card("Hit rate", _pct(hit_rate), accent="#7c3aed"),
        _card("Avg latency", f"{avg_latency:.1f} ms", accent="#d97706"),
        _card("Token reduction", _pct(avg_reduction), accent="#0891b2"),
    ]
    if kind == "golden":
        cards.append(_card("Golden bonus", f"{golden_pts}/10",
                           accent="#16a34a" if golden_pts else "#dc2626",
                           sub="20/20 required"))

    # --- results table ----------------------------------------------------
    rows = []
    for r in results:
        ok = bool(r.get("passed"))
        status = ('<span class="tag ok">PASS</span>' if ok
                  else '<span class="tag bad">FAIL</span>')
        issue = r.get("error") or ""
        if r.get("missing"):
            issue += " missing=" + ", ".join(map(str, r["missing"]))
        if r.get("forbidden_found"):
            issue += " forbidden=" + ", ".join(map(str, r["forbidden_found"]))
        rows.append(
            f'<tr class="{"row-ok" if ok else "row-bad"}">'
            f'<td><b>{_esc(r.get("id"))}</b></td>'
            f'<td>{_layer_pill(r.get("layer", "?"))}</td>'
            f'<td>{status}</td>'
            f'<td class="num">{r.get("latency_ms", 0):.1f}</td>'
            f'<td class="num">{r.get("retrieved_tokens", 0)}</td>'
            f'<td class="num">{_pct(r.get("token_reduction", 0.0))}</td>'
            f'<td class="issue">{_esc(issue.strip())}</td></tr>'
        )
    table = "".join(rows) or '<tr><td colspan="7">No cases.</td></tr>'

    # --- per-case evidence ------------------------------------------------
    details = []
    for r in results:
        ok = bool(r.get("passed"))
        preview = _esc((r.get("retrieved") or "").strip()[:1200] or "(empty)")
        budget = r.get("budget_breakdown") or {}
        budget_html = ""
        if budget:
            items = "".join(
                f"<li>{_layer_pill(k)} used <b>{v.get('used_tokens',0)}</b> "
                f"/ limit {v.get('limit_tokens',0)} (raw {v.get('raw_tokens',0)})</li>"
                for k, v in budget.items()
            )
            budget_html = f'<div class="budget"><b>Budget</b><ul>{items}</ul></div>'
        details.append(
            f'<details class="case {"ok" if ok else "bad"}">'
            f'<summary>{_layer_pill(r.get("layer","?"))} '
            f'<b>{_esc(r.get("id"))}</b> — {_esc(r.get("query",""))}</summary>'
            f'{budget_html}'
            f'<div class="evidence"><b>Retrieved evidence</b><pre>{preview}</pre></div>'
            f'</details>'
        )
    details_html = "".join(details)

    log_html = ""
    if log_text:
        log_html = (
            '<h2>Run log</h2>'
            f'<details class="log"><summary>Show captured run log '
            f'({len(log_text.splitlines())} lines)</summary>'
            f'<pre>{_esc(log_text)}</pre></details>'
        )

    banner_color = "#16a34a" if perfect else ("#dc2626" if fail else "#334155")
    banner_text = ("PERFECT — all cases passed" if perfect
                   else f"{fail} case(s) failing")

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lab 17 Report — {_esc(impl)} ({_esc(kind)})</title>
<style>
  :root {{ color-scheme: light dark; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
         margin:0; background:#0f172a; color:#e2e8f0; }}
  .wrap {{ max-width:1100px; margin:0 auto; padding:28px 20px 60px; }}
  h1 {{ margin:0 0 4px; font-size:1.7rem; }}
  .meta {{ opacity:.7; font-size:.85rem; margin-bottom:18px; }}
  .banner {{ padding:10px 16px; border-radius:10px; font-weight:700;
            color:#fff; background:{banner_color}; margin-bottom:20px; }}
  .cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
           gap:12px; margin-bottom:24px; }}
  .card {{ background:#1e293b; border-radius:12px; padding:14px 16px; }}
  .card .label {{ font-size:.72rem; text-transform:uppercase; letter-spacing:.05em; opacity:.65; }}
  .card .value {{ font-size:1.5rem; font-weight:700; margin-top:4px; }}
  .card .sub {{ font-size:.75rem; opacity:.6; margin-top:2px; }}
  .progress {{ height:14px; background:#334155; border-radius:999px; overflow:hidden; margin-bottom:24px; }}
  .progress > i {{ display:block; height:100%; width:{pass_pct:.1f}%;
                  background:linear-gradient(90deg,#22c55e,#16a34a); }}
  table {{ width:100%; border-collapse:collapse; font-size:.88rem; margin-bottom:28px; }}
  th, td {{ padding:8px 10px; text-align:left; border-bottom:1px solid #334155; }}
  th {{ font-size:.72rem; text-transform:uppercase; letter-spacing:.05em; opacity:.7; }}
  td.num {{ text-align:right; font-variant-numeric:tabular-nums; }}
  td.issue {{ color:#fca5a5; font-size:.8rem; }}
  tr.row-ok td:first-child {{ border-left:3px solid #16a34a; }}
  tr.row-bad td:first-child {{ border-left:3px solid #dc2626; }}
  .pill {{ display:inline-block; padding:2px 9px; border-radius:999px; color:#fff;
          font-size:.72rem; font-weight:600; }}
  .tag {{ padding:2px 9px; border-radius:6px; font-size:.72rem; font-weight:700; }}
  .tag.ok {{ background:#16a34a; color:#fff; }}
  .tag.bad {{ background:#dc2626; color:#fff; }}
  details.case, details.log {{ background:#1e293b; border-radius:10px; padding:10px 14px;
                              margin-bottom:10px; border-left:4px solid #334155; }}
  details.case.ok {{ border-left-color:#16a34a; }}
  details.case.bad {{ border-left-color:#dc2626; }}
  summary {{ cursor:pointer; font-size:.9rem; }}
  pre {{ white-space:pre-wrap; word-break:break-word; background:#0f172a;
        padding:12px; border-radius:8px; font-size:.8rem; overflow-x:auto; }}
  .budget ul {{ margin:6px 0; padding-left:18px; font-size:.82rem; }}
  h2 {{ margin-top:30px; font-size:1.15rem; }}
  @media (prefers-color-scheme: light) {{
    body {{ background:#f8fafc; color:#0f172a; }}
    .card, details.case, details.log {{ background:#fff; box-shadow:0 1px 3px rgba(0,0,0,.08); }}
    pre {{ background:#f1f5f9; }}
    th, td {{ border-bottom-color:#e2e8f0; }}
    .progress {{ background:#e2e8f0; }}
  }}
</style></head>
<body><div class="wrap">
  <h1>Lab 17 — Memory Benchmark Report</h1>
  <div class="meta">Source: <code>{_esc(source_name)}</code> · generated {now}</div>
  <div class="banner">{_esc(banner_text)} · {passed}/{total} passed ({pass_pct:.0f}%)</div>
  <div class="cards">{''.join(cards)}</div>
  <div class="progress"><i></i></div>
  <h2>Cases</h2>
  <table><thead><tr>
    <th>Case</th><th>Layer</th><th>Result</th><th>Latency</th>
    <th>Tokens</th><th>Reduction</th><th>Issue</th>
  </tr></thead><tbody>{table}</tbody></table>
  <h2>Evidence</h2>
  {details_html}
  {log_html}
</div></body></html>
"""


def generate(input_path: Path, output_path: Path | None, log_path: Path | None) -> Path:
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    log_text = None
    if log_path and log_path.exists():
        log_text = log_path.read_text(encoding="utf-8", errors="replace")
    out = output_path or input_path.with_suffix(".html")
    html_doc = build_html(payload, log_text, source_name=input_path.name)
    out.write_text(html_doc, encoding="utf-8")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an HTML report from a benchmark JSON.")
    parser.add_argument("--input", default=str(REPORT_DIR / "benchmark.json"),
                        help="Benchmark JSON produced by src.evaluate.")
    parser.add_argument("--output", default=None, help="Output HTML path (default: <input>.html).")
    parser.add_argument("--log", default=None, help="Optional run-log file to embed.")
    parser.add_argument("--all", action="store_true",
                        help="Convert every reports/*benchmark*.json file.")
    parser.add_argument(
        "--include-golden",
        action="store_true",
        help="With --all, also convert *golden* JSON. Default skips those files.",
    )
    args = parser.parse_args()

    log_path = Path(args.log) if args.log else None
    if args.all:
        targets = sorted(glob.glob(str(REPORT_DIR / "*benchmark*.json")))
        if not args.include_golden:
            targets = [t for t in targets if "golden" not in Path(t).name.lower()]
        if not targets:
            raise SystemExit(f"No benchmark JSON found in {REPORT_DIR}")
        for t in targets:
            out = generate(Path(t), None, log_path)
            print(f"Wrote {out}")
        return

    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(
            f"Input not found: {input_path}. Run a benchmark first, e.g. "
            f"`make student` or `make golden`."
        )
    out = generate(input_path, Path(args.output) if args.output else None, log_path)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
