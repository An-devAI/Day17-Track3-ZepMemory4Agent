# Golden set release (instructor only)

`data/golden_eval.json` is gitignored. Do not commit it. Keep a private copy (LMS / USB / this machine).

## When

Release **60 minutes before lab end** (minute 110 of a 170-minute lab).

## How

1. Upload `data/golden_eval.json` to LMS (or a classroom USB).
2. Students copy it to `data/golden_eval.json` in their starter kit.
3. They run:

```bash
docker compose run --rm app python -m src.evaluate --impl student --reuse-seeded --golden
```

4. Collect `reports/golden_benchmark.json`. **20/20 PASS = +10. Any miss = 0.**

Before class, dry-run once:

```bash
docker compose run --rm app python -m src.evaluate --impl reference --reuse-seeded --golden
```

Reference should be close to 20/20. If unused KB markers (`DELETE-VERIFY-ALL`, `BUDGET-10-4-3-3`) miss, re-seed and wait; do not release a broken set.

## Do not

- Put the file in git, email the class earlier, or leave it in a public fork.
- Re-seed Zep after students have a warm graph; golden reuses the same users/KB.
- Grade golden from a student-edited JSON. Re-run with the instructor copy.

## After class

Delete student copies if needed. The public practice set remains `data/sessions.json` (E01-E11).
