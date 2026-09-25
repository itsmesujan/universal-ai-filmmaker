# Prompt Compilation

Compile prompts from `SHOT_SPEC` deterministically. Do not write freehand prose per
shot: hand-written prompts drift, drop continuity, and cannot be diffed.

`scripts/prompt_compile.py` implements this algorithm. Use it when available.

## Assembly order (image)

```text
SUBJECT            subject + canonical ID + version
APPEARANCE         observable facts from the character bible
POSE / START STATE start_state
ACTION             primary_action (single event)
COMPOSITION        framing, angle, lens, subject position
ENVIRONMENT        location ID, time, weather, set dressing
LIGHTING           direction, quality, ratio, temperature, practicals
STYLE              STYLE_LOCK + style.mode
MOOD               emotional read implied by grammar
CONTINUITY         only the anchors that can drift
CONSTRAINTS        only risks known for this shot
```

## Assembly order (video)

```text
START STATE        inherited end_state of the previous shot
SUBJECT MOTION     primary_action, with timing
SECONDARY MOTION   environment/background motion (one)
CAMERA             one primary movement + optional motivated secondary
PERFORMANCE        playable behaviour and emotion ladder stage
TIMING             duration_target and pacing (e.g. "hold 1.5 s, then react")
END STATE          the state the next shot must inherit
CONTINUITY         anchors + screen direction
CONSTRAINTS        only known risks; no generic spam
```

## Linting rules (run before emitting)

1. No provider syntax in a neutral prompt (`--ar`, `--motion`, API parameters).
2. No contradictions (`static camera` + `whip pan`, `hands at sides` + `raising the cup`).
3. Exactly one primary action and one primary camera movement.
4. Every referenced asset ID must exist in the bibles.
5. No unverifiable claims ("8K HDR masterpiece") and no quality spam.
6. No abstract emotion without an observable behaviour.
7. For image-to-video, do not restate what the reference frame already locks — restate
   only what motion can destroy (identity, costume, props, direction).
8. Constraints must be traceable to a `risk_level` or a prior QC failure.
9. Screen direction, key-light direction, and costume/state version appear exactly once.
10. Total prompt stays inside the target model's context/prompt budget; trim adjectives,
    never continuity.

## Conflict resolution

When two fields disagree, resolve in this order and record the decision:

1. continuity ledger (canon)
2. scene lighting/colour plan
3. style bible / STYLE_LOCK
4. beat-level direction
5. the individual shot field

Never resolve a conflict by silently deleting canon.

## Reuse blocks

Keep reusable fragments in the bibles and reference them by name so the same text is
used verbatim across shots:

```text
STYLE_LOCK        the look
IDENTITY_HANA     face/hair/costume facts
CHARACTER_BLOCK   performance rules for the character
LOCATION_BLOCK    layout + landmarks for the location
```

## Prompt provenance

Record for each compiled prompt: `prompt_version`, source `shot_id`, adapter used,
compiled hash, and whether it was human-edited. Human-edited prompts must be marked so
that later recompiles do not silently discard the edit.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Drift across shots | freehand prompts | recompile with the compiler, reuse blocks |
| Model ignores the action | prompt leads with style | put action and motion before style |
| Style overwhelms identity | style text too long | shorten style block, lead with subject |
| Constraint ignored | huge generic negative list | keep constraints specific and few |
| Same shot never converges | contradictory prompt | run the linter, resolve the conflict |
