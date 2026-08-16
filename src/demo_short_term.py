from __future__ import annotations

from rich.console import Console
from rich.panel import Panel

from .short_term import ShortTermMemory

console = Console()

MESSAGES = [
    ("user", "Constraint: REVIEW-DEADLINE-1600 - project review is Friday at 16:00 and must not be forgotten."),
    ("assistant", "Acknowledged."),
] + [("user" if i % 2 == 0 else "assistant", f"Filler turn {i} about an already-resolved detail.") for i in range(1, 15)]


def main() -> None:
    for strategy in ("buffer", "summary", "sliding"):
        memory = ShortTermMemory(strategy=strategy, max_recent_messages=6, pressure_tokens=300)
        for role, content in MESSAGES:
            memory.add(role, content)
        console.print(Panel(memory.render(), title=f"{strategy} | {memory.stats()}"))


if __name__ == "__main__":
    main()
