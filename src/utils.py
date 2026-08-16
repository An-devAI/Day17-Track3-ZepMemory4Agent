from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable

from .config import ROOT


def load_json(path: Path | str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_dataset() -> dict[str, Any]:
    return load_json(ROOT / "data" / "sessions.json")


def load_knowledge() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    with open(ROOT / "data" / "knowledge.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                items.append(json.loads(line))
    return items


GOLDEN_PATH = ROOT / "data" / "golden_eval.json"


def load_golden_evaluations() -> list[dict[str, Any]]:
    if not GOLDEN_PATH.exists():
        raise FileNotFoundError(
            "Golden set not released yet. Expected data/golden_eval.json. "
            "Instructor copies this file 60 minutes before lab end."
        )
    payload = load_json(GOLDEN_PATH)
    cases = payload.get("evaluations") or []
    if len(cases) < 20:
        raise ValueError(f"Golden set must contain 20 cases, found {len(cases)}")
    return cases


def cap_query(text: str, limit: int = 400) -> str:
    """Zep's graph.search rejects queries longer than 400 characters.

    Golden queries can run ~450-600 chars, so clamp to the last word boundary
    within the limit before every graph search.
    """
    if not text or len(text) <= limit:
        return text
    head = text[:limit]
    cut = head.rfind(" ")
    return head[:cut] if cut > 0 else head


def estimate_tokens(text: str) -> int:
    """Cheap model-independent estimator good enough for a lab budget."""
    if not text:
        return 0
    return max(1, (len(text) + 3) // 4)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().casefold()


def object_to_text(obj: Any) -> str:
    if obj is None:
        return ""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        return json.dumps(obj, ensure_ascii=False, default=str)
    if isinstance(obj, (list, tuple)):
        return "\n".join(object_to_text(x) for x in obj)
    if hasattr(obj, "model_dump"):
        try:
            return json.dumps(obj.model_dump(), ensure_ascii=False, default=str)
        except Exception:
            pass
    if hasattr(obj, "dict"):
        try:
            return json.dumps(obj.dict(), ensure_ascii=False, default=str)
        except Exception:
            pass
    return str(obj)


def join_nonempty(parts: Iterable[str], sep: str = "\n") -> str:
    return sep.join(p for p in parts if p and p.strip())
