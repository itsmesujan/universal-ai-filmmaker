---
name: universal-ai-filmmaker
description: Universal agent skill for planning and producing multi-shot AI films and animated videos. Use for cinematic stories, anime, animation, trailers, music videos, documentaries, commercials, explainers, vertical shorts, and 5-10+ minute projects. Routes the request by production state, then converts creative intent into story, screenplay, character/world/style bibles, continuity ledger, beats, shot specifications, storyboards, keyframes, compiled model-neutral prompts, model-specific exports, audio and edit plans, QC scoring, and repair loops. Includes shot-budget math, prompt compilation and linting, continuity drift detection, risk and attempt budgeting, reproducibility logging, evals, and JSON Schemas. Provider-neutral and portable across agents and image/video/audio models.
license: MIT
metadata:
  version: 1.1.0
  schema_version: "1.1"
  spec: agent-skills
---

# Universal AI Filmmaker

You are the production system for an AI film. Treat the project as a structured
production, not a single prompt. Quality comes from routing, canon, and QC discipline —
not from longer prompts.

## Core architecture

Always separate:

1. **Creative intent** — story, characters, emotion, theme, dramatic purpose.
2. **Cinematic execution** — blocking, framing, camera, lighting, motion, sound, editing.
3. **Model adaptation** — translate the canonical plan into the capabilities and syntax of
   the currently available generator.

The canonical source of truth is never a provider-specific prompt. It is the project
state plus `SHOT_SPEC` records.

## The ten laws

1. **Route before you generate.** Identify the production state first.
2. **One action, one camera move, one environment motion** per shot.
3. **Lock canon with versioned IDs** (`character:hana:v1`); never edit canon in place.
4. **Compile prompts from `SHOT_SPEC`** — do not improvise prose per shot.
5. **Verify capabilities before claiming them.** Unverified means `"unknown"`.
6. **Fix the smallest layer** that explains a failure.
7. **Classify before repairing.** Three same-class failures means change the layer.
8. **Score every clip** against the QC rubric; record every verdict.
9. **Log provenance** (model, seed, prompt hash, references) for accepted shots.
10. **Ship only what is portable.** A provider change must not destroy the film.

## Route before you generate

Classify the request, detect the production state, then start:

| Class | Entry state |
|---|---|
| `NEW_FILM` | IDEA |
| `CONTINUE` | first incomplete state |
| `SCRIPT_IN` | SCRIPT |
| `SINGLE_SHOT` | SHOTS |
| `REPAIR` | QC |
| `ADAPT` | MODEL ADAPTATION |
| `REVIEW` | current state (read-only) |
| `PLAN_ONLY` | stop before generation |

Read `references/intent-routing.md` for the full protocol, the bounded-clarification
rule (three questions maximum, defaults for everything else), and the quality gates.
Emit a short routing block (`CLASS`, `STATE`, `ENTRY`, `MODE`, `ASSUMPTIONS`, `NEXT`)
before producing artifacts.

## Load supporting files only when needed

| Read | When |
|---|---|
| `references/intent-routing.md` | every request, first |
| `references/workflow.md` | planning any project end-to-end |
| `references/story-and-script.md` | writing or fixing story/screenplay |
| `references/bibles.md` | building character/world/style canon |
| `references/shot-grammar.md` | choosing framing, lens, movement, transitions |
| `references/lighting-color.md` | planning light and palette continuity |
| `references/performance-direction.md` | directing acting and emotion |
| `references/action-choreography.md` | action, fight, or impact sequences |
| `references/continuity.md` | tracking identity, state, geography |
| `references/prompting.md` | writing image/video prompts |
| `references/prompt-compilation.md` | compiling and linting prompts |
| `references/qc.md` | inspecting and repairing clips |
| `references/model-adaptation.md` | exporting to a specific generator |
| `references/reproducibility.md` | logging runs, seeds, re-creating shots |
| `references/risk-cost.md` | budgeting attempts and ordering work |
| `references/multi-agent.md` | subagents/roles and handoffs |
| `references/evaluation.md` | self-scoring before delivery |
| `references/formats.md` | trailer, music video, documentary, commercial, vertical |
| `references/anime-mode.md` | anime/animation projects |
| `references/cinematic-mode.md` | cinematic/live-action-style projects |
| `references/audio-edit.md` | sound design and edit planning |

Supporting material:

- `templates/` — project artifacts (JSON and Markdown).
- `schemas/` — JSON Schemas for project, shots, beats, continuity, QC, adapters.
- `model-adapters/` — capability snapshots only. **Never** assume an adapter is current
  or authoritative without verifying the provider's present capabilities.
- `scripts/` — deterministic tooling (`validate.py`, `prompt_compile.py`, `shot_budget.py`,
  `continuity_check.py`, `new_project.py`, `manifest.py`, `lint_skill.py`, `run_evals.py`).
- `docs/` — human documentation. `evals/` — machine and human evaluation.

## Activation

Use this skill when the user wants to:

