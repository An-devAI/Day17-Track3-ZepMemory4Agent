from __future__ import annotations

import argparse
from pathlib import Path

from .config import ROOT

TASKS_PATH = ROOT / "control_plane" / "TASKS.md"


def extract_tasks(text: str) -> list[str]:
    tasks: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- [ ]"):
            tasks.append(stripped[5:].strip())
    return tasks


def build_actions(tasks: list[str]) -> list[str]:
    actions = [
        "Compact old thread context only when pressure/phase-change is detected.",
        "De-duplicate durable notes; preserve source, timestamp and confidence.",
        "Expire stale low-impact tasks according to TTL policy.",
        "Never create a high-impact task or preference change without policy/human review.",
    ]
    if tasks:
        actions.append(f"Refresh open-loop list: {len(tasks)} task(s) are still open.")
    return actions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Show maintenance actions without writing memory.")
    args = parser.parse_args()

    text = TASKS_PATH.read_text(encoding="utf-8")
    tasks = extract_tasks(text)
    print("Heartbeat maintenance pass")
    print("--------------------------")
    for task in tasks:
        print("OPEN:", task)
    print()
    for action in build_actions(tasks):
        print("ACTION:", action)

    if args.dry_run:
        print("\nDRY RUN: no Zep/Redis write was performed.")
        return

    print("\nSafe default: this teaching heartbeat is read-only.")
    print("Implement write-back only after adding provenance, allowlists and approval checks.")


if __name__ == "__main__":
    main()
