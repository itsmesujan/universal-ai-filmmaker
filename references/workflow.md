# Production Workflow

## State machine

```text
IDEA → STORY → SCRIPT → BIBLES → BEATS → SHOTS → STORYBOARD → KEYFRAMES
     → VIDEO → AUDIO → EDIT → QC → REPAIR → FINAL
```

Never skip a state silently. A project can enter at any state when the user already has
approved artifacts; detect that state first (`intent-routing.md`).

Each state has: an **artifact**, an **exit gate**, and a **blocker rule**.

| State | Artifact | Exit gate |
|---|---|---|
| IDEA | routing block + assumptions | user accepts premise or you proceed with stated defaults |
| STORY | `story.md` (logline, theme, arc, ending) | STORY gate |
| SCRIPT | `script.md`, `scenes` in `project.json` | every scene has purpose, turn, location |
| BIBLES | `characters.md`, `locations.md`, `style.md` | all used assets have canon IDs |
| BEATS | `beats.json` | every beat has story function + visual idea |
| SHOTS | `shots.json` (SHOT_SPEC list) | every shot has purpose, 1 action, 1 camera move, duration |
| STORYBOARD | `storyboard.md` (panel per shot) | framing/axis/staging readable |
| KEYFRAMES | keyframe images + prompt locks | style + identity representative |
| VIDEO | clips per shot + `runs.jsonl` | QC rubric passed or repair plan |
| AUDIO | `audio-plan.md` | dialogue/ambience/SFX/music mapped per shot |
| EDIT | `edit-plan.md` | cut list with durations, transitions, timing |
| QC | `qc-report.md` | all shots scored, failures classified |
| REPAIR | updated shots/renders | repaired shots re-scored and accepted |
| FINAL | locked deliverables | continuity clean, QC signed, provenance complete |

A blocker (missing canon, unverifiable capability, rights issue) stops the pipeline.
Report it; do not generate past it.

## Planning math

- **5–10 min film:** ~8–15 scenes, ~25–80 shots (heuristic, adjust to pacing).
- **Rule of thumb:** most shots run 3–8 s. Long clips are where quality collapses.
- Also derive shot count from content: `shots ≈ dialogue shots + action shots + coverage inserts`.
- Use `scripts/shot_budget.py` for arithmetic that must sum to the runtime target.
- Total planned duration should land within ±10% of `target_duration_seconds`; if not,
  fix the plan rather than stretching clips in the edit.

## Scene record

```json
{
  "scene_id": "scene-01",
  "purpose": "why this scene exists",
  "location_id": "location:platform-4:v1",
  "time": "night",
  "characters": ["character:hana:v1"],
  "emotional_start": "hopeful",
  "emotional_end": "isolated",
  "dramatic_turn": "the platform is empty",
  "visual_thesis": "small figure, huge empty space",
  "required_assets": ["prop:red-umbrella:v1"],
  "lighting_plan": "cool practicals, key screen-left, high ratio",
  "beat_ids": ["beat-01", "beat-02"]
}
```

## Beat record

```json
{
  "beat_id": "beat-03",
  "scene_id": "scene-01",
  "story_function": "reveal isolation",
  "character_goal": "find the friend",
  "character_state": "expectant",
  "action": "she scans the platform",
  "reaction": "no one is there",
  "pressure": "the last train is leaving",
  "turn": "expectation becomes dread",
  "visual_opportunity": "empty platform in the background",
  "sound_opportunity": "rain, then engine hum",
  "shot_ids": ["shot-004", "shot-005"]
}
```

## Shot record

The canonical SHOT_SPEC: see `SKILL.md`, `schemas/shots.schema.json`, and
`shot-grammar.md` for the token vocabulary. One shot = one action + one camera move +
one environmental motion.

## Coverage model

For each beat, choose the smallest sufficient set:

1. **establishing** (where/when) — optional if already clear
2. **subject** (who/what) — required
3. **action** (what changes) — required
4. **detail/insert** (proof, clue, texture) — when it carries meaning
5. **reaction** (who is affected) — required in dialogue and action
6. **transition/exit** (what pulls to the next beat) — when the cut needs motivation

More coverage is not better; unnecessary shots cost money and dilute the cut.

## Generation order

1. Bibles → style test shot → QC → fix bibles (not the shot).
2. One coverage set for the highest-risk scene → validate geometry, light, identity.
3. Low-risk bulk shots.
4. Hero/high-risk shots with full attempt budget.
5. Repairs only for classified failures.

This ordering is what prevents expensive continuity failures late in production.

## Reviews

- **After SCRIPT:** read aloud. If a scene can be cut without loss, cut it.
- **After SHOTS:** check for redundant shots, unlocked axis, unspecified light.
- **After KEYFRAMES:** check identity/style against bibles at a glance.
- **After VIDEO:** apply the QC rubric; do not accept "close enough" without recording it.
