from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import ROOT

REPORTS = ROOT / "reports"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory", default="reports/benchmark.json")
    parser.add_argument("--baseline", default="reports/benchmark_no_memory.json")
    args = parser.parse_args()

    memory = load(ROOT / args.memory)
    baseline = load(ROOT / args.baseline)
    m = memory["summary"]
    b = baseline["summary"]

    lines = [
        "# Memory vs No-Memory Comparison",
        "",
        "| Metric | Memory-enabled | No-memory | Delta |",
        "| --- | ---: | ---: | ---: |",
        f"| Evidence hit rate | {m['memory_hit_rate']:.1%} | {b['memory_hit_rate']:.1%} | {(m['memory_hit_rate'] - b['memory_hit_rate']):+.1%} |",
        f"| Passed cases | {m['passed']}/{m['cases']} | {b['passed']}/{b['cases']} | {m['passed'] - b['passed']:+d} |",
        f"| Avg retrieval latency (ms) | {m['avg_latency_ms']:.1f} | {b['avg_latency_ms']:.1f} | {(m['avg_latency_ms'] - b['avg_latency_ms']):+.1f} |",
        f"| Avg token reduction | {m['avg_token_reduction']:.1%} | {b['avg_token_reduction']:.1%} | {(m['avg_token_reduction'] - b['avg_token_reduction']):+.1%} |",
        "",
        "## Interpretation",
        "",
        "Short-term cases can pass without durable memory because their evidence is still in the current thread. Cross-session, episodic and semantic cases should fail in the no-memory baseline and recover when memory retrieval is enabled.",
        "",
        "A no-memory baseline may show near-100 percent token reduction simply because it retrieves nothing. Treat token reduction as useful only together with evidence hit rate; dropping all context is cheap but incorrect.",
    ]
    out = REPORTS / "comparison.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
