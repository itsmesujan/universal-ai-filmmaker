# Evals

Two layers of evaluation keep the skill honest:

1. **Machine evals** (`cases/`, `fixtures/`) — deterministic assertions about schemas,
   prompt compilation, planning math, continuity detection, and risk scoring. Run by
   `scripts/run_evals.py`; CI fails when any case fails.
2. **Human rubrics** (`rubrics/`) — creative quality cannot be machine-graded. Review
   representative outputs against the rubric and record the score in the project's
   `evaluation.md`.

## Running

```bash
python scripts/run_evals.py
python scripts/run_evals.py --only continuity
python scripts/run_evals.py --json
```

## Case types

| Type | What it asserts | Key fields |
|---|---|---|
| `validate` | artifacts satisfy the bundled schemas | `path`, `expect.errors`, `expect.min_checked` |
| `prompt_compile` | compiled prompts contain the required blocks and lint correctly | `shots`, `shot`, `expect_image_blocks`, `expect_video_blocks`, `expect_no_lint`, `expect_lint_contains` |
| `shot_budget` | planning math sums to the runtime and stays realistic | `duration`, `format`, `pacing`, `expect.max_drift_percent`, `expect.min_shots`, `expect.max_shots` |
| `continuity` | the drift detector finds the right violation classes | `shots`, `ledger`, `expect_classes`, `forbid_classes` |
| `risk` | risk scoring and attempt budgets match the documented model | inline `shot`, `expect.risk_level`, `expect.attempt_budget` |

## Adding a case

1. Put the input in `fixtures/<name>/` (never edit `examples/mini-project` to make a case pass).
2. Add `cases/<id>.json` with a `type` from the table above.
3. Run `python scripts/run_evals.py --only <id>` and confirm it passes.
4. Run `python scripts/manifest.py` so the manifest stays current.

Prefer cases that encode a real failure you have seen: a fixture plus an assertion is how
a lesson stops being repeated.

## Rubrics

| Rubric | Reviews |
|---|---|
| `rubrics/shot-design.md` | the SHOTS gate: coverage, framing, continuity, risk honesty |
| `rubrics/prompt-quality.md` | compiled prompts: specificity, block discipline, no spam |
| `rubrics/qc-discipline.md` | the QC loop: scoring, classification, repair reasoning |

Scores are 0–5 per dimension. The delivery threshold and the repair map live in
[`references/evaluation.md`](../references/evaluation.md).
