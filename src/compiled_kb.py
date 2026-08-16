from __future__ import annotations

import argparse
import json

from .config import ROOT
from .zep_common import ensure_semantic_graph, get_zep_client, render_graph_search, safe_call

GRAPH_ID = "vinuni-lab17-compiled-kb"
PAGES = ROOT / "data" / "compiled_kb.jsonl"


def load_pages() -> list[dict]:
    return [json.loads(line) for line in PAGES.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--query", default="payment retry policy and provenance")
    args = parser.parse_args()

    client = get_zep_client()
    ensure_semantic_graph(client, GRAPH_ID, reset=args.reset)
    if args.reset:
        for page in load_pages():
            client.graph.add(graph_id=GRAPH_ID, type="json", data=json.dumps(page, ensure_ascii=False))

    try:
        result = client.graph.search(
            graph_id=GRAPH_ID,
            query=args.query,
            scope="auto",
            return_raw_results=True,
            max_characters=2400,
        )
    except Exception:
        result = client.graph.search(graph_id=GRAPH_ID, query=args.query, scope="episodes", limit=8)

    print("Compiled KB query:", args.query)
    print(render_graph_search(result))
    print("\nThe records are curated entity/decision pages with provenance, not raw chat chunks.")


if __name__ == "__main__":
    main()
