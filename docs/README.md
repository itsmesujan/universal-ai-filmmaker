# Universal AI Filmmaker — Documentation

**Version 1.1.0** · [Project README](../README.md) · [Skill definition](../SKILL.md)

This directory is the human documentation. `../references/` holds the operational rules the
agent loads while working; `docs/` explains the system, the artifacts, and the tooling.

## Start here

| If you want to… | Read |
|---|---|
| produce something in the next ten minutes | [getting-started.md](getting-started.md) |
| understand why the skill is built this way | [architecture.md](architecture.md) |
| follow the production pipeline stage by stage | [workflow.md](workflow.md) |
| know what every file and field means | [data-model.md](data-model.md) · [shot-spec.md](shot-spec.md) |
| write better prompts | [prompting.md](prompting.md) |
| stop characters from drifting | [continuity.md](continuity.md) |
| judge and repair generated shots | [quality-control.md](quality-control.md) |
| export to a specific model safely | [model-adapters.md](model-adapters.md) |
| run this with subagents or a team | [multi-agent.md](multi-agent.md) |
| use the command line tools | [cli.md](cli.md) |
| measure whether output improved | [evals.md](evals.md) |
| reproduce a shot later | [reproducibility.md](reproducibility.md) |
| pick a structure for a trailer/ad/music video | [formats.md](formats.md) |
| understand versioning and compatibility | [versioning.md](versioning.md) |
| handle rights, consent, and safety | [security-and-rights.md](security-and-rights.md) |
| fix something that went wrong | [troubleshooting.md](troubleshooting.md) |
| get quick answers | [faq.md](faq.md) |
| look up a term | [glossary.md](glossary.md) |

## The one-paragraph version

The skill separates **creative intent**, **cinematic execution**, and **model adaptation**.
The canonical source of truth is the project state plus `SHOT_SPEC` records — never a
provider prompt. Prompts are *compiled* from the spec, continuity is tracked in a versioned
ledger, every generated clip is scored against a QC rubric, and every attempt is logged so
results can be reproduced. Deterministic Python tooling enforces the mechanical parts, and
machine evals plus human rubrics keep the standard from silently decaying.

## Reference index

The agent loads these on demand (`../references/`):

| Reference | Covers |
|---|---|
| `intent-routing.md` | request classification, state detection, gates |
| `workflow.md` | pipeline, per-state artifacts, coverage model |
| `story-and-script.md` | structure, scenes, screenplay conventions |
| `bibles.md` | character/world/style canon and versioned ids |
| `shot-grammar.md` | framing, lens, movement, composition, transitions |
| `lighting-color.md` | lighting plans, palettes, light continuity |
| `performance-direction.md` | emotion ladder, playable verbs, eyelines |
| `action-choreography.md` | action beats, axis, effects, damage tracking |
| `continuity.md` | ledger structure, drift classes, repair order |
| `prompting.md` | prompt blocks, i2v rules, anti-patterns |
| `prompt-compilation.md` | deterministic compilation and linting |
| `qc.md` | scorecard, failure taxonomy, repair table |
| `model-adaptation.md` | adapter protocol, tiers, degraded mode |
| `reproducibility.md` | run logs, determinism ladder, change control |
| `risk-cost.md` | risk axes, attempt budgets, generation ladder |
| `multi-agent.md` | role contracts and handoff protocol |
| `evaluation.md` | delivery rubric and repair map |
| `formats.md` | trailer, music video, documentary, commercial, vertical |
| `anime-mode.md` · `cinematic-mode.md` | mode-specific priorities |
| `audio-edit.md` | audio layers, sync, mixing, edit grammar |

## Conventions used in this documentation

- **Canon id** — `character:hana:v1`, `location:platform-4:v1`, `prop:red-umbrella:v1`.
- **Required vs recommended** — "must" is a gate; "prefer" is a default you may justify against.
- **Example project** — almost every page can be verified against
  `../examples/mini-project/`, a four-shot scene with a complete ledger.
