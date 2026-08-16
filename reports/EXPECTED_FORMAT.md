# Expected benchmark format

The evaluator creates `benchmark.json` and `benchmark.md` with:

- implementation name
- case count and pass count
- memory retrieval hit rate
- no-memory evidence baseline
- average retrieval latency
- token reduction versus full source context
- per-case layer, expected markers, forbidden leakage markers and evidence excerpt

A strong submission should also explain one failed case instead of hiding it.

`--golden` writes `reports/golden_benchmark.json` and `reports/golden_benchmark.md`. `summary.perfect` must be true and `passed == 20` for the +10 golden bonus. Do not commit `data/golden_eval.json`.
