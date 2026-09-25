# Contributing

Contributions are welcome. This repository is a *skill package*: prose, schemas, templates,
tooling, and evals that must all agree with each other.

## Principles

1. Keep the core skill provider-neutral.
2. Do not claim a model capability without verification.
3. Keep creative intent separate from model-specific syntax.
4. Prefer reusable references and schemas over duplicated instructions.
5. Preserve backward compatibility for project and shot schemas where practical.
6. Add or update examples when changing the workflow.
7. If a change fixes a real failure, add an eval case that would have caught it.
8. Anything deterministic belongs in `scripts/`, not in prose.

## Before you open a pull request

Run the full CI sequence locally — each command exits non-zero on failure:

```bash
python scripts/lint_skill.py
python scripts/manifest.py --check
python scripts/validate.py examples model-adapters
python scripts/run_evals.py
python scripts/manifest.py          # after adding/removing/editing any file
```

CI runs the same steps on push and pull request
(`.github/workflows/validate.yml`).

## Adding or changing a reference

- `references/` holds operational rules the agent loads on demand: imperative, compact,
  decision-oriented. `docs/` holds human explanation. Do not duplicate one into the other;
  link instead.
- Every reference ends with a **Failure modes** table (`Symptom | Cause | Fix`).
- Reference new files from `SKILL.md` (load table) and `docs/README.md` (reference index).
  `lint_skill.py` errors when `docs/README.md` misses a docs page and warns when it misses a
  reference.

## Changing a schema

- Additive optional fields are minor; removals or retypings are major.
- New enums must include an escape value (`other`, `unknown`) so exotic-but-real values stay valid.
- Keep `additionalProperties: true` where practical so unknown fields survive round trips.
- Update `docs/data-model.md`, `docs/versioning.md`, and `CHANGELOG.md` in the same change.
- Validate the examples: `python scripts/validate.py examples`.

## Adding tooling

- Python 3.9+, standard library only, no network access, no credentials.
- Share helpers through `scripts/uaf_lib.py`; do not copy them.
- Exit non-zero on failure and print actionable messages.
- Write UTF-8 explicitly: `open(..., encoding="utf-8")`.

## Adding a template

- Templates contain `{{placeholder}}` values and are therefore **not** valid instances.
  Name them such that `validate.py` skips them (`*template*`) or place them in `templates/`.
- New scaffold files must be registered in `TEMPLATE_FILES` inside `scripts/new_project.py`.

## Model adapters

An adapter must document: provider, model, `model_type`, `adapter_version`, `verified_at`,
`docs_url`, capabilities, limits, failure modes, translation notes, and `degraded_mode`.

Unverified capabilities are the string `"unknown"` — never `true`, never a guess.
Adapters are capability snapshots, not permanent guarantees, and placeholder adapters must
carry `"placeholder": true`.

## Evals

Add a case when you:

- fix a bug (the fixture should reproduce it),
- change prompt compilation, budgeting, risk scoring, or continuity detection,
- introduce a new artifact type.

Put inputs in `evals/fixtures/<name>/` and cases in `evals/cases/<id>.json`. Run
`python scripts/run_evals.py --only <id>`.

## Pull requests

Explain:

- what changed;
- why it changed;
- whether schemas changed;
- whether existing projects remain valid;
- which commands you ran and what they printed.

## Commit messages

Conventional and specific: `feat(schemas): add beats schema`,
`fix(risk): match values only when scoring text risk`, `docs(cli): document --strict`.
