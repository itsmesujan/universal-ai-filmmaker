# SHOT_SPEC {{shot_id}}

Read with `references/shot-grammar.md` for the token vocabulary. One action, one camera
move, one environmental motion.

## Identity

- id:
- scene_id:
- beat_id:
- coverage_role: (establishing | subject | action | reaction | insert | transition)
- story_purpose:
- duration_target:
- risk_level: (low | medium | high | critical)
- attempt_budget:
- generation_method: (text_to_video | image_to_video | multi_keyframe | reference_video)
- prompt_version:

## Content

- subject:
- reference_assets: (versioned canon ids)
- start_state:
- primary_action:
- secondary_motion:
- end_state:

## Camera and composition

- camera.type: (one primary movement)
- camera.position / height / lens_equivalent / movement_speed / stabilization:
- composition.framing / angle / subject_position / screen_direction / headroom:

## Light and world

- lighting.key / direction / quality / ratio / temperature / rim / practicals:
- environment.location_id / time / weather / dressing:

## Style and performance

- style.mode / rendering / style_lock_ref:
- performance.behaviour / beat_stage / emotion_start / emotion_end:
- timing.pacing / holds / speed:

## Continuity

- canon anchors: (costume version, hair, prop state, damage, held items)

## Audio

- audio.dialogue / speaker / ambience / foley / effects / music:

## Constraints

- negative_constraints: (only known risks)

## QC

- status: (PASS | REPAIR | REGENERATE | REPLACE)
- score / failure_class / repair / compromise:
