# Prompting

Prompts are **compiled** from `SHOT_SPEC`, not written per shot. Hand-written prompts drift,
drop continuity, and cannot be diffed across forty shots.

## Compile

```bash
python scripts/prompt_compile.py shots.json --shot shot-003 --format both
python scripts/prompt_compile.py shots.json --write video-prompts/
```

## Block order (fixed)

Image: `SUBJECT` → `APPEARANCE` → `POSE` → `ACTION` → `COMPOSITION` → `ENVIRONMENT` →
`LIGHTING` → `CAMERA` → `STYLE` → `PERFORMANCE` → `CONTINUITY` → `CONSTRAINTS`.

Video: `START STATE` → `SUBJECT MOTION` → `SECONDARY MOTION` → `CAMERA MOTION` →
`PERFORMANCE` → `TIMING` → `END STATE` → `CONTINUITY` → `AUDIO` → `CONSTRAINTS`.

Action and motion come **before** style: models weight the opening of a prompt, and a long
style block at the front will swallow the event.

## Real compiled output

```text
SUBJECT: Close-up of an anime teenage girl beginning to lower a red umbrella
APPEARANCE: character:hana:v1, prop:red-umbrella:v1
POSE: Hana in close-up, umbrella canopy entering the top of frame, eyes on the far end
ACTION: She lowers the umbrella to shoulder height as her eyes widen a fraction
COMPOSITION: close, eye level, subject center, screen direction center, headroom tight
ENVIRONMENT: location:platform-4:v1, night, rain
LIGHTING: key from screen-left, cool fluorescent platform light, soft, high contrast, 5600K
CAMERA: static, portrait lens, close front
STYLE: anime mode, 2D cel with painted background, style:main:v1
PERFORMANCE: Her eyes widen a fraction, she blinks once, and her shoulders drop, peak
CONTINUITY: costume school_uniform_v1, damage none, hair hana_v1, prop state red_umbrella_lowered
CONSTRAINTS: do not change her uniform, no extra characters, no tears
```

## Linting

```bash
python scripts/prompt_compile.py shots.json --lint
```

The linter rejects: provider syntax in a neutral prompt, quality spam, abstract emotion
without behaviour, unversioned canon references, references missing from the ledger,
multi-action `primary_action`, duplicate blocks, and empty prompts.

## Concrete beats vague

| Vague | Concrete |
|---|---|
| cinematic lighting | warm key screen-left, cool rim, high contrast |
| she is sad | eyes down, jaw tight, shallow breath, hand still on the rail |
| dynamic camera | 3 s push-in from medium to close |
| epic battle | two fighters, locked axis, impact insert, dust settling |
| 4K masterpiece | delete — unverifiable and useless |

## Image-to-video rules

1. Do not restate what the reference frame already locks (face, costume, set).
2. Restate only what motion destroys: identity, screen direction, props, light direction.
3. One action and one camera move per clip; long choreography fails.
4. Always define `start_state` and `end_state` — the edit and the next shot depend on them.

## Negative constraints

Three to six constraints that each address a known risk or a previous QC failure class.
A generic wall of "no bad anatomy, no artifacts" mostly degrades compliance; the linter
flags quality spam for that reason.

## Length budget

Subject and action carry detail; style and constraints stay short and identical across the
film. That repetition is exactly how the look stays stable.

## Conflict resolution

When fields disagree, resolve in this order and record the decision:

1. continuity ledger (canon)
2. scene lighting/colour plan
3. style bible / STYLE_LOCK
4. beat-level direction
5. the individual shot field

Never resolve a conflict by silently deleting canon.

## Anti-patterns

- rewriting prompts without classifying the failure first
- three or more simultaneous actions
- unmotivated camera movement stacked on complex action
- provider parameters inside a portable spec
- restating the whole bible in every prompt instead of using named blocks
- human-edited prompts that are not marked as such

See also: [`../references/prompt-compilation.md`](../references/prompt-compilation.md),
[`../references/prompting.md`](../references/prompting.md).
