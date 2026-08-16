from __future__ import annotations

import argparse

from .graph_agent import build_memory_graph
from .memory_reference import ReferenceMemory
from .memory_student import StudentMemory
from .utils import load_dataset
from .zep_common import ensure_user, get_zep_client, ingest_user_stage


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--impl", choices=["reference", "student"], default="reference")
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--user-id", default="minh-lab17")
    parser.add_argument(
        "--query",
        default="Lan truoc Minh fix async HTTP timeout bang cach nao?",
    )
    args = parser.parse_args()

    dataset = load_dataset()
    zep = get_zep_client()
    selected_user = next(u for u in dataset["users"] if u["user_id"] == args.user_id)
    ensure_user(zep, selected_user, reset=args.reset)
    for stage in (1, 2):
        ingest_user_stage(zep, selected_user, stage)

    impl = ReferenceMemory(zep) if args.impl == "reference" else StudentMemory(zep)
    graph = build_memory_graph(impl)
    result = graph.invoke(
        {
            "user_id": args.user_id,
            "thread_id": "demo-agent-eval",
            "query": args.query,
            "recent_messages": [],
        }
    )

    print("route:", result.get("route"))
    print("\nmerged context:\n")
    print(result.get("merged_context", ""))
    print("\nbudget:\n", result.get("budget", {}))


if __name__ == "__main__":
    main()
