from __future__ import annotations

from typing import Any

from .config import settings
from .context_budget import ContextBudgetManager


class NoMemory:
    """Baseline: current-thread short-term is handled by evaluator; no durable retrieval exists."""

    def __init__(self, client: Any = None):
        self.client = client
        self.budget = ContextBudgetManager(settings.context_tokens)

    def retrieve_long_term(self, user_id: str, thread_id: str, query: str) -> str:
        return ""

    def retrieve_episodic(self, user_id: str, query: str) -> str:
        return ""

    def retrieve_semantic(self, graph_id: str, query: str) -> str:
        return ""

    def assemble_context(self, layers: dict[str, str]):
        return self.budget.assemble(layers)
