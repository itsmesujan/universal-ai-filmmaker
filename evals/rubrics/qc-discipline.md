# Rubric — QC Discipline

Score each dimension 0–5 for a completed QC report over a generated scene.

| Dimension | 0 | 3 | 5 |
|---|---|---|---|
| Coverage | not every shot scored | all shots scored | all shots scored against a defined threshold |
| Classification | "looks wrong" | failure class named | class named plus the layer that explains it |
| Repair reasoning | prompt rewritten blindly | one variable changed | smallest-layer fix, with the layer justified |
| Attempt hygiene | repeated identical retries | attempts counted | stop rule applied after three same-class failures |
| Evidence | verdict without evidence | scores and notes | scores, notes, and run-log entries linked |
| Compromise honesty | silent acceptance | compromise mentioned | compromise recorded, scoped, and approved |
| Continuity | ledger ignored | ledger consulted | ledger updated with violations and decisions |

**Ship** at ≥ 28/35. A QC pass that cannot point at evidence is not a pass; it is an opinion
that will be re-litigated after the next generation run.

## Automatic checks

```bash
python scripts/validate.py qc-report.json     # structural: PASS below threshold, missing repairs
python scripts/continuity_check.py shots.json continuity.json
```
