# Provider-Neutral Prompting

A useful prompt describes observable requirements. It is compiled from `SHOT_SPEC`, not
invented per shot. Use `prompt-compilation.md` for the algorithm and the linter.

## Image prompt blocks

`SUBJECT` → `APPEARANCE / REFERENCES` → `POSE` (start_state) → `COMPOSITION` →
`ENVIRONMENT` → `LIGHTING` → `CAMERA` (lens, angle, framing) → `STYLE` (STYLE_LOCK) →
`MOOD` → `CONTINUITY ANCHORS` → `CONSTRAINTS`.

## Video prompt blocks

`SUBJECT MOTION` → `CAMERA MOTION` → `ENVIRONMENT MOTION` → `TIMING` → `PERFORMANCE` →
`START STATE` → `END STATE` → `CONTINUITY` → `CONSTRAINTS`.

Order matters: models weight the beginning most. Put the action and motion before the
style block so style cannot swallow the event.

## Concrete beats vague

| Vague | Concrete |
|---|---|
| cinematic lighting | warm key screen-left, cool rim, high contrast |
| she is sad | eyes down, jaw tight, shallow breath, hand still on the rail |
| dynamic camera | slow 3 s push-in from medium to close |
| epic battle | two fighters, locked axis, impact insert, dust settling |
| 4K masterpiece | (delete — unverifiable and useless) |

## Image-to-video rules

- Do not restate what the reference frame already locks (costume, face, set) unless the
  model benefits; restate only what motion destroys: identity, direction, props, light.
- Describe motion that the model can actually perform in the clip length: one action,
  one camera move. Long complex choreography fails.
- Anchor the first and last visual states explicitly (`start_state`, `end_state`), since
  they are what the edit and the next shot depend on.

## Negative constraints

Use only constraints that address a known risk or a prior QC failure class. Three to six
specific constraints beat a generic wall of "no bad anatomy, no artifacts" spam, which
mostly degrades compliance.

## Length budget

Keep prompts proportional to shot complexity. As a working guide: subject and action
blocks carry the most detail; style and constraints stay short and constant across the
film (which is also how style stays stable).

## Examples

```text
IMAGE
[Hana: anime teenage girl, character:hana:v1] in a school uniform, black hair with a
low ponytail, standing under a red umbrella on a rain-soaked night platform; umbrella
raised at shoulder height, looking off screen left; medium shot, eye level, 35 mm
equivalent, subject left of centre with negative space right; commuter station at
night, wet concrete, fluorescent practicals, distant train lights; key light cool
5600K from screen-left, wet backlight rim, high contrast; 2D cel animation, visible
ink lines, muted teal-amber palette, soft volumetric rain, shallow depth of field;
quiet unease; keep uniform and umbrella unchanged; no other characters.

VIDEO (from the above frame)
Start: umbrella raised, weight on the back foot. She slowly lowers the umbrella to
shoulder height as her eyes widen slightly, then holds still; rain falls continuously,
a train light sweeps across the background once; camera does a slow 3 s push-in from
medium to medium close, ending on her face; breath visible, shoulders relaxing; end
state: umbrella lowered, gaze fixed off screen; keep uniform, umbrella, and light
direction unchanged; no camera shake, no extra characters.
```

## Anti-patterns

- quality spam, superlatives, and unverifiable claims
- contradictory camera instructions
- three or more simultaneous actions
- abstract emotions without behaviour
- provider-specific syntax inside a neutral prompt
- restating the whole bible in every prompt (use named blocks instead)