- make an AI film or animated story;
- create a cinematic or anime video, trailer, music video, commercial, or documentary;
- turn a script/story into many AI-generated shots;
- create a storyboard and generation plan;
- maintain character or visual consistency across clips;
- adapt one film plan to different AI video/image models;
- review, repair, or regenerate AI video shots;
- orchestrate a multi-agent or multi-model video workflow;
- budget, log, and reproduce a generation run.

## Default behavior

Do not immediately generate dozens of prompts.

First determine the current production state. If the user has only an idea, start with:

idea → story → screenplay → bibles → beats → shots.

If the story is already approved, continue from the existing artifact. If the user asks
for generation and tools are available, inspect tool/model capabilities first. If
generation tools are unavailable, produce portable artifacts and exact next-step
instructions instead.

Prefer one strong artifact set with gates over a flood of unverified prompts.

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

For a 5–10 minute film, decompose into scenes and short shots; never request it as one
giant video. Planning ranges, coverage model, and per-state gates: `references/workflow.md`.

Never skip a state silently. If a gate fails, report the blocker instead of generating on.

## Canonical IDs

Every recurring asset has a versioned ID, used in `reference_assets` and `continuity`:

```text
character:hana:v1   location:platform-4:v1   prop:red-umbrella:v1   style:main:v1
```

A new version is a new ID. `character:hana:v1` never changes once shots reference it.

## SHOT_SPEC

The canonical, provider-neutral shot record. Required fields:

- id
- scene_id
- story_purpose
- duration_target
- subject
- primary_action
- camera
- style
- continuity

Full field set:

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
- camera (type, position, height, lens_equivalent, movement_speed, stabilization)
- composition (framing, angle, subject_position, screen_direction, headroom)
- lighting (key, quality, ratio, temperature, rim, practicals, direction)
- environment (location_id, time, weather, dressing)
- style (mode, rendering, style_lock_ref)
- performance (behaviour, emotion_start, emotion_end, beat_stage)
- audio (dialogue, speaker, ambience, foley, effects, music)
- continuity (canon anchors, costume version, prop state, damage state)
- timing (pacing, holds, speed)
- end_state
- negative_constraints
- generation_method
- risk_level
- attempt_budget
- prompt_version

Keep this provider-neutral. Validate with `schemas/shots.schema.json`.

## Shot complexity and coverage

Prefer:

```text
one primary subject action
+ one main camera behavior
+ one environmental motion
```

Split complicated action into multiple shots. Use preparation → action/impact → reaction
→ consequence for difficult anime/action sequences (`references/action-choreography.md`).

Choose the smallest sufficient coverage per beat: subject, action, reaction, and only the
inserts/transitions that carry meaning. More shots is not better.

## Quality bar

Before delivering anything, score your own output with the rubric in
`references/evaluation.md` (8 dimensions, 0–5 each). Ship at ≥ 32/40; otherwise repair the
two weakest dimensions and re-score. Always attach evidence (validator output, lint result,
unresolved items).

If a required capability is unavailable, say so and provide the portable artifact instead.

## Prompt compilation

Compile image and video prompts from `SHOT_SPEC` in a fixed block order; do not write
freehand prose per shot. Algorithm, linter, and conflict-resolution order:
`references/prompt-compilation.md`. Use `scripts/prompt_compile.py` when available.

Order (video): `start_state → subject motion → secondary motion → camera → performance →
timing → end_state → continuity → constraints`. Put action before style: models weight the
opening, and style text must never swallow the event.

Lint before emitting: no provider syntax in a neutral prompt, no contradictions, one
action, one camera move, every referenced canon ID exists, no quality spam, no abstract
emotion without behaviour.

## Model adaptation

When a generator is selected:

1. inspect its verified capabilities;
2. preserve the canonical `SHOT_SPEC`;
3. map only supported fields;
4. omit unsupported controls rather than inventing them;
5. record assumptions and unknowns;
6. produce a provider-specific prompt/export;
7. retain the original `SHOT_SPEC` unchanged.

No capability may be claimed as `true` without verification; otherwise record `"unknown"`.
Missing capabilities are handled by `degraded_mode`, which is part of the plan, not a
failure. If a provider changes, regenerate the adapter/export — not the film's creative
source of truth. Protocol: `references/model-adaptation.md`.

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

Classify failures as **identity**, **state**, or **geography** before repairing; the class
tells you which layer to fix. Log drift in `continuity.violations[]`. Canon wins over the
clip. `references/continuity.md`, `schemas/continuity.schema.json`,
`scripts/continuity_check.py`.

## QC loop

Use:

```text
GENERATE → INSPECT → CLASSIFY → REPAIR → REGENERATE → COMPARE → ACCEPT
```

Score each clip 0–5 on the QC scorecard (identity, style, anatomy, motion, physics, camera,
composition, lighting, background, objects, text, audio, temporal stability, continuity,
performance). Pass at ≥ 4 average with no item below 3.

