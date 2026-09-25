# Universal AI Filmmaker

**Version 1.1.0** · [Documentation](docs/README.md) · [Skill definition](SKILL.md) · [Changelog](CHANGELOG.md)

A portable, agent-agnostic production skill for multi-shot AI films and animated videos —
cinematic shorts, anime, trailers, music videos, documentaries, commercials, explainers, and
vertical content.

## What it does

```text
idea → story → screenplay → bibles → beats → shots → storyboard → keyframes
     → compiled prompts → generation → audio → edit → QC → repair → final
```

The plan is deliberately independent of any one generator: prompts are *compiled* from a
canonical shot specification, continuity lives in a versioned ledger, every clip is scored
against a QC rubric, and every attempt is logged so results can be reproduced.

## What is new in 1.1.0

- **Routing and gates** — detect the production state before generating anything; bounded
  clarification (three questions maximum); explicit pass conditions per stage.
- **Deep craft references** — 13 new references covering story and script, bibles, shot
  grammar, lighting and colour, performance, action choreography, formats, prompt
  compilation, risk and cost, reproducibility, multi-agent contracts, evaluation, routing.
- **Deterministic tooling** — dependency-free Python for validation, prompt compilation,
  shot budgeting, continuity drift detection, project scaffolding, manifest keeping, and
  skill linting.
- **Machine evals + human rubrics** — six passing eval cases and three scoring rubrics,
  wired into CI.
- **Complete documentation** — a 20-page `docs/` set plus three new JSON Schemas (beats,
  continuity ledger, QC report).

## Architecture

```text
Creative intent
      ↓
Cinematic execution
      ↓
Universal SHOT_SPEC          (canonical, provider-neutral)
      ↓
Model adapter                (capability snapshot, dated)
      ↓
Video / image / audio generator
```

Change the model and you regenerate an export — not the film. See
[docs/architecture.md](docs/architecture.md).

## Quickstart

```bash
git clone https://github.com/itsmesujan/universal-ai-filmmaker.git
cd universal-ai-filmmaker

python scripts/run_evals.py                                  # sanity check, no dependencies
python scripts/new_project.py projects/demo --duration 90    # scaffold a project
python scripts/shot_budget.py --duration 90                  # plan scenes and shots
python scripts/validate.py examples/mini-project             # validate the example project
```

`projects/` is local scratch space for your own productions (git-ignored, and skipped by the
package tooling) — the repository ships the skill, not your film.

Then work the pipeline: [docs/getting-started.md](docs/getting-started.md).

## Installation

For an Agent Skills-compatible environment, install or upload the directory containing
[`SKILL.md`](SKILL.md). For OpenAI/Codex-style packaging, use the plugin package generated
alongside this repository.


## Repository layout

```text
.
├── SKILL.md              agent entry point: laws, pipeline, gates, tooling
├── references/           21 operating guides the agent loads on demand
├── templates/            project artifacts (JSON + Markdown)
├── schemas/              JSON Schemas: project, shots, beats, continuity, QC, adapter
├── model-adapters/       capability snapshot templates (never authoritative)
├── examples/             shot example, adapter example, complete mini project
├── scripts/              deterministic CLI tooling (stdlib only)
├── evals/                machine eval cases, fixtures, human rubrics
├── docs/                 human documentation (20 pages)
├── .github/workflows/    CI: lint, manifest, validate, evals
├── CONTRIBUTING.md
└── CHANGELOG.md
```

## Tooling

| Command | Purpose |
|---|---|
| `python scripts/new_project.py <dir>` | scaffold the canonical artifact set |
| `python scripts/shot_budget.py --duration 480` | plan scenes/shots that sum to the runtime |
| `python scripts/validate.py <path>` | schema and semantic validation |
| `python scripts/prompt_compile.py shots.json --shot shot-001` | compile neutral prompts |
| `python scripts/prompt_compile.py shots.json --lint` | reject prompt defects |
| `python scripts/continuity_check.py <project-dir>` | detect identity/state/geography drift |
| `python scripts/manifest.py --check` | verify repository manifest freshness |
| `python scripts/lint_skill.py` | package integrity |
| `python scripts/run_evals.py` | run the machine evals |

Full reference: [docs/cli.md](docs/cli.md).

## Evidence it works

```text
$ python scripts/run_evals.py
PASS  continuity-detects-costume-drift (continuity)
PASS  mini-project-schemas (validate)
PASS  prompt-compile-anime-shot (prompt_compile)
PASS  prompt-lint-catches-provider-syntax (prompt_compile)
PASS  risk-scores-moderate-shot (risk)
PASS  shot-budget-360s (shot_budget)

evals: 6/6 passed
```

`examples/mini-project/` is a complete four-shot scene (42 s) with a full continuity ledger
that validates cleanly and reports no drift.

## Core rules

1. Route before you generate — detect the state, then work one gate at a time.
2. One action, one camera move, one environmental motion per shot.
3. Canon ids are versioned (`character:hana:v1`); never edit a version in place.
4. Compile prompts from `SHOT_SPEC`; never improvise prose per shot.
5. Verify model capabilities before claiming them; record `unknown` otherwise.
6. Classify a failure before repairing it; fix the smallest layer.
7. Score every clip and record the verdict and any compromise.
8. Log provenance (model, adapter, seed, prompt hash, references) for accepted shots.
9. Keep the plan portable — a provider change must not destroy the film.
10. Never fabricate capabilities, credentials, or tool results.

## Portability

The core skill assumes no particular provider or model is available. Model adapters are
separate snapshots: verify the provider's current documentation before using one. If a
required capability is unavailable, the skill states the limitation, records a degraded-mode
fallback, and still delivers the portable artifacts.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Keep the core provider-neutral, add an eval case for
every lesson learned, and run the CI sequence before opening a pull request.

## License

MIT. See [LICENSE](LICENSE).
