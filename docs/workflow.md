# Workflow

The pipeline is a state machine with gates. Artifacts, not conversations, carry the project
forward.

```text
IDEA → STORY → SCRIPT → BIBLES → BEATS → SHOTS → STORYBOARD → KEYFRAMES
     → VIDEO → AUDIO → EDIT → QC → REPAIR → FINAL
```

## Entering mid-pipeline

| Request | Class | Entry state |
|---|---|---|
| "make me a film about…" | `NEW_FILM` | IDEA |
| "continue", "next step" | `CONTINUE` | first incomplete state |
| pasted script or treatment | `SCRIPT_IN` | SCRIPT |
| "one shot of…" | `SINGLE_SHOT` | SHOTS |
| "this clip is wrong" | `REPAIR` | QC |
| "make it work for model X" | `ADAPT` | MODEL ADAPTATION |
| "critique this" | `REVIEW` | current state, read-only |
| "just the plan" | `PLAN_ONLY` | stop before generation |

Detection order: project manifest → story → script → bibles → ledger → beats → shots →
storyboard → keyframes → clips → audio → edit → QC. The first missing or incomplete
artifact is where work resumes.

## Per-state contract

| State | Produce | Exit gate | Blocker example |
|---|---|---|---|
| IDEA | routing block + assumptions | premise accepted | subject unclear |
| STORY | logline, theme, arc, ending | STORY gate | no ending proposed |
| SCRIPT | scenes with purpose, turn, location | SCRIPT gate | scene with no turn |
| BIBLES | canon for every used asset | BIBLES gate | costume undefined |
| BEATS | beats with function + visual idea | BEATS gate | beat with no change |
| SHOTS | `SHOT_SPEC` list | SHOTS gate | two actions in one shot |
| STORYBOARD | panel/spec per shot | framing + axis readable | axis unplanned |
| KEYFRAMES | approved keyframes | representative style/identity | style drift vs bible |
| VIDEO | clips + run log | QC rubric passed | unverified capability needed |
| AUDIO | audio plan | layers mapped | lip-sync unverified |
| EDIT | cut list | transitions + timing | exit state contradicts next entry |
| QC | QC report | all shots scored/classified | failure class unknown |
| REPAIR | fixed shots | re-scored and accepted | budget exhausted |
| FINAL | locked deliverables | continuity clean, provenance complete | missing run log |

A blocker stops the pipeline. Report it and deliver what is complete — never paper over a
missing canon entry with a guess.

## Planning math

- 5–10 min film: **8–15 scenes, 25–80 shots** (heuristic; adjust to pacing).
- Most shots run **3–8 s**; long clips are where quality collapses.
- Planned duration should land within **±10%** of `target_duration_seconds`.
- Use `../scripts/shot_budget.py` so the arithmetic is reproducible:

```bash
python scripts/shot_budget.py --duration 480 --format narrative_short --pacing normal
```

## Coverage model

For each beat, choose the smallest sufficient set:

| Role | Purpose | Required? |
|---|---|---|
| establishing | where/when | only if not already clear |
| subject | who/what | yes |
| action | what changes | yes |
| insert/detail | proof, clue, texture | only when it carries meaning |
| reaction | who is affected | yes in dialogue and action |
| transition/exit | pull to the next beat | only when the cut needs motivation |

If a shot can be deleted without losing information or feeling, delete it.

## Generation order (cost-aware)

1. Bibles → one cheap **style test shot** → QC → fix the bibles, not the shot.
2. One coverage set for the highest-risk scene → validate geometry, light, identity.
3. Bulk low-risk shots.
4. Hero/high-risk shots with the full attempt budget.
5. Repairs only for classified failures.

## Reviews that catch real problems

- **After SCRIPT:** read aloud; cut any scene that can be removed without loss.
- **After SHOTS:** hunt for redundant shots, unlocked axis, unspecified light, unmotivated movement.
- **After KEYFRAMES:** compare identity and style to the bibles at a glance.
- **After VIDEO:** apply the QC scorecard; record every accepted compromise.
- **After EDIT:** check `end_state` → `start_state` continuity across every cut.

## Triggering a repair loop

```text
GENERATE → INSPECT → CLASSIFY → REPAIR → REGENERATE → COMPARE → ACCEPT
```

One variable per attempt, re-score after each, and after three failures of the same class
change the layer (keyframe → method → model → shot design) rather than the wording.

See also: [`architecture.md`](architecture.md), [`quality-control.md`](quality-control.md),
[`../references/workflow.md`](../references/workflow.md).