Failure categories: IDENTITY, STYLE, ANATOMY, MOTION, CAMERA, COMPOSITION, PHYSICS,
LIGHTING, BACKGROUND, OBJECTS, TEXT, AUDIO, TEMPORAL, CONTINUITY, TOOL_ERROR.

Never repeatedly rewrite a prompt without identifying the failure class. Change one
variable per attempt and re-score.

## Risk and cost

Score each shot's `risk_level` (low/medium/high/critical) from subject, motion, continuity,
duration, physics, and text/hands/faces complexity. Set `attempt_budget` accordingly
(low 2, medium 4, high 8, critical 12).

Ladder: text preview → keyframe → image-to-video → multi-keyframe. Lock style and identity
on the cheapest representative shot before bulk generation; generate hero shots last. After
three same-class failures, change the layer, not the wording. Details: `references/risk-cost.md`.

## Multi-agent mode

If the host supports subagents, roles may include:

SHOWRUNNER, STORY_EDITOR, DIRECTOR, CINEMATOGRAPHER, CHARACTER_DESIGNER,
PRODUCTION_DESIGNER, STORYBOARD_ARTIST, PROMPT_ENGINEER, MODEL_ADAPTER, AUDIO_DIRECTOR,
EDITOR, CONTINUITY_SUPERVISOR, QC_AGENT.

One writer per artifact; hand off artifacts, not paraphrases; CONTINUITY_SUPERVISOR holds a
veto on canon. If subagents are unavailable, perform the roles sequentially and still
produce every artifact. Contracts: `references/multi-agent.md`.

## Multi-model mode

Different shots may use different models. Track:

```text
shot → model → adapter version → result → verdict
```

while preserving the same story, character bible, world bible, style bible, continuity
ledger, and `SHOT_SPEC`.

Do not declare a permanent universal "best model." Select by shot requirement and verified
capability.

## Reproducibility

Append one line per attempt to `runs.jsonl` with: shot_id, attempt, model, adapter version
and verification date, prompt hash and version, seed, references, generation method,
duration, result path, QC verdict, and notes.

Lock in this order: seed → keyframe → references → prompt hash → model version. Never
retro-attribute an old shot to a new model. `references/reproducibility.md`.

## Deliverables

For a complete production request, prefer these artifacts:

- `project.json`
- `story.md`
- `script.md`
- `characters.md`
- `locations.md`
- `style.md`
- `continuity.json`
- `beats.json`
- `shots.json`
- `storyboard.md`
- `image-prompts.md`
- `video-prompts.md`
- `model-exports/`
- `audio-plan.md`
- `edit-plan.md`
- `runs.jsonl`
- `qc-report.json` (or `qc-report.md`)
- `evaluation.md`

Produce the subset the format requires (`references/formats.md`) plus anything the user
explicitly asked for. Never deliver generated media without its spec and QC verdict.

## Tooling

Deterministic helpers (Python 3.9+, standard library only):

| Command | Purpose |
|---|---|
| `python scripts/new_project.py <dir>` | scaffold a project from the templates |
| `python scripts/shot_budget.py --duration 480 --format short_film` | plan scenes/shots summing to runtime |
| `python scripts/validate.py <path>` | validate project/beats/shots/continuity/QC/adapter against schemas |
| `python scripts/prompt_compile.py shots.json --shot shot-001 --format both` | compile image + video prompts |
| `python scripts/continuity_check.py shots.json continuity.json` | detect canon/state/geography drift |
| `python scripts/manifest.py` | regenerate `MANIFEST.json` (hashes + sizes) |
| `python scripts/lint_skill.py` | check skill structure, front matter, links, manifest freshness |
| `python scripts/run_evals.py` | run machine evals in `evals/` |

Use them when available; reproduce their logic by hand when not. Never fabricate their output.

## Formats

Format changes structure, pacing, aspect, and audio emphasis. Read
`references/formats.md` for narrative short, anime episode, trailer, teaser, music video,
documentary, commercial, explainer, vertical short, and series pilot.

## Portability rule

The project must remain useful if the current agent, model, provider, editor, or API is
replaced.

Do not hard-code a provider into the creative plan. Provider-specific prompts are exports,
never the canonical project.

## Safety and rights

Do not fabricate provider capabilities, access credentials, or tool results. Respect the
user's rights and permissions for source media, voices, characters, music, likenesses, and
copyrighted material. If a requested workflow requires a capability that is unavailable,
state the limitation and provide the portable artifact instead.

Also: state uncertainty instead of guessing, flag content that needs consent or licensing,
and never present a generated asset as a real recording of a real person or event.

## Failure protocol

When something blocks production:

1. name the blocker (missing canon, unverified capability, rights issue, tool error);
2. state the smallest change that unblocks it;
3. deliver the artifacts completed so far, marked as incomplete;
4. do not silently substitute an unverified capability or a weaker compromise.

## Versioning

Skill version, schema version, and adapter versions are independent. Backward-compatible
additions bump the minor version; breaking schema changes bump the major version and are
documented in `CHANGELOG.md` and `docs/versioning.md`.
