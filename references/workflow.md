# Production Workflow

## State machine

IDEA
→ STORY
→ SCRIPT
→ BIBLES
→ BEATS
→ SHOTS
→ STORYBOARD
→ KEYFRAMES
→ VIDEO
→ AUDIO
→ EDIT
→ QC
→ REPAIR
→ FINAL

Never skip a state silently. A project can enter at any state if the user already has approved artifacts.

## 5–10 minute default

Use roughly 8–15 scenes and 25–80 shots as a planning range, then adjust to pacing. These are planning heuristics, not hard limits.

## Scene record

scene_id, purpose, location_id, time, characters, emotional_start, emotional_end, dramatic_turn, visual_thesis, required_assets.

## Beat record

beat_id, scene_id, story_function, character_goal, character_state, action, reaction, pressure, turn, visual_opportunity, sound_opportunity.

## Shot record

Use the canonical SHOT_SPEC defined by SKILL.md and schemas/shots.schema.json.

## Generation order

Validate the bibles and a small representative set of shots before generating the entire project. This reduces expensive continuity failures.
