from __future__ import annotations

from .memory_reference import ReferenceMemory
from .utils import load_dataset
from .zep_common import ensure_user, get_zep_client, ingest_user_stage


def show(title: str, text: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)
    print(text[:3500])


def main() -> None:
    dataset = load_dataset()
    user = next(u for u in dataset["users"] if u["user_id"] == "minh-lab17")
    client = get_zep_client()
    ensure_user(client, user, reset=True)
    memory = ReferenceMemory(client)

    ingest_user_stage(client, user, 1)
    show(
        "Session 1 -> Session 2: cross-session preference",
        memory.retrieve_long_term("minh-lab17", "demo-s2", "Voi demo ca nhan, Minh uu tien ngon ngu nao?"),
    )

    ingest_user_stage(client, user, 2)
    show(
        "Session 2 -> Session 3: episodic trajectory",
        memory.retrieve_episodic("minh-lab17", "Lan truoc fix async HTTP timeout bang cach nao?"),
    )

    ingest_user_stage(client, user, 3)
    show(
        "Session 3: scoped update / recency",
        memory.retrieve_long_term("minh-lab17", "demo-s4", "Backend BLUEBIRD-42 bat buoc dung stack gi?"),
    )


if __name__ == "__main__":
    main()
