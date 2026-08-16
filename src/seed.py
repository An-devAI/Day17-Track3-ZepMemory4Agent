from __future__ import annotations

from rich.console import Console

from .config import settings
from .utils import load_dataset, load_knowledge
from .zep_common import (
    add_semantic_documents,
    ensure_semantic_graph,
    ensure_user,
    get_zep_client,
    ingest_user_stage,
    wait_for_search,
)

console = Console()


def main() -> None:
    dataset = load_dataset()
    client = get_zep_client()

    console.print("[cyan]Resetting synthetic lab users...[/cyan]")
    for user in dataset["users"]:
        ensure_user(client, user, reset=True)

    console.print("[cyan]Resetting and seeding semantic graph...[/cyan]")
    ensure_semantic_graph(client, settings.semantic_graph_id, reset=True)
    add_semantic_documents(client, settings.semantic_graph_id, load_knowledge())
    wait_for_search(
        client,
        graph_id=settings.semantic_graph_id,
        query="payment retry Idempotency-Key PAYMENT-RULE-3",
        expected="PAYMENT-RULE-3",
    )
    wait_for_search(
        client,
        graph_id=settings.semantic_graph_id,
        query="connection pooling CONN-POOL-FIRST",
        expected="CONN-POOL-FIRST",
    )
    wait_for_search(
        client,
        graph_id=settings.semantic_graph_id,
        query="DELETE-VERIFY-ALL opt-in deletion request",
        expected="DELETE-VERIFY-ALL",
    )
    wait_for_search(
        client,
        graph_id=settings.semantic_graph_id,
        query="BUDGET-10-4-3-3 Memory Context Budget",
        expected="BUDGET-10-4-3-3",
    )

    max_stage = max(session["stage"] for user in dataset["users"] for session in user.get("sessions", []))
    for stage in range(1, max_stage + 1):
        console.print(f"[cyan]Ingesting stage {stage}...[/cyan]")
        for user in dataset["users"]:
            ingest_user_stage(client, user, stage)

    console.print("[green]Seed complete.[/green]")
    console.print("Use: python -m src.evaluate --impl student --reuse-seeded")


if __name__ == "__main__":
    main()
