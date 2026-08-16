from __future__ import annotations


def route_query(query: str) -> list[str]:
    q = query.casefold()

    short_hints = ("vua", "gan day", "luot truoc", "tin nhan", "recent", "deadline review cu")
    episodic_hints = ("lan truoc", "da thu", "fix", "trajectory", "reflection", "su co", "kinh nghiem")
    semantic_hints = ("quy tac", "policy", "payment", "retry", "playbook", "domain", "knowledge")
    long_hints = ("thich", "uu tien", "preference", "open loop", "deadline", "du an", "backend", "stack")

    layers: list[str] = []
    if any(x in q for x in short_hints):
        layers.append("short_term")
    if any(x in q for x in long_hints):
        layers.append("long_term")
    if any(x in q for x in episodic_hints):
        layers.append("episodic")
    if any(x in q for x in semantic_hints):
        layers.append("semantic")

    return layers or ["long_term", "episodic", "semantic"]
