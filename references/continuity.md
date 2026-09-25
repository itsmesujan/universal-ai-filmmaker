# Continuity and Identity

The continuity ledger is authoritative for recurring assets. If a clip disagrees with
the ledger, the clip is wrong — unless the ledger was deliberately versioned.

## Ledger structure

`continuity.json` (schema: `schemas/continuity.schema.json`):

- `characters[]` — id, canon appearance summary, costume version, accessories,
  voice, movement style, per-scene state overrides
- `locations[]` — id, layout reference, landmarks, entrances/exits, light direction
- `props[]` — id, owner, position history, condition
- `time_and_weather[]` — scene_id, time, weather, light source, direction
- `screen_geometry[]` — scene_id, axis, who is screen-left/right, travel directions
- `object_state[]` — scene_id, per-subject costume/damage/dirt/wetness/held items
- `emotional_state[]` — shot_id, state at start and end
- `violations[]` — logged drift events with shot_id, class, decision

Canon IDs are always versioned: `character:hana:v1`. A deliberate change creates `v2`;
never edit `v1` in place.

## Character continuity

Track face, hair, body proportions, costume, accessories, palette, age presentation,
voice, and movement style. Also track *state*: wet, dirty, injured, holding items.
State changes are events: record where they happen so later shots inherit them.

## World continuity

Track location layout, entrances/exits, landmarks, props, weather, time, lighting
direction, and environmental damage. Add a text plan view so the camera can be placed
consistently: which wall the door is on, where the window light enters, where the
camera may stand.

## Screen geography

- Lock the **axis (180° line)** per scene; state who is screen-left and screen-right.
- Preserve **travel direction**: a subject moving screen-right keeps moving screen-right.
- Eyelines: define the off-screen target and match the angle/height.
- Camera side of the action changes only via a neutral shot (insert, cutaway, or a
  deliberate crossing on a move).
- Foreground/background layering and subject distance should be compatible across cuts.

## The three continuity classes

| Class | Question | Example failure |
|---|---|---|
| Identity | is it the same character? | face morphs, hair length changes |
| State | is it the same moment? | clean shirt after the fight, umbrella appears |
| Geography | is it the same space? | door flips sides, light flips direction |

Classify every continuity failure before repairing; the class tells you which layer to fix.

## Repair order

Fix the smallest layer that explains the failure:

1. reference asset
2. keyframe
3. shot design
4. model adapter/prompt
5. model/provider

Do not change the whole project to repair one shot. Do not re-litigate the story to fix
a face.

## Drift detection routine

After generating a scene, compare each clip against the ledger and ask:

1. Does the subject match the canon ID version used earlier in the scene?
2. Does costume/damage/prop state match the previous `end_state`?
3. Does light direction and key temperature match the scene plan?
4. Does the axis and travel direction hold?
5. Does the emotional state at start match the previous shot's end?

Log every mismatch in `violations[]` with a decision: repair, re-keyframe, or accept with
recorded compromise. `scripts/continuity_check.py` automates the mechanical part.

## Failure modes

| Symptom | Class | Fix |
|---|---|---|
| Face changes between cuts | identity | restate canon ID + reference sheet; re-keyframe |
| Costume changes mid-scene | state | restate costume version and state events |
| Light flips direction | geography | restate key direction from the scene plan |
| Door/window on wrong side | geography | re-keyframe against the plan view |
| Damage disappears | state | add damage to the ledger and to the next prompt |
| Emotional jump between shots | state | align `end_state` → `start_state` in the beat sheet |
