from __future__ import annotations

from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from .config import settings
from .router import route_query
from .short_term import ShortTermMemory


class MemoryState(TypedDict, total=False):
    user_id: str
    thread_id: str
    query: str
    recent_messages: list[dict[str, str]]
    route: list[str]
    layers: dict[str, str]
    merged_context: str
    budget: dict[str, dict[str, int]]


def build_memory_graph(memory_impl: Any):
    def route_node(state: MemoryState) -> dict[str, Any]:
        return {"route": route_query(state["query"])}

    def retrieve_node(state: MemoryState) -> dict[str, Any]:
        layers = {"short_term": "", "long_term": "", "episodic": "", "semantic": ""}
        selected = state.get("route", [])

        if "short_term" in selected:
            stm = ShortTermMemory(strategy="sliding", max_recent_messages=6, pressure_tokens=450)
            for msg in state.get("recent_messages", []):
                stm.add(msg["role"], msg["content"])
            layers["short_term"] = stm.render()
        if "long_term" in selected:
            layers["long_term"] = memory_impl.retrieve_long_term(
                state["user_id"], state["thread_id"], state["query"]
            )
        if "episodic" in selected:
            layers["episodic"] = memory_impl.retrieve_episodic(state["user_id"], state["query"])
        if "semantic" in selected:
            layers["semantic"] = memory_impl.retrieve_semantic(settings.semantic_graph_id, state["query"])
        return {"layers": layers}

    def assemble_node(state: MemoryState) -> dict[str, Any]:
        merged, budget = memory_impl.assemble_context(state.get("layers", {}))
        return {"merged_context": merged, "budget": budget}

    graph = StateGraph(MemoryState)
    graph.add_node("route_memory", route_node)
    graph.add_node("retrieve_memory", retrieve_node)
    graph.add_node("assemble_context", assemble_node)
    graph.add_edge(START, "route_memory")
    graph.add_edge("route_memory", "retrieve_memory")
    graph.add_edge("retrieve_memory", "assemble_context")
    graph.add_edge("assemble_context", END)
    return graph.compile()
