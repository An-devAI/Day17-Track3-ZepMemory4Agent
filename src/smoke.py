from __future__ import annotations

import sys

import requests
import redis

from .config import settings
from .utils import load_dataset


def check(condition: bool, ok: str, fail: str) -> bool:
    print(f"[{'OK' if condition else 'FAIL'}] {ok if condition else fail}")
    return condition


def main() -> None:
    all_ok = True

    try:
        r = redis.from_url(settings.redis_url, decode_responses=True)
        all_ok &= check(r.ping() is True, "Redis reachable", "Redis ping failed")
    except Exception as exc:
        all_ok &= check(False, "", f"Redis unreachable: {exc}")

    try:
        response = requests.get(f"{settings.qdrant_url}/collections", timeout=5)
        all_ok &= check(response.ok, "Qdrant reachable", f"Qdrant HTTP {response.status_code}")
    except Exception as exc:
        all_ok &= check(False, "", f"Qdrant unreachable: {exc}")

    try:
        dataset = load_dataset()
        evals = dataset.get("evaluations", [])
        layers = {e["expected_layer"] for e in evals}
        valid = len(evals) >= 10 and {"short_term", "long_term", "episodic", "semantic"}.issubset(layers)
        all_ok &= check(valid, f"sessions.json valid: {len(evals)} evaluations", "sessions.json is incomplete")
    except Exception as exc:
        all_ok &= check(False, "", f"Dataset invalid: {exc}")

    all_ok &= check(bool(settings.zep_api_key), "ZEP_API_KEY is present", "ZEP_API_KEY is missing")
    raise SystemExit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
