# Lighting and Colour Continuity

Light and colour are the cheapest way to make unrelated clips feel like one film, and
the fastest way to break that illusion.

## Lighting plan per scene

Record before shots are written:

- time of day and light source(s)
- motivation (what in the world creates the light)
- direction of key (screen-left / screen-right / front / back / top)
- quality (hard / soft / diffused / dappled)
- ratio (low / medium / high contrast)
- colour temperature (Kelvin or warm / neutral / cool)
- practicals visible in frame
- movement (static sun, flickering neon, passing headlights)
- continuity rule: which direction light comes from across the whole scene

The **continuity rule** matters most: once the key light is established screen-left, it
stays screen-left until a motivated change occurs (time passes, a lamp is switched,
the character turns). Unmotivated light flips are the classic AI-video tell.

## Colour script

Plan colour per act/scene, not per shot:

| Element | Meaning |
|---|---|
| base palette | 2–4 colours that define the film |
| scene palette | subset used in this scene |
| accent | single colour reserved for the story's subject or threat |
| progression | how saturation/value shift as tension rises or falls |
| skin-tone constraint | skin must stay inside a stable range for identity to hold |

Store palettes and the `STYLE_LOCK` in the style bible so every prompt reuses the same
words. Prefer explicit colour names plus hex where useful (`teal #1F4E5F`).

## Cross-shot consistency

- Fix a "hero frame" per scene and treat its lighting as the reference for all shots.
- Keep white balance stable inside a scene; let it shift only with motive.
- Match contrast level between coverage shots of the same scene, otherwise cuts read as
  location changes.
- Practicals must keep the same position, colour, and brightness between shots.
- Night is not black: define moon/neon/screen sources and keep silhouettes readable.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Colour drifts between shots | palette never locked in prompts | add STYLE_LOCK + palette to every shot |
| Cuts feel like new locations | contrast/white balance mismatch | re-keyframe against hero frame |
| Light direction flips | continuity rule missing | record direction per scene, restate in shot |
| Character looks like a different person | skin/exposure shift | lock skin range, restate in continuity block |
| Flat, unreadable night | no motivated source | add practicals, raise fill ratio |
| Overly saturated "AI look" | palettes unconstrained | lower saturation, add palette limits to constraints |
