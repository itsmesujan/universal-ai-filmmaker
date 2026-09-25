# Evals

"How do you know it got better?" Two layers answer that: **machine evals** for everything
deterministic, and **human rubrics** for craft.

## Run them

```bash
python scripts/run_evals.py
python scripts/run_evals.py --only continuity
python scripts/run_evals.py --json
```

Current suite: 6 cases, all passing (validate, prompt compilation ×2, budget, continuity,
risk).

## Machine evals

| Type | Asserts | Fixture |
|---|---|---|
| `validate` | artifacts satisfy the bundled schemas | `../examples/mini-project/` |
| `prompt_compile` | required blocks present; lint clean or lint catches the intended defect | mini project, `../evals/fixtures/lint-violations/` |
| `shot_budget` | plan sums to the runtime within 10% and stays in a realistic shot range | inline case data |
| `continuity` | the drift detector finds the right violation classes | `../evals/fixtures/costume-drift/` |
| `risk` | risk scoring and attempt budgets match the documented axes | inline shot |

Cases live in `../evals/cases/*.json`. A case is data, not code, so adding coverage is cheap.

## Adding a case

1. Put the input under `../evals/fixtures/<name>/` — never bend
   `../examples/mini-project/` to make a case pass.
2. Add `../evals/cases/<id>.json` with a `type` from the table above.
3. Run `python scripts/run_evals.py --only <id>` until it passes.
4. Run `python scripts/manifest.py` so the manifest stays current.

Encode failures you have actually seen. A fixture plus an assertion is how a lesson stops
being repeated.

## Human rubrics

| Rubric | Reviews | Ship threshold |
|---|---|---|
| `../evals/rubrics/shot-design.md` | coverage, framing, continuity, risk honesty | ≥ 32/40 |
| `../evals/rubrics/prompt-quality.md` | specificity, block discipline, no spam | ≥ 28/35 |
| `../evals/rubrics/qc-discipline.md` | scoring, classification, repair reasoning | ≥ 28/35 |

Review at least: one style test shot, one coverage set, one hero shot. Record the score and
the evidence in the project's `evaluation.md`.

## Delivery rubric

The 8-dimension self-evaluation in [`../references/evaluation.md`](../references/evaluation.md)
covers the whole production: story clarity, shot necessity, spec completeness, continuity
coverage, prompt specificity, model realism, QC discipline, reproducibility. Ship at ≥ 32/40.

Low dimension → the reference that fixes it:

| Weak | Apply |
|---|---|
| story clarity | [`../references/story-and-script.md`](../references/story-and-script.md) |
| shot necessity | [`workflow.md`](workflow.md) |
| spec completeness | [`shot-spec.md`](shot-spec.md) |
| continuity coverage | [`continuity.md`](continuity.md) |
| prompt specificity | [`prompting.md`](prompting.md) |
| model realism | [`model-adapters.md`](model-adapters.md) |
| QC discipline | [`quality-control.md`](quality-control.md) |
| reproducibility | [`reproducibility.md`](reproducibility.md) |

## What cannot be automated

Does the film move anyone? Does the ending land? Is the camera motivated? Machine evals
cannot answer those; the rubrics force a human to name a score and defend it with evidence.

## Reporting template

```text
SCORE: 33/40   (weakest: continuity coverage 3, reproducibility 3)
EVIDENCE: shots.json validates; prompt lint 0 findings; 2 shots lack canon ids
REPAIR: add ids to shot-011/014; append run log for scene-02 retries
DECISION: ship after repair
```
