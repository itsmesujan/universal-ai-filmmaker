# Bibles: Character, World, Style

Bibles are the canon that keeps 30+ generated shots looking like one film. They are
written once, referenced by ID everywhere, and changed only deliberately.

## Canonical IDs

Every recurring asset gets a stable ID and a version:

```text
character:hana:v1
location:platform-4:v1
prop:red-umbrella:v1
style:main:v1
voice:hana:v1
```

Rules: lowercase, hyphen-separated, no spaces, version suffix always present. A new
version is a new ID. Shots reference IDs in `reference_assets` and `continuity`.

## Character bible

Identity → role, motivation, fear, desire, arc.
Canonical appearance → face, hair, eyes, body, height, costume, accessories, palette.
Performance → voice, movement style, expression rules, posture, gait.
References → portrait, full body, turnaround, expression sheet, signature pose.

Write appearance as **observable, repeatable facts** ("left cheek scar, 2 cm, under
the left eye"), never as adjectives that a model cannot hold ("beautiful").

Track immutable vs mutable:

| Layer | Changes during a film? |
|---|---|
| face shape, proportions, eye colour | no |
| hair length/state | only at deliberate story events |
| costume | only at deliberate story events (record the switch in continuity) |
| injuries, dirt, wetness, damage | yes — record per scene |
| emotional state | yes — record per beat |

## World / location bible

Architecture, layout, materials, entrances/exits, landmarks, time period, weather,
lighting sources, props, and continuity anchors. Add a rough plan view (text is fine)
that fixes: which way is north, where the door is, where the light comes from, and
where the camera may stand.

## Style bible

Medium, realism level, animation type, line quality, shading, texture, lighting logic,
colour logic, contrast, lens language, camera language, motion language, editing
language, and the reference frames that define "on-style".

Add a **style lock statement** — one paragraph reused verbatim in every prompt so the
look does not drift. Store reusable fragments as named blocks:

```text
STYLE_LOCK: 2D cel animation, visible ink lines, muted teal-amber palette,
soft volumetric rain, 24 fps, shallow depth of field, no photoreal skin texture.
```

## Bible hygiene

- One writer per bible; versions bump on any visible change.
- Every shot's `style.mode` and `reference_assets` must resolve to a bible entry.
- New props introduced mid-film must be added to the world bible before generation.
- Contradictions between bibles are blockers, not creative freedom.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Character drifts between shots | appearance written loosely | rewrite canon as measurable facts + reference sheet |
| Style drifts | no style lock | add STYLE_LOCK and reuse verbatim |
| Locations don't match | no plan view / landmarks | add layout + landmarks, re-keyframe |
| Costume chaos | costume change untracked | record switch events in continuity ledger |
