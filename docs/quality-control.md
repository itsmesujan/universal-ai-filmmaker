# Quality Control

Every generated clip is inspected, scored, classified, repaired, and re-scored. Nothing is
accepted on the strength of "looks fine".

## The loop

```text
GENERATE → INSPECT → CLASSIFY → REPAIR → REGENERATE → COMPARE → ACCEPT
```

## Scorecard

Score 0–5 on: identity, style, anatomy, motion, physics, camera, composition, lighting,
background, objects, text, audio, temporal stability, continuity, emotional performance.

**Pass:** average ≥ 4.0 **and** no item below 3.

| Status | Meaning | Action |
|---|---|---|
| `PASS` | meets requirements | accept and log |
| `REPAIR` | targeted correction likely to work | fix the smallest layer |
| `REGENERATE` | generation failure | retry with one variable changed |
| `REPLACE` | method/model/design is wrong | split the shot, re-keyframe, or switch model |

## Failure taxonomy

`IDENTITY`, `STYLE`, `ANATOMY`, `MOTION`, `CAMERA`, `COMPOSITION`, `PHYSICS`, `LIGHTING`,
`BACKGROUND`, `OBJECTS`, `TEXT`, `AUDIO`, `TEMPORAL`, `CONTINUITY`, `TOOL_ERROR`.

Classify **before** rewriting anything. Three failures of the same class means a layer is
wrong, not the wording.

## Repair table

| Class | Smallest fix |
|---|---|
| IDENTITY | strengthen the identity anchor, re-keyframe |
| STYLE | re-apply STYLE_LOCK verbatim |
| ANATOMY | split the shot, simplify the pose |
| MOTION | specify subject and environment motion explicitly |
| CAMERA | one move only; state start and end framing |
| COMPOSITION | regenerate the keyframe, not the video |
| PHYSICS | simplify, add weight, reduce airborne elements |
| LIGHTING | restate key direction and temperature |
| BACKGROUND | restate location canon and landmarks |
| OBJECTS | restate prop id, hand, position |
| TEXT | remove text from generation; add it in the edit |
| AUDIO | re-time dialogue, fix the mix |
| TEMPORAL | shorten the clip, lock seed and keyframe |
| CONTINUITY | re-keyframe against the ledger |
| TOOL_ERROR | record it, retry, note it in the adapter's `known_limits` |

## Structural checks

```bash
python scripts/validate.py qc-report.json          # PASS below threshold, unresolved shots
python scripts/continuity_check.py shots.json continuity.json
```

The validator fails a `PASS` whose score is below the threshold, and fails a final `PASS`
while shots remain unresolved. Scoring itself stays human; the structure around it does not.

## Repair discipline

1. Change one variable per attempt; otherwise nothing is learned.
2. Re-score after every repair.
3. After three same-class failures, escalate: keyframe → method → model → redesign.
4. Record accepted compromises (what, where, who approved) — never ship silently broken.
5. Log both attempts in `runs.jsonl` so the cost of the decision is visible.

## QC report contents

- per-shot score, status, failure class, repair action, outcome
- continuity checks (identity, costume, props, geography, lighting, time/weather, emotion)
- evidence: validator output, continuity violations, run-log references
- final decision: PASS / REPAIR / REGENERATE / REPLACE / OPEN

Templates: `../templates/qc-report.md`, `../templates/qc-report.json`.
Rubric: `../evals/rubrics/qc-discipline.md`.

## Delivery evaluation

Before hand-off, score the whole production with the 8-dimension rubric in
[`../references/evaluation.md`](../references/evaluation.md) (0–5 each). Ship at ≥ 32/40;
below that, repair the two weakest dimensions and re-score. Attach evidence with the score —
an evaluation without evidence is an opinion.
