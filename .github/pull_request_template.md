## Summary

Describe the change.

## Why

Explain the problem or use case. If this fixes a real failure, say what went wrong in
practice.

## Validation

- [ ] `python scripts/lint_skill.py` passes
- [ ] `python scripts/manifest.py --check` passes (or MANIFEST.json was regenerated)
- [ ] `python scripts/validate.py examples model-adapters` passes
- [ ] `python scripts/run_evals.py` passes
- [ ] JSON files parse successfully
- [ ] `SKILL.md` remains valid (front matter name, description ≤ 1024 chars, version)
- [ ] Provider-neutral core remains provider-neutral
- [ ] Documentation updated in `docs/` if behaviour changed
- [ ] CHANGELOG entry added

## Tests and evidence

Paste the commands you ran and their output (eval summary, validator summary, or both).

## Compatibility

Does this change affect project/shot/beats/continuity/QC schemas or existing projects? If
yes, state whether 1.0 files remain valid and link the migration note in
[docs/versioning.md](../docs/versioning.md).

## Eval coverage

Which eval case (new or existing) proves this change? If none applies, explain why.

\n
