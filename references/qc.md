# Quality Control and Repair

Inspect each clip against the canonical project state, score it, classify failures, and
repair the smallest layer. Never accept a clip without a recorded verdict.

## Scorecard (0–5 per item)

| Check | 0 | 5 |
|---|---|---|
| Identity | wrong person | matches canon version exactly |
| Style | off-style | matches STYLE_LOCK |
| Anatomy | broken | plausible for the medium |
| Motion | frozen or chaotic | one clear, weighted action |
| Physics | impossible | weight, recoil, follow-through |
| Camera | random | exactly the intended move |
| Composition | unusable | framing as specified |
| Lighting | wrong direction/ratio | matches scene plan |
| Background | wrong location | matches location bible |
| Objects | missing/wrong props | props correct and held correctly |
| Text | garbled | legible or absent by design |
| Audio | broken/synced wrong | dialogue/ambience correct |
| Temporal stability | flicker, morph | stable across the clip |
| Continuity | violates ledger | ledger satisfied |
| Emotional performance | flat/incorrect | readable and on-beat |

A shot passes at **≥ 4 average with no item below 3**. Anything else is not accepted.

## Status

- `PASS` — meets requirements; accept and log.
- `REPAIR` — a targeted correction is likely to work (adjust the smallest layer).
- `REGENERATE` — fundamental generation failure; retry with a changed variable.
- `REPLACE` — change method/model/shot design (split the shot, re-keyframe).

## Failure taxonomy

`IDENTITY`, `STYLE`, `ANATOMY`, `MOTION`, `CAMERA`, `COMPOSITION`, `PHYSICS`,
`LIGHTING`, `BACKGROUND`, `OBJECTS`, `TEXT`, `AUDIO`, `TEMPORAL`, `CONTINUITY`,
`TOOL_ERROR`.

Classify **before** repairing. Three failures with the same class means the layer is
wrong, not the wording.

## Diagnosis and repair table

| Class | Diagnosis | Smallest fix |
|---|---|---|
| IDENTITY | reference identity weak | strengthen identity anchor, re-keyframe |
| STYLE | style block lost or drifting | re-apply STYLE_LOCK verbatim |
| ANATOMY | too much simultaneous action | split the shot, simplify pose |
| MOTION | no defined motion | specify subject + environment motion explicitly |
| CAMERA | conflicting/unmotivated move | one move only, state start and end framing |
| COMPOSITION | frame not as designed | regenerate the keyframe, not the video |
| PHYSICS | impossible action | simplify, add weight, reduce airborne elements |
| LIGHTING | direction/ratio mismatch | restate key direction and temperature |
| BACKGROUND | location drift | restate location canon + landmarks |
| OBJECTS | prop missing/wrong hand | restate prop ID, hand, and position |
| TEXT | garbled glyphs | remove text from generation; add in edit |
| AUDIO | wrong or desynced | re-time dialogue, fix mix in edit |
| TEMPORAL | flicker/morph across frames | shorten clip, lock seed and keyframe |
| CONTINUITY | ledger violated | re-keyframe against the ledger |
| TOOL_ERROR | provider/API failure | record it, retry, note in adapter `known_limits` |

`scripts/validate.py` can check the structural part of a QC report; scoring stays human.

## Repair discipline

1. Change one variable per attempt; otherwise nothing is learned.
2. Re-score after every repair; log both attempts in `runs.jsonl`.
3. After three same-class failures, escalate (keyframe → method → model → redesign).
4. Record accepted compromises explicitly — never silently ship a broken shot.

## QC report

Use `templates/qc-report.md` or `qc-report.json`. Required content: per-shot score,
status, failure class, repair action, and a final decision, plus continuity checks and
the reviewer identity/date.
