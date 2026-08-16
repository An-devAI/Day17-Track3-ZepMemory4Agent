from __future__ import annotations

import json
import re
from pathlib import Path

from .config import ROOT

CONSENT_PATH = ROOT / "data" / "consent.json"
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?<!\d)(?:\+?\d[\d -]{7,}\d)(?!\d)")


def load_consent() -> dict:
    return json.loads(CONSENT_PATH.read_text(encoding="utf-8"))


def require_memory_consent(user_id: str) -> dict:
    record = load_consent().get(user_id)
    if not record or not record.get("memory_opt_in"):
        raise PermissionError(f"No durable-memory opt-in for {user_id}")
    return record


def minimize_pii(text: str) -> str:
    text = EMAIL_RE.sub("[EMAIL_REDACTED]", text)
    text = PHONE_RE.sub("[PHONE_REDACTED]", text)
    return text


def can_write_type(user_id: str, memory_type: str) -> bool:
    record = require_memory_consent(user_id)
    return memory_type in set(record.get("allowed_memory_types", []))
