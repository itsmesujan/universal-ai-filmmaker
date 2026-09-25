# Versioning and Compatibility

Three version numbers move independently:

| Version | Where | Meaning |
|---|---|---|
| **skill** | `SKILL.md` front matter `metadata.version` | the package (references, tools, docs) |
| **schema** | `project.json`, `continuity.json`, `qc-report.json` `schema_version` | data contracts |
| **adapter** | `adapter_version` in each adapter | capability snapshot |

## Current versions

| Thing | Version |
|---|---|
| skill | 1.1.0 |
| schema | 1.1 (also accepts 1.0 files) |
| adapter template | 1.1.0 |

## Semver rules for the skill

- **Patch** (1.1.x): wording, typos, clarifications that change no behaviour.
- **Minor** (1.x.0): new references, new scripts, new optional fields, new eval cases.
- **Major** (x.0.0): a gate changes meaning, a required field changes, or an existing
  artifact becomes invalid.

## Schema evolution

1. **Additive** — a new optional field is a minor change.
2. **Restrictive** — new enums/patterns are documented as minor *if* an escape value
   (`other`, `unknown`) exists; otherwise they are major.
3. **Breaking** — removing or retyping a field is major and requires a migration note in
   [`../CHANGELOG.md`](../CHANGELOG.md).
4. `additionalProperties: true` is used where practical so unknown fields survive round trips
   instead of being silently dropped.

## Reading older projects

- A 1.0 project remains valid: 1.1 added optional fields (`beat_id` was already optional,
  `performance`, `timing`, `attempt_budget`, `production_state`, `budget`, `schema_version`
  bumps) and enums that include escape values.
- Missing optional fields are reported as warnings at most, never errors.
- `python scripts/validate.py project-dir` is the authority on what a project is missing.

## Migrating 1.0 → 1.1

Optional but recommended:

1. Set `project.json` `schema_version` to `"1.1"` and add `production_state` and `budget`.
2. Move continuity content into `continuity.json` with a `schema_version` of `"1.1"`.
3. Convert a single-shot example file into an array of shots (the schema has always
   required an array).
4. Add `performance`, `timing`, `attempt_budget`, and `prompt_version` to shots as they are
   next touched; there is no need to retrofit a finished film.
5. Start `runs.jsonl` before the next generation session.

## Deprecation policy

1. Announce the change in `../CHANGELOG.md` under `Deprecated`.
2. Keep reading the old shape for at least one minor release.
3. Remove it only in a major release, with a migration note.

## Adapter versions

Adapters are snapshots, not contracts. A provider update means a **new snapshot**
(`verified_at` bumped), never an edit to the meaning of an old one. Shots generated under an
older adapter stay attributable to it forever.

## What compatibility protects

The promise is narrow and concrete: **a project that validated yesterday still validates
today, and its prompts still recompile to the same text.** That is what makes the artifacts
safe to keep, share, and hand to a different operator or model.
