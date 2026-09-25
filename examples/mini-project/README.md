# Mini Project — Rain Platform

A deliberately small, complete example project used by the CI workflow, the evals, and
the documentation. It is the reference for "what good artifacts look like".

- 42 s total planned runtime, 1 scene, 4 shots (10 + 12 + 12 + 8)
- One character, one location, one prop, one lighting direction, one locked axis
- Every reference uses a versioned canon id (`character:hana:v1`)

## Files

| File | Purpose |
|---|---|
| `project.json` | manifest, format, scenes, creative intent |
| `beats.json` | two beats with mapped shots |
| `shots.json` | four full SHOT_SPEC records |
| `continuity.json` | canon ledger, prop history, emotional chain |

## Commands

```bash
python scripts/validate.py examples/mini-project
python scripts/continuity_check.py examples/mini-project
python scripts/prompt_compile.py examples/mini-project/shots.json --shot shot-003
python scripts/prompt_compile.py examples/mini-project/shots.json --lint
```

## What this example demonstrates

1. **One action per shot.** Each `primary_action` is a single event.
2. **Coverage with a purpose.** establishing → subject → reaction → insert.
3. **Locked continuity.** The same costume, hair, prop state chain, and key-light
   direction across every shot of the scene.
4. **Risk budgeting.** `risk_level` and `attempt_budget` are declared per shot.
5. **Emotional chain.** `shot-00N.end` matches `shot-00N+1.start` in the ledger.

## What it deliberately omits

Generated media, storyboard panels, and QC verdicts — the example stops at the SHOTS
gate so the specification, not the render, is the object under review.
