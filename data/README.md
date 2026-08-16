# Lab data

- `sessions.json`: synthetic users, staged chat threads and evaluation cases.
- `ground_truth.json`: the evaluation portion extracted for easy inspection.
- `consent.json`: opt-in registry used by the teaching privacy guard.
- `knowledge.jsonl`: shared domain knowledge ingested into the semantic standalone graph.
- `compiled_kb.jsonl`: curated entity/decision pages used by the compiled-KB demo.

`data/golden_eval.json` is **not in git**. Instructor releases it 60 minutes before lab end. Schema-only file: `golden_eval.example.json`.

## Ground-truth scoring

A case passes when every string in `must_contain_all` occurs in the retrieved evidence and every string in `must_not_contain` is absent.

This is intentionally retrieval-level scoring. A language model cannot get credit by guessing the answer when the memory backend did not return supporting evidence.
