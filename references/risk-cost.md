# Risk, Attempt Budgets, and Cost Discipline

Generation is expensive. Spend attempts where they change the outcome.

## Risk scoring

Score each shot 0–2 on each axis, sum, then map to `risk_level`:

| Axis | 0 | 1 | 2 |
|---|---|---|---|
| subject complexity | 1 subject | 2–3 | crowd / children / animals |
| motion complexity | static/simple | moderate | multi-body, contact, airborne |
| continuity dependency | self-contained | shares one canon asset | many overlapping anchors |
| duration | short clip | medium | near model limit |
| physics/effects | none | simple effects | destruction, water, fire |
| text/hands/faces | none | hands or face | both plus text |

Total 0–3 → `low`, 4–6 → `medium`, 7–9 → `high`, 10–12 → `critical`.

## Attempt budget

| risk_level | Attempts | Escalation |
|---|---|---|
| low | 2 | re-prompt once, then accept best |
| medium | 4 | tweak prompt → keyframe → regenerate |
| high | 8 | keyframe test → simplify action → alternate model |
| critical | 12 | redesign the shot into multiple shots |

Stop rules:

- 3 failures with the same failure class → change a layer, not the wording.
- Budget exhausted → fall back down the ladder and record the compromise.
- Never regenerate an accepted shot to "try for better" unless QC flagged it.

## The generation ladder

Cheapest first, always:

1. text prompt only (preview, low resolution, fast mode)
2. keyframe image → image-to-video
3. approved keyframe → multi-keyframe interpolation
4. reference-video / style transfer (only with verified support)

Lock style and identity with the cheapest rung that is representative. Lock
continuity-heavy shots (recurring characters) after locking the style.

## Order of work

1. Build the bibles.
2. Generate the **style test shot** (representative, low risk).
3. QC the style test. Iterate on bibles, not on the shot.
4. Generate one coverage set per scene to validate geometry and light.
5. Bulk-generate low-risk shots.
6. Generate hero and high-risk shots last, with the full budget available.
7. Regenerate only failures.

## Batch strategy

- Batch by scene, never by random shots: consistency improves when adjacent shots share
  references.
- Keep the same seed/reference set for shots that must match.
- Log per-attempt results so a later reviewer can tell luck from method.

## Stop-loss

If the failure rate inside a scene exceeds roughly half its shots, the problem is the
design, not the prompts: return to the KEYFRAMES or SHOTS gate and simplify.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Budget burned early | hero shot attempted first | reorder: cheap representative shot first |
| Endless near-misses | no escalation rule | apply the 3-failure stop rule |
| Cost per finished second explodes | too many complex shots | split action, reduce effects per shot |
| Inconsistent results | shots batched randomly | batch per scene with shared references |
