from __future__ import annotations

import math
from dataclasses import dataclass

from .utils import load_dataset


@dataclass
class EpisodeCandidate:
    episode_id: str
    age_days: float
    last_used_days_ago: float
    importance: float
    content: str

    def decayed_importance(self, half_life_days: float = 14.0) -> float:
        return self.importance * math.exp(-math.log(2) * self.age_days / half_life_days)


def build_candidates() -> list[EpisodeCandidate]:
    return [
        EpisodeCandidate("ep-ui", 25, 20, 0.2, "UI spacing discussion; no durable decision."),
        EpisodeCandidate("ep-async", 14, 2, 0.95, "ASYNC-FIX-20: ClientSession + concurrency=20 fixed connection churn."),
        EpisodeCandidate("ep-naming", 18, 16, 0.25, "Temporary variable naming brainstorm."),
        EpisodeCandidate("ep-deadline", 16, 4, 0.85, "LAB-REPORT-1600 deadline Friday 16:00."),
    ]


def consolidate_async_episode() -> dict[str, str]:
    dataset = load_dataset()
    minh = next(u for u in dataset["users"] if u["user_id"] == "minh-lab17")
    session = next(s for s in minh["sessions"] if s["thread_id"] == "minh-s2")
    source = " ".join(m["content"] for m in session["messages"])
    assert "ClientSession" in source and "connection churn" in source
    return {
        "task": "debug async HTTP timeout",
        "trajectory": "increase timeout to 60s -> inspect pool/lifecycle -> reuse aiohttp ClientSession",
        "outcome": "ClientSession + concurrency=20 worked",
        "reflection": "root cause was connection churn, not timeout threshold",
        "reusable_strategy": "Check connection pooling and client lifecycle before increasing timeout.",
    }


def main() -> None:
    items = build_candidates()
    print("[Importance decay]")
    for item in sorted(items, key=lambda x: x.decayed_importance(), reverse=True):
        print(f"{item.episode_id}: score={item.decayed_importance():.3f} content={item.content}")

    print("\n[LRU eviction candidates]")
    for item in sorted(items, key=lambda x: x.last_used_days_ago, reverse=True)[:2]:
        print(f"evict-first: {item.episode_id} last_used_days_ago={item.last_used_days_ago}")

    print("\n[Consolidation -> reusable strategy]")
    episode = consolidate_async_episode()
    for key, value in episode.items():
        print(f"{key}: {value}")

    print("\nTeaching note: do not delete Zep episodes blindly. Apply retention and review policy before destructive maintenance.")


if __name__ == "__main__":
    main()
