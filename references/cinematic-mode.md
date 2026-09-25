# Cinematic Mode

Prioritise blocking, motivated camera movement, lens/composition language, lighting
continuity, production design, performance, eyelines, screen direction, depth, and sound
perspective.

## Priorities in order

1. **Blocking** — where bodies are in the space and how they move. Decide blocking before
   camera; camera follows actors, not the reverse.
2. **Motivated movement** — every move has a reason: reveal, follow, escalate, withhold.
3. **Lens discipline** — pick a lens per scene and stay near it. Mixing 18 mm and 135 mm
   inside one scene reads as a different film.
4. **Light continuity** — fix key direction and colour temperature per scene
   (`lighting-color.md`).
5. **Performance** — playable behaviour, eyelines, breath (`performance-direction.md`).
6. **Depth** — foreground/midground/background layers create the cinematic feel more than
   any "film look" phrase in a prompt.

## Rules

- Use camera movement only when it serves the scene. A static or restrained camera can be
  more cinematic than constant movement.
- Prefer 3–8 s shots with one event each; long takes of complex action fail.
- Keep the axis and eyelines consistent; use inserts/cutaways for reversals.
- Motivate light: window, practical, screen, fire. Avoid unmotivated "cinematic lighting".
- Direct reaction shots as carefully as action shots — they carry emotion.
- Treat sound as part of the shot: define what the camera would hear from this angle.

## Cinematic token defaults

| Scene type | Lens | Movement | Light |
|---|---|---|---|
| dialogue | normal/portrait | static or micro-drift | soft 3/4 key, low ratio |
| tense | normal/telephoto | slow push or static | side/back, high ratio |
| reveal | wide | reveal pan or dolly out | motivated source, motion allowed |
| scale/establishing | wide/ultra wide | crane or slow truck | ambient + practicals |
| isolation | portrait/telephoto | static | negative space, cool temp |

## Anti-patterns

- gratuitous drone/aerial shots with no story purpose
- constant movement, "epic" adjectives, and generic film-look spam
- photoreal skin plus stylised animation in the same scene without a declared rule
- coverage that ignores the axis
- unmotivated colour-temperature changes between shots of one scene

## Reference example

```text
Scene: night platform, one character.
Blocking: subject centre-left on the platform edge, train line background right.
Light: cool 5600K practicals screen-left, wet rim from background, ratio high.
Coverage: (1) wide establishing, static; (2) medium, slow push-in on the empty
platform; (3) close reaction, static; (4) insert on lowered umbrella, static.
Exit: match_cut from umbrella to platform clock.
```
