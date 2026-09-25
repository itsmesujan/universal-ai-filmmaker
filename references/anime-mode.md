# Anime / Animation Mode

Prioritise character identity, silhouette, facial readability, costume continuity,
expressive posing, cel/line rendering, stylised motion, effects, and readable action.

## Priorities in order

1. **Identity** — the audience must recognise the character in every shot. Lock the face
   sheet, hair, costume, and palette as canon (`bibles.md`).
2. **Silhouette** — design poses that read as solid shapes. Silhouette carries action and
   emotion in animation.
3. **Facial readability** — eyes and mouth must be legible at the shot size you chose;
   pick the shot size that shows the intended expression.
4. **Line/cel consistency** — line weight, shadow shapes, and highlight style come from the
   style lock and stay verbatim across shots.
5. **Effects** — speed lines, impact frames, smears, particles: assign each effect to a
   specific shot and layer, and keep them from covering the character.
6. **Stylised motion** — snap, hold, and smear beats. Animation tolerates exaggeration in
   wide shots and restraint in close-ups.

For action sequences use:

`PREPARATION → ACTION/IMPACT → REACTION → CONSEQUENCE`

Detailed shot breakdown: `action-choreography.md`.

## Rules

- Never mix photorealism with anime style unless the mixing rule is explicitly declared in
  the style bible (e.g. stylised flashbacks only).
- Recurring canonical prompts and reference sheets are mandatory for repeated characters
  and locations.
- Keep background style stable inside a scene; background detail drift is the most common
  anime continuity failure.
- Avoid crowd and complex machinery shots unless the design is simple enough to hold.
- Text (signs, subtitles, phone screens) is unreliable: plan it as a post element.

## Anime token defaults

| Intent | Grammar |
|---|---|
| emotional beat | medium_close/close, static, soft rim, palette accent |
| action impact | impact frame, speed lines, high contrast, directional blur |
| establishing | wide, painted background, slow truck |
| comedy beat | snap cut, exaggerated pose, flat lighting, hold |
| tension | extreme_close on eye, static, high contrast, silence |

## Anti-patterns

- photoreal skin texture, lens flare spam, or film grain in a cel-shaded project
- facial structure drift between cuts (different eye shape, different nose)
- costume detail changes (collar shape, sleeve length, accessory loss)
- effect layers that hide the character or read as noise
- 3D-style motion with 2D rendering without a declared rule

## Reference example

```text
Shot: close-up, Hana realises she is alone.
Pose: shoulders dropped, umbrella held loosely, eyes widening 5%.
Rendering: 2D cel, ink lines 2 px at 1080p, two-tone shadows, teal-amber palette.
Effects: faint rain streaks in foreground only, no speed lines.
Motion: eye widen (3 frames), hold (12 frames), slight head tilt.
Continuity: uniform v1, hair hana_v1, red umbrella prop:v1 in right hand.
```
