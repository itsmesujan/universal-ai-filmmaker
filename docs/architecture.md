# Architecture

## Three layers, one source of truth

```text
Creative intent          story, characters, theme, emotion, dramatic purpose
      ↓
Cinematic execution      blocking, framing, camera, lighting, motion, sound, edit
      ↓
Universal SHOT_SPEC      provider-neutral record of one shot
      ↓
Model adapter            capability map → provider syntax
      ↓
Image / video / audio generator
```

The canonical source of truth is **project state + `SHOT_SPEC`**, never a provider prompt.
Provider prompts are compiled exports; if the model changes, you regenerate the export and
keep the film.

## Why this split exists

| Failure you have seen | Structural cause | What this architecture does |
|---|---|---|
| A great prompt that cannot be repeated | prompt was the only artifact | spec is the artifact, prompt is derived |
| Characters changing between clips | no canon | versioned canon ids in a ledger |
| Rewriting everything when the model changes | provider hard-coded into the plan | adapter is a replaceable snapshot |
| Cost spiralling with no improvement | no risk model, no attempt budget | risk axes + attempt budgets + ladder |
| "It got better" with no evidence | nothing measured | QC scorecard, evals, run logs |

## The artifacts and their roles

| Artifact | Role | Authority |
|---|---|---|
| project manifest | format, runtime, scenes, budget, production state | scheduling |
| story / script | creative intent | story |
| bibles | canon appearance, world, style | identity and look |
| continuity ledger | versioned canon plus changing states | continuity |
| beats | dramatic units and their turns | dramaturgy |
| `SHOT_SPEC` list | the specification of every shot | production |
| compiled prompts | adapter-ready text derived from specs | derived, disposable |
| run log | provenance of every attempt | audit |
| QC report | verdict per clip | acceptance |

Rule: when a clip and the ledger disagree, the clip is wrong — unless the ledger was
deliberately versioned to a new canon id.

## Portability

1. Nothing in the creative layer names a provider.
2. Adapters are snapshots with a verification date and explicit `unknown`s.
3. Missing capabilities are handled by `degraded_mode`, which is documented, not hidden.
4. Any `SHOT_SPEC` must be exportable to a different model without redesign.

A useful test: could a different operator, with a different set of models, produce a
recognisably similar film from these artifacts alone? If not, the plan is not portable.

## Determinism and tools

Mechanical work is delegated to dependency-free Python:

```text
scripts/uaf_lib.py          schema subset, canon ids, prompt compiler, risk scoring
scripts/validate.py         schema + semantic validation
scripts/prompt_compile.py   SHOT_SPEC → image/video prompts + lint
scripts/shot_budget.py      runtime → scene/shot plan
scripts/continuity_check.py ledger vs shots drift detection
scripts/new_project.py      scaffold a project
scripts/manifest.py         repository manifest (hashes/sizes)
scripts/lint_skill.py       package integrity
scripts/run_evals.py        deterministic evals
```

Anything a script can decide deterministically should not be decided by an LLM: arithmetic,
schema conformance, id checks, and drift detection are all cheaper and more reliable as code.

## Where quality comes from

1. **Gates** — no stage begins before the previous one can be reviewed.
2. **Canon** — one written source for identity, world, and look.
3. **Compilation** — prompts derived from specs, so every shot is consistent and diffable.
4. **Classification** — failures diagnosed by class before anything is rewritten.
5. **Budgets** — spend attempts where they change the outcome.
6. **Evidence** — evals, QC scores, and run logs so improvement is provable.
