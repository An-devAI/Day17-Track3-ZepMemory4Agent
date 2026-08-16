# Instructor Notes - Lab 17

## Teaching goal

The lab is intentionally retrieval-first. Students do not need another LLM key to pass. A case passes only when the memory system retrieves explicit ground-truth evidence. This prevents a fluent model from masking a broken memory layer.

## Slide-to-lab mapping

| Slide concept | Lab artifact / exercise |
| --- | --- |
| Four memory types | `ShortTermMemory`, Zep Context Block/user graph, episode search, standalone semantic graph |
| Buffer / summary / sliding | `src/short_term.py`, `src/demo_short_term.py`, E10 |
| Redis long-term pattern | `src/local_baseline.py` as contrast; main implementation uses Zep |
| Buffer -> summarize -> extract -> persist | deterministic compaction + durable notes; write only after stable task state |
| LangGraph memory state | `src/graph_agent.py` |
| Episodic tuple / reflection | stages 2, E04/E05 |
| Semantic Vector DB | Zep standalone graph, E06/E11; Qdrant local comparison |
| Unified retrieval + token budget | `ContextBudgetManager`, E07 |
| Managed Zep | four TODOs in `src/memory_student.py` |
| Privacy / deletion | E09 + `src/forget.py` |
| Cross-session scope / recency | E02/E03/E08/E09 |
| Compaction + notes | E10 |
| Identity files | `control_plane/AGENTS.md`, `SOUL.md`, `MEMORY.md`, `TASKS.md` |
| Heartbeat loop | `src/heartbeat.py --dry-run` |
| Compiled knowledge base | `data/compiled_kb.jsonl`, `src/compiled_kb.py` |

## Timebox for 170 minutes (AI-era)

- 0-15: environment + smoke
- 15-45: short-term/compaction
- 45-85: long-term Context Block
- 85-110: episodic + semantic + E01-E11 benchmark + privacy screenshot + re-seed
- 110-170: **release golden set** (20 hidden cases, 20/20 = +10) and UI mini-product (+10)

Base score caps at 80. Golden and UI are the only +10/+10 bonuses. Hide/rename `memory_reference.py` before class.

Golden file: keep `instructor/golden_eval.json` private (gitignored). Release protocol: `instructor/GOLDEN_RELEASE.md`.

## Expected student edits

Only `src/memory_student.py` is required. The reference implementation is intentionally shipped in `src/memory_reference.py`; remove the `instructor/` folder and optionally hide/rename the reference file before assessment if needed.

Minimal solution shape:

1. Long-term: prime eval thread, call `thread.get_user_context`, optionally append `graph.search(scope="edges")`.
2. Episodic: `graph.search(user_id=..., scope="episodes")`.
3. Semantic: `graph.search(graph_id=..., scope="episodes")`, with a nodes fallback if needed. Avoid `scope="auto"` (drops literal markers).
4. Merge: call `ContextBudgetManager.assemble`.

## Zep ingestion timing

Graph extraction is asynchronous. The starter kit polls readiness after each seeded session and semantic graph probe. Do not remove the polling during a live class unless you replace it with another readiness check.

## Ground-truth rationale

Markers such as `ORCHID-27`, `ASYNC-FIX-20`, `PAYMENT-RULE-3` and `CONN-POOL-FIRST` are deliberately artificial. They make automated evidence scoring stable and make memory leakage obvious.

## Privacy drill

Use a disposable lab user only. `src/forget.py` deletes the Zep user and any local Redis keys under that user namespace, then verifies both. Shared semantic domain knowledge is not user PII and remains intact.
