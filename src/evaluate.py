from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table

from .config import ROOT, settings
from .memory_reference import ReferenceMemory
from .memory_student import StudentMemory
from .no_memory import NoMemory
from .short_term import ShortTermMemory
from .utils import estimate_tokens, load_dataset, load_golden_evaluations, load_knowledge, normalize
from .zep_common import (
    add_semantic_documents,
    ensure_semantic_graph,
    ensure_user,
    get_zep_client,
    ingest_user_stage,
    wait_for_search,
)

console = Console()
REPORT_DIR = ROOT / "reports"


def find_user(dataset: dict[str, Any], user_id: str) -> dict[str, Any]:
    for user in dataset["users"]:
        if user["user_id"] == user_id:
            return user
    raise KeyError(user_id)


def find_session(user: dict[str, Any], thread_id: str) -> dict[str, Any] | None:
    for session in user.get("sessions", []):
        if session["thread_id"] == thread_id:
            return session
    return None


def short_term_text(case: dict[str, Any], dataset: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    memory = ShortTermMemory(strategy="sliding", max_recent_messages=6, pressure_tokens=450)
    messages = case.get("fixture_messages")
    if not messages:
        user = find_user(dataset, case["user_id"])
        session = find_session(user, case["thread_id"])
        messages = (session or {}).get("messages", [])
    for msg in messages or []:
        memory.add(msg["role"], msg["content"])
    return memory.render(), memory.stats()


def score_case(case: dict[str, Any], retrieved: str) -> tuple[bool, list[str], list[str]]:
    text = normalize(retrieved)
    missing = [x for x in case.get("must_contain_all", []) if normalize(x) not in text]
    forbidden = [x for x in case.get("must_not_contain", []) if normalize(x) in text]
    return not missing and not forbidden, missing, forbidden


def user_source_text(dataset: dict[str, Any], user_id: str, max_stage: int) -> str:
    user = find_user(dataset, user_id)
    chunks: list[str] = []
    for session in user.get("sessions", []):
        if session["stage"] <= max_stage:
            chunks.extend(m["content"] for m in session["messages"])
    return "\n".join(chunks)


def seed_semantic_graph(client, reset: bool) -> None:
    docs = load_knowledge()
    ensure_semantic_graph(client, settings.semantic_graph_id, reset=reset)
    if reset:
        console.print("[cyan]Seeding standalone semantic graph...[/cyan]")
        add_semantic_documents(client, settings.semantic_graph_id, docs)
        # Two probes are enough to establish that the graph index is ready for the benchmark.
        wait_for_search(
            client,
            graph_id=settings.semantic_graph_id,
            query="payment retry idempotency",
            expected="PAYMENT-RULE-3",
        )
        wait_for_search(
            client,
            graph_id=settings.semantic_graph_id,
            query="async HTTP connection pool",
            expected="CONN-POOL-FIRST",
        )


def run_case(case: dict[str, Any], dataset: dict[str, Any], memory_impl) -> dict[str, Any]:
    layer = case["expected_layer"]
    query = case["query"]
    started = time.perf_counter()
    budget_breakdown: dict[str, Any] = {}
    short_stats: dict[str, Any] = {}
    error = ""

    try:
        if layer == "short_term":
            retrieved, short_stats = short_term_text(case, dataset)
        elif layer == "long_term":
            retrieved = memory_impl.retrieve_long_term(
                user_id=case["user_id"],
                thread_id=case["thread_id"],
                query=query,
            )
        elif layer == "episodic":
            retrieved = memory_impl.retrieve_episodic(case["user_id"], query)
        elif layer == "semantic":
            retrieved = memory_impl.retrieve_semantic(settings.semantic_graph_id, query)
        elif layer == "mixed":
            wanted = case.get("retrieve_layers") or ["long_term", "semantic"]
            layers = {
                "short_term": "",
                "long_term": "",
                "episodic": "",
                "semantic": "",
            }
            if "short_term" in wanted:
                layers["short_term"], short_stats = short_term_text(case, dataset)
            if "long_term" in wanted:
                layers["long_term"] = memory_impl.retrieve_long_term(
                    user_id=case["user_id"],
                    thread_id=case["thread_id"],
                    query=query,
                )
            if "episodic" in wanted:
                layers["episodic"] = memory_impl.retrieve_episodic(case["user_id"], query)
            if "semantic" in wanted:
                layers["semantic"] = memory_impl.retrieve_semantic(
                    settings.semantic_graph_id, query
                )
            retrieved, budget_breakdown = memory_impl.assemble_context(layers)
        else:
            raise ValueError(f"Unknown expected_layer: {layer}")
    except Exception as exc:
        retrieved = ""
        error = f"{type(exc).__name__}: {exc}"

    latency_ms = round((time.perf_counter() - started) * 1000, 1)
    passed, missing, forbidden = score_case(case, retrieved)
    if error:
        passed = False

    kb_text = "\n".join(json.dumps(x, ensure_ascii=False) for x in load_knowledge())
    if layer == "short_term" and case.get("fixture_messages"):
        source_text = "\n".join(m["content"] for m in case["fixture_messages"])
    else:
        source_text = user_source_text(dataset, case["user_id"], case["after_stage"])
        if layer in ("semantic", "mixed"):
            source_text += "\n" + kb_text

    retrieved_tokens = estimate_tokens(retrieved)
    full_tokens = max(1, estimate_tokens(source_text))
    reduction = max(0.0, 1.0 - retrieved_tokens / full_tokens)

    return {
        "id": case["id"],
        "layer": layer,
        "query": query,
        "passed": passed,
        "missing": missing,
        "forbidden_found": forbidden,
        "latency_ms": latency_ms,
        "retrieved_tokens": retrieved_tokens,
        "full_source_tokens": full_tokens,
        "token_reduction": round(reduction, 4),
        "short_term_stats": short_stats,
        "budget_breakdown": budget_breakdown,
        "error": error,
        "retrieved": retrieved,
    }


def write_reports(
    results: list[dict[str, Any]],
    impl_name: str,
    *,
    stem: str | None = None,
    title: str = "Lab 17 Benchmark Report",
    kind: str = "practice",
) -> tuple[Path, Path]:
    REPORT_DIR.mkdir(exist_ok=True)
    if stem:
        json_path = REPORT_DIR / f"{stem}.json"
        md_path = REPORT_DIR / f"{stem}.md"
    else:
        suffix = "" if impl_name == "student" else f"_{impl_name}"
        json_path = REPORT_DIR / f"benchmark{suffix}.json"
        md_path = REPORT_DIR / f"benchmark{suffix}.md"

    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    hit_rate = passed / total if total else 0.0
    avg_latency = sum(r["latency_ms"] for r in results) / total if total else 0.0
    avg_reduction = sum(r["token_reduction"] for r in results) / total if total else 0.0
    perfect = total > 0 and passed == total

    payload = {
        "implementation": impl_name,
        "kind": kind,
        "summary": {
            "cases": total,
            "passed": passed,
            "memory_hit_rate": round(hit_rate, 4),
            "avg_latency_ms": round(avg_latency, 1),
            "avg_token_reduction": round(avg_reduction, 4),
            "perfect": perfect,
            "golden_points": 10 if kind == "golden" and perfect else 0,
        },
        "results": results,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        f"# {title}",
        "",
        f"- Implementation: `{impl_name}`",
        f"- Kind: `{kind}`",
        f"- Cases: **{total}**",
        f"- Passed: **{passed}/{total}**",
        f"- Evidence hit rate: **{hit_rate:.1%}**",
        f"- Average retrieval latency: **{avg_latency:.1f} ms**",
        f"- Average token reduction vs full source context: **{avg_reduction:.1%}**",
    ]
    if kind == "golden":
        lines.append(f"- Golden bonus: **{10 if perfect else 0}/10** (100% required)")
    lines += [
        "",
        "| Case | Layer | Pass | Latency ms | Retrieved tokens | Token reduction | Missing / Error |",
        "| --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for r in results:
        issue = r["error"] or ("missing=" + ", ".join(r["missing"]) if r["missing"] else "")
        if r["forbidden_found"]:
            issue += " forbidden=" + ", ".join(r["forbidden_found"])
        lines.append(
            f"| {r['id']} | {r['layer']} | {'PASS' if r['passed'] else 'FAIL'} | "
            f"{r['latency_ms']:.1f} | {r['retrieved_tokens']} | {r['token_reduction']:.1%} | {issue} |"
        )

    lines += ["", "## Evidence excerpts", ""]
    for r in results:
        preview = r["retrieved"].replace("\n", " ")[:700]
        lines += [f"### {r['id']} - {r['layer']}", "", f"`{preview}`", ""]

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--impl", choices=["reference", "student", "no_memory"], default="student")
    parser.add_argument("--reset", action="store_true", help="Reset lab users/semantic graph before ingest.")
    parser.add_argument(
        "--reuse-seeded",
        action="store_true",
        help="Skip ingestion and reuse data prepared by python -m src.seed.",
    )
    parser.add_argument(
        "--only-layer",
        choices=["short_term", "long_term", "episodic", "semantic", "mixed"],
        default=None,
    )
    parser.add_argument(
        "--golden",
        action="store_true",
        help="Run the hidden 20-case golden set from data/golden_eval.json. Writes reports/golden_benchmark.*",
    )
    args = parser.parse_args()

    if args.reset and args.reuse_seeded:
        parser.error("--reset and --reuse-seeded cannot be used together")

    dataset = load_dataset()
    client = None
    if args.impl == "no_memory":
        memory_impl = NoMemory()
    else:
        client = get_zep_client()
        if not args.reuse_seeded:
            for user in dataset["users"]:
                ensure_user(client, user, reset=args.reset)
            seed_semantic_graph(client, reset=args.reset)
        memory_impl = ReferenceMemory(client) if args.impl == "reference" else StudentMemory(client)

    if args.golden:
        try:
            selected = load_golden_evaluations()
        except FileNotFoundError as exc:
            console.print(f"[red]{exc}[/red]")
            raise SystemExit(2) from exc
        if args.only_layer:
            selected = [e for e in selected if e["expected_layer"] == args.only_layer]
    else:
        selected = [
            e for e in dataset["evaluations"] if args.only_layer is None or e["expected_layer"] == args.only_layer
        ]

    stages = sorted({e["after_stage"] for e in selected})
    results: list[dict[str, Any]] = []
    ingested_through = 0

    for stage in stages:
        while ingested_through < stage:
            next_stage = ingested_through + 1
            if client is not None and not args.reuse_seeded:
                console.print(f"[cyan]Ingesting user sessions for stage {next_stage}...[/cyan]")
                for user in dataset["users"]:
                    ingest_user_stage(client, user, next_stage)
            ingested_through = next_stage

        for case in [e for e in selected if e["after_stage"] == stage]:
            console.print(f"[bold]{case['id']}[/bold] {case['expected_layer']}: {case['query']}")
            result = run_case(case, dataset, memory_impl)
            results.append(result)
            status = "[green]PASS[/green]" if result["passed"] else "[red]FAIL[/red]"
            console.print(f"  {status}  {result['latency_ms']} ms")
            if result["error"]:
                console.print(f"  [red]{result['error']}[/red]")
            elif result["missing"]:
                console.print(f"  missing: {result['missing']}")

    if args.golden:
        json_path, md_path = write_reports(
            results,
            args.impl,
            stem="golden_benchmark",
            title="Lab 17 Golden Set Report",
            kind="golden",
        )
        perfect = all(r["passed"] for r in results) and len(results) >= 20
        if perfect:
            console.print("[bold green]Golden 20/20. Bonus = 10/10.[/bold green]")
        else:
            console.print("[bold yellow]Golden not perfect. Bonus = 0/10.[/bold yellow]")
    else:
        json_path, md_path = write_reports(results, args.impl)

    table = Table(title="Benchmark summary")
    table.add_column("Case")
    table.add_column("Layer")
    table.add_column("Pass")
    table.add_column("Latency ms", justify="right")
    for r in results:
        table.add_row(r["id"], r["layer"], "yes" if r["passed"] else "no", f"{r['latency_ms']:.1f}")
    console.print(table)
    console.print(f"Reports: {json_path} | {md_path}")


if __name__ == "__main__":
    main()
