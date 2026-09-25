# Data Model

All structured artifacts are JSON, validated against the schemas in `../schemas/`.

## File map

| File | Schema | Purpose |
|---|---|---|
| `project.json` | `../schemas/project.schema.json` | manifest, creative intent, scenes, budget, state |
| `shots.json` | `../schemas/shots.schema.json` | array of canonical SHOT_SPEC records |
| `beats.json` | `../schemas/beats.schema.json` | dramatic beats mapped to shots |
| `continuity.json` | `../schemas/continuity.schema.json` | canon ledger, states, violations |
| `qc-report.json` | `../schemas/qc.schema.json` | per-shot scores and repair verdicts |
| `model-adapters/*.json` | `../schemas/model-adapter.schema.json` | capability snapshots |
| `runs.jsonl` | — | one JSON object per generation attempt |

Validate everything with `../scripts/validate.py`:

```bash
python scripts/validate.py project-dir
python scripts/validate.py shots.json --strict
```

## project.json

Required: `schema_version`, `project_id`, `title`, `format`, `target_duration_seconds`.

| Field | Notes |
|---|---|
| `schema_version` | `major.minor`; 1.1 for this release |
| `format` | narrative_short, anime_episode, trailer, teaser, music_video, documentary, commercial, explainer, vertical_short, series_pilot, feature |
| `target_duration_seconds` | positive number; shot durations should sum within ±10% |
| `aspect_ratio` | `16:9`, `9:16`, `2.39:1`, `1:1`, … |
| `status` | development → preproduction → production → postproduction → review → locked → delivered → archived |
| `production_state` | current pipeline state (see [`workflow.md`](workflow.md)) |
| `creative` | logline, theme, tone, audience |
| `assets` | characters, locations, props (canon ids) |
| `production` | agents, image/video/audio models, editors |
| `budget` | scene count, shot count, total attempt budget |
| `scenes` | scene records (purpose, turn, light plan, beat ids) |
| `shots` | optional inline copies; `shots.json` is authoritative |
| `continuity` / `audio` / `edit` / `qc` | pointers to the sibling artifacts |

## beats.json

Each beat carries: `beat_id`, `scene_id`, `story_function`, `action`, `turn` (required) plus
`character_goal`, `character_state`, `reaction`, `pressure`, `visual_opportunity`,
`sound_opportunity`, `emotional_start`, `emotional_end`, `shot_ids`.

A beat without a `turn` is not a beat; it is a description.

## continuity.json

| Key | Contents |
|---|---|
| `characters[]` | canon appearance, costume version, accessories, voice, state overrides |
| `locations[]` | layout reference, landmarks, entrances/exits, light direction |
| `props[]` | owner, condition, position history per shot |
| `time_and_weather[]` | per scene: time, weather, light source and direction |
| `screen_geometry[]` | per scene: axis, screen-left/right, travel directions |
| `object_state[]` | per scene per subject: costume, damage, dirt, wetness, held items |
| `emotional_state[]` | per shot: start and end emotional state (must chain) |
| `violations[]` | logged drift: `shot_id`, `class`, `decision`, `notes` |

Canon ids follow `kind:name:vN` where kind ∈ {character, location, prop, style, voice, keyframe}.

## qc-report.json

Required: `schema_version`, `project_id`, `shots[]`. Each shot entry has `shot_id`, `status`
(`PASS`/`REPAIR`/`REGENERATE`/`REPLACE`), `score` (0–5), `failure_class`, `repair`, and an
optional `compromise`. The validator flags a `PASS` below the threshold and any unresolved
shot under a final `PASS`.

## runs.jsonl

One object per attempt:

```json
{"shot_id":"shot-003","attempt":2,"model":"provider/model","adapter_version":"1.1.0",
 "prompt_hash":"sha256:…","prompt_version":1,"seed":123456,
 "references":["character:hana:v1"],"generation_method":"image_to_video",
 "duration_s":12,"result_path":"renders/shot-003-a2.mp4",
 "qc":{"status":"REPAIR","failure_class":"IDENTITY","score":3.4}}
```

## Compatibility rules

1. Adding an optional field is a minor change.
2. Removing or retyping a field is a major change, documented in [`versioning.md`](versioning.md).
3. Schemas use `additionalProperties: true` where practical, so unknown fields survive a
   round trip instead of being silently dropped.
4. Enum values include an escape (`other`, `unknown`) so exotic-but-real values stay valid.

See [`shot-spec.md`](shot-spec.md) for the full field reference of a shot.
