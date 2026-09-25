# SHOT_SPEC Reference

The canonical record of one shot. Provider-neutral, validated by
`../schemas/shots.schema.json`, compiled into prompts by `../scripts/prompt_compile.py`.

## Required fields

| Field | Type | Meaning |
|---|---|---|
| `id` | string | unique shot id, e.g. `shot-003` |
| `scene_id` | string | owning scene |
| `story_purpose` | string | what this shot does dramatically |
| `duration_target` | number | seconds; 3–8 s is the reliable band |
| `subject` | string | who or what we see |
| `primary_action` | string | the single observable event |
| `camera` | object | one primary camera behaviour |
| `style` | object | mode, rendering, style lock reference |
| `continuity` | object | canon anchors that must hold |

## All fields

### Identity and planning

| Field | Notes |
|---|---|
| `beat_id` | beat this shot serves |
| `coverage_role` | establishing / subject / action / reaction / insert / transition |
| `risk_level` | low / medium / high / critical (see [`../references/risk-cost.md`](../references/risk-cost.md)) |
| `attempt_budget` | permitted attempts before escalating |
| `generation_method` | text_to_video / image_to_video / multi_keyframe / reference_video / hybrid |
| `prompt_version` | increments on any prompt edit |

### Content

| Field | Notes |
|---|---|
| `reference_assets` | versioned canon ids used by this shot |
| `start_state` | the state the shot begins in (inherited from the previous `end_state`) |
| `secondary_motion` | one environmental motion (rain, traffic, curtain) |
| `end_state` | the state the next shot inherits |
| `negative_constraints` | constraints traceable to a known risk — never generic spam |

### Camera and composition

```json
"camera": {
  "type": "slow_push_in",
  "position": "medium_front",
  "height": "eye_level",
  "lens_equivalent": "normal",
  "movement_speed": "slow",
  "stabilization": "steadicam"
}
```

```json
"composition": {
  "framing": "medium",
  "angle": "eye_level",
  "subject_position": "left",
  "screen_direction": "moving_right",
  "headroom": "normal"
}
```

Token vocabulary (framing, lens, movement, transitions, lighting): see
[`../references/shot-grammar.md`](../references/shot-grammar.md).

### Lighting and environment

```json
"lighting": {
  "key": "cool fluorescent platform light",
  "direction": "screen-left",
  "quality": "soft",
  "ratio": "high",
  "temperature": "5600K",
  "rim": "wet backlight",
  "practicals": ["ceiling fluorescents", "vending machine glow"]
}
```

```json
"environment": { "location_id": "location:platform-4:v1", "time": "night", "weather": "rain" }
```

`direction` must stay consistent inside a scene unless a motivated change is recorded; the
continuity checker flags flips.

### Style, performance, timing

| Object | Fields |
|---|---|
| `style` | `mode`, `rendering`, `style_lock_ref` |
| `performance` | `behaviour`, `beat_stage` (neutralise/build/peak/release), `emotion_start`, `emotion_end` |
| `timing` | `pacing`, `holds`, `speed` |

### Continuity

Free-form anchors, conventionally: `costume`, `hair`, `prop_state`, `damage`, `held_items`.
Use the values that exist in the ledger; anything written here must be true of the ledger too.

### Audio

| Field | Notes |
|---|---|
| `dialogue` | the line, exactly |
| `speaker` | canon character id |
| `ambience` | location bed |
| `foley` | body/prop sound |
| `effects` | hard effects synced to impact frames |
| `music` | cue intent, not a track name |

## Example (abridged)

```json
{
  "id": "shot-003",
  "scene_id": "scene-01",
  "beat_id": "beat-02",
  "coverage_role": "reaction",
  "story_purpose": "Reveal that she understands no one is coming",
  "duration_target": 12,
  "subject": "Close-up of an anime teenage girl beginning to lower a red umbrella",
  "reference_assets": ["character:hana:v1", "prop:red-umbrella:v1"],
  "start_state": "Hana in close-up, umbrella canopy entering the top of frame",
  "primary_action": "She lowers the umbrella to shoulder height as her eyes widen a fraction",
  "secondary_motion": "A departing train light crosses the background once",
  "camera": { "type": "static", "lens_equivalent": "portrait" },
  "composition": { "framing": "close", "screen_direction": "center" },
  "lighting": { "direction": "screen-left", "temperature": "5600K", "ratio": "high" },
  "style": { "mode": "anime", "style_lock_ref": "style:main:v1" },
  "performance": { "beat_stage": "peak", "emotion_start": "concerned", "emotion_end": "isolated" },
  "continuity": { "costume": "school_uniform_v1", "prop_state": "red_umbrella_lowered" },
  "end_state": "Umbrella lowered to shoulder height, her gaze fixed off screen",
  "negative_constraints": ["do not change her uniform", "no extra characters"],
  "generation_method": "image_to_video",
  "risk_level": "high",
  "attempt_budget": 8,
  "prompt_version": 1
}
```

Full working example: `../examples/mini-project/shots.json`.

## Authoring rules

1. One action, one camera move, one environmental motion.
2. `end_state` of shot *N* must equal `start_state` of shot *N+1* in the same scene.
3. Every `reference_assets` entry is a versioned canon id present in the ledger.
4. `risk_level` and `attempt_budget` must agree with the documented axes.
5. Constraints address a known risk; if you cannot name the risk, delete the constraint.

## Compiled output

```bash
python scripts/prompt_compile.py shots.json --shot shot-003 --format both
python scripts/prompt_compile.py shots.json --lint
python scripts/prompt_compile.py shots.json --write video-prompts/
```

The compiler is deterministic: the same spec always produces the same prompt, which is what
makes a 40-shot film consistent and reviewable.
