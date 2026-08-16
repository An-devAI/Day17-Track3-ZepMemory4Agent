from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Literal

from .utils import estimate_tokens

Strategy = Literal["buffer", "summary", "sliding"]

DURABLE_PATTERNS = (
    "todo",
    "deadline",
    "constraint",
    "decision",
    "must",
    "bat buoc",
    "khong duoc quen",
    "open loop",
    "preference",
    "uu tien",
)


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class ShortTermMemory:
    strategy: Strategy = "sliding"
    max_recent_messages: int = 6
    pressure_tokens: int = 500
    messages: list[ChatMessage] = field(default_factory=list)
    summary: str = ""
    durable_notes: list[str] = field(default_factory=list)
    compactions: int = 0

    def add(self, role: str, content: str) -> None:
        self.messages.append(ChatMessage(role=role, content=content))
        if self.strategy != "buffer" and self.detect_pressure():
            self.compact()

    def detect_pressure(self) -> bool:
        if len(self.messages) > self.max_recent_messages:
            return True
        return estimate_tokens(self._render_messages(self.messages)) > self.pressure_tokens

    def extract_durable_notes(self, messages: list[ChatMessage]) -> list[str]:
        notes: list[str] = []
        for msg in messages:
            text = msg.content.strip()
            low = text.casefold()
            has_marker = bool(re.search(r"\b[A-Z][A-Z0-9-]{5,}\b", text))
            if any(p in low for p in DURABLE_PATTERNS) or has_marker:
                note = f"{msg.role}: {text}"
                if note not in self.durable_notes and note not in notes:
                    notes.append(note)
        return notes

    def _summarize(self, messages: list[ChatMessage]) -> str:
        """Deterministic extractive summary so the lab needs no second LLM key."""
        notes = self.extract_durable_notes(messages)
        if notes:
            return " | ".join(notes[-8:])
        # Fallback: keep a compact trace instead of a free-form summary.
        snippets = [f"{m.role}: {m.content[:120]}" for m in messages[-4:]]
        return " | ".join(snippets)

    def compact(self) -> None:
        if len(self.messages) <= 2:
            return

        if self.strategy == "summary":
            old = self.messages[:-2]
            keep = self.messages[-2:]
        else:  # sliding
            keep_n = max(2, self.max_recent_messages)
            old = self.messages[:-keep_n]
            keep = self.messages[-keep_n:]

        if not old:
            return

        new_notes = self.extract_durable_notes(old)
        for note in new_notes:
            if note not in self.durable_notes:
                self.durable_notes.append(note)

        old_summary = self._summarize(old)
        if old_summary:
            if self.summary:
                self.summary = f"{self.summary} | {old_summary}"
            else:
                self.summary = old_summary
            # Bound the summary for repeated compactions.
            self.summary = self.summary[-2500:]

        self.messages = keep
        self.compactions += 1

    def render(self) -> str:
        if self.strategy == "buffer":
            return self._render_messages(self.messages)

        parts: list[str] = []
        if self.summary:
            parts.append(f"<SESSION_SUMMARY>\n{self.summary}\n</SESSION_SUMMARY>")
        if self.durable_notes:
            parts.append("<DURABLE_NOTES>\n- " + "\n- ".join(self.durable_notes[-12:]) + "\n</DURABLE_NOTES>")
        if self.messages:
            parts.append("<RECENT_TURNS>\n" + self._render_messages(self.messages) + "\n</RECENT_TURNS>")
        return "\n".join(parts)

    @staticmethod
    def _render_messages(messages: list[ChatMessage]) -> str:
        return "\n".join(f"{m.role}: {m.content}" for m in messages)

    def stats(self) -> dict[str, int]:
        rendered = self.render()
        return {
            "messages_kept": len(self.messages),
            "durable_notes": len(self.durable_notes),
            "compactions": self.compactions,
            "estimated_tokens": estimate_tokens(rendered),
        }
