# Evaluation: Scoring Your Own Output

Self-evaluation is the difference between "produced artifacts" and "good film". Score
before delivering, and repair the weakest dimension.

## Delivery rubric (0–5 each, total 40)

| Dimension | 0 | 3 | 5 |
|---|---|---|---|
| Story clarity | no logline | logline + theme | logline, theme, and an earned ending |
| Shot necessity | coverage for its own sake | shots map to beats | every shot either advances or reveals |
| Spec completeness | fields missing | required fields present | all fields plus canon IDs and risk |
| Continuity coverage | no ledger | ledger exists | ledger + drift risks named per shot |
| Prompt specificity | adjectives only | observable actions | compiled prompts that pass the linter |
| Model realism | invented capabilities | unknowns declared | verified capabilities + degraded mode |
| QC discipline | no checks | rubric applied | failures classified with repair plan |
| Reproducibility | nothing recorded | prompts saved | run logs with seed/model/hash |

Thresholds: **≥ 32** ship. **24–31** repair the two lowest dimensions and re-score.
**< 24** return to the failing gate (`intent-routing.md`).

## Repair map (low score → reference to apply)

| Weak dimension | Apply |
|---|---|
| Story clarity | `story-and-script.md` |
| Shot necessity | `workflow.md` beat→shot mapping |
| Spec completeness | `shot-grammar.md`, `schemas/shots.schema.json` |
| Continuity coverage | `continuity.md`, `bibles.md` |
| Prompt specificity | `prompt-compilation.md`, `prompting.md` |
| Model realism | `model-adaptation.md` |
| QC discipline | `qc.md` |
| Reproducibility | `reproducibility.md` |
| Look/feel flatness | `lighting-color.md`, `cinematic-mode.md` |
| Performance flatness | `performance-direction.md` |
| Action confusion | `action-choreography.md` |
| Wrong structure for the format | `formats.md` |
| Budget blown / poor hit rate | `risk-cost.md` |

## Machine evals

`evals/cases/*.json` hold deterministic assertions (schema validity, compiled prompt
contains required blocks, budget arithmetic, drift detection). `scripts/run_evals.py`
runs them and prints a score. Run it after any change to references, schemas, or scripts.

Creative quality cannot be machine-graded: `evals/rubrics/*.md` describe the human
review of representative outputs (style test shot, one coverage set, one hero shot).

## Reporting an evaluation

```text
SCORE: 33/40   (weakest: continuity coverage 3, reproducibility 3)
EVIDENCE: shots.json validated; prompt lint 0 errors; 2 shots lack canon IDs
REPAIR: add IDs to shot-011/014; append run log for scene-02 retries
DECISION: ship after repair
```

Always include evidence. An evaluation without evidence is an opinion, and opinions
do not improve the next production.
