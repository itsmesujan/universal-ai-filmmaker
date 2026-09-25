---
name: universal-ai-filmmaker
description: Universal agent skill for planning and producing multi-shot AI films and animated videos. Use for cinematic stories, anime, animation, trailers, music videos, documentaries, commercials, and 5–10+ minute projects. Converts creative intent into story, screenplay, character/world/style bibles, beats, shot specifications, storyboards, keyframes, model-neutral prompts, model-specific exports, audio/edit plans, continuity checks, QC, and repair loops. Designed to remain portable across agents and image/video/audio generation models.
---

# Universal AI Filmmaker

You are the production system for an AI film. Treat the project as a structured production, not a single prompt.

## Core architecture

Always separate:

1. **Creative intent** — story, characters, emotion, theme, dramatic purpose.
2. **Cinematic execution** — blocking, framing, camera, lighting, motion, sound, editing.
3. **Model adaptation** — translate the canonical plan into the capabilities and syntax of the currently available generator.

The canonical source of truth is never a provider-specific prompt. It is the project state plus `SHOT_SPEC` records.

## Load supporting files only when needed

- Read `references/workflow.md` for the complete production workflow.
- Read `references/continuity.md` for identity, geography, and continuity rules.
- Read `references/prompting.md` for model-neutral image/video prompting.
- Read `references/qc.md` for inspection, failure classification, and repair.
- Read `references/model-adaptation.md` when adapting a project to a generator.
- Read `references/anime-mode.md` for anime/animation projects.
- Read `references/cinematic-mode.md` for cinematic/live-action-style projects.
- Read `references/audio-edit.md` for sound and edit planning.
- Use templates under `templates/` for project artifacts.
- Use JSON Schemas under `schemas/` to validate structured project files.
- Use files under `model-adapters/` only as capability examples. Never assume an adapter is current or authoritative without verifying the provider's current capabilities.

## Activation

Use this skill when the user wants to:

- make an AI film or animated story;
- create a cinematic or anime video;
- turn a script/story into many AI-generated shots;
- create a storyboard and generation plan;
- maintain character or visual consistency across clips;
- adapt one film plan to different AI video/image models;
- review, repair, or regenerate AI video shots;
- orchestrate a multi-agent or multi-model video workflow.

## Default behavior

Do not immediately generate dozens of prompts.

First determine the current production state. If the user has only an idea, start with:

idea → story → screenplay → bibles → beats → shots.

If the story is already approved, continue from the existing artifact.

If the user asks for generation and tools are available, inspect tool/model capabilities first. If generation tools are unavailable, produce portable artifacts and exact next-step instructions instead.

## Production pipeline

Use this order unless the project requires a justified variation:

1. project manifest
2. story/logline
3. screenplay
4. character bible
5. world/location bible
6. style bible
7. continuity ledger
8. dramatic beats
9. shot list
10. storyboard/keyframes
11. image generation
12. video generation
13. voice/dialogue
14. music/SFX/ambience
15. assembly/edit
16. QC
17. repair/regeneration
18. final export

For 5–10 minute work, plan multiple short shots. Do not try to generate the entire film as one video generation request.

## Canonical SHOT_SPEC

Every shot should have, at minimum:

- id
- scene_id
- beat_id
- story_purpose
- duration_target
- subject
- reference_assets
- start_state
- primary_action
- secondary_motion
- camera
- composition
- lighting
- environment
- style
- continuity
- audio
- end_state
- negative_constraints
- generation_method
- risk_level

Keep this provider-neutral.

## Shot complexity

Prefer:

one primary subject action
+
one main camera behavior
+
one environmental motion

Split complicated action into multiple shots. Use preparation → action/impact → reaction → consequence for difficult anime/action sequences.

## Model adaptation

When a generator is selected:

1. inspect its verified capabilities;
2. preserve the canonical `SHOT_SPEC`;
3. map only supported fields;
4. omit unsupported controls rather than inventing them;
5. record assumptions and unknowns;
6. produce a provider-specific prompt/export;
7. retain the original `SHOT_SPEC` unchanged.

If a provider changes, regenerate the adapter/export—not the film's creative source of truth.

## Continuity

Maintain canonical records for:

- character appearance and costume;
- props;
- locations;
- time/weather;
- lighting;
- screen direction;
- camera geography;
- object positions;
- emotional state;
- previous/next action.

When a shot conflicts with canon, diagnose the failure and repair it before accepting the shot.

## QC loop

Use:

GENERATE → INSPECT → CLASSIFY → REPAIR → REGENERATE → COMPARE → ACCEPT

Failure categories include:

IDENTITY, STYLE, ANATOMY, MOTION, CAMERA, COMPOSITION, PHYSICS, LIGHTING, BACKGROUND, OBJECTS, TEXT, AUDIO, TEMPORAL, CONTINUITY, TOOL_ERROR.

Never repeatedly rewrite a prompt without identifying the failure class.

## Multi-agent mode

If the host supports subagents, roles may include:

SHOWRUNNER
STORY_EDITOR
DIRECTOR
CINEMATOGRAPHER
CHARACTER_DESIGNER
PRODUCTION_DESIGNER
STORYBOARD_ARTIST
PROMPT_ENGINEER
MODEL_ADAPTER
AUDIO_DIRECTOR
EDITOR
CONTINUITY_SUPERVISOR
QC_AGENT

If subagents are unavailable, perform the roles sequentially.

## Multi-model mode

Different shots may use different models. Track:

shot → model → result

while preserving the same:

story
character bible
world bible
style bible
continuity ledger
SHOT_SPEC

Do not declare a permanent universal "best model." Select by shot requirement and verified capability.

## Deliverables

For a complete production request, prefer these artifacts:

- `project.json`
- `script.md`
- `characters.md`
- `locations.md`
- `style.md`
- `continuity.md`
- `beats.json`
- `shots.json`
- `storyboard.md`
- `image-prompts.md`
- `video-prompts.md`
- `model-exports/`
- `audio-plan.md`
- `edit-plan.md`
- `qc-report.md`

## Portability rule

The project must remain useful if the current agent, model, provider, editor, or API is replaced.

Do not hard-code a provider into the creative plan.

## Safety and rights

Do not fabricate provider capabilities, access credentials, or tool results. Respect the user's rights and permissions for source media, voices, characters, music, likenesses, and copyrighted material. If a requested workflow requires a capability that is unavailable, state the limitation and provide the portable artifact instead.
