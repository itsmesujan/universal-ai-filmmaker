# Universal AI Filmmaker

**Version 1.0.0**

A portable, agent-agnostic production skill for creating multi-shot AI films and animated videos.

It is designed for cinematic stories, anime, animation, trailers, music videos, documentaries, commercials, and other long-form or multi-shot projects.

## What it does

The skill turns:

**idea → story → screenplay → character/world/style bibles → beats → shots → storyboards → keyframes → model prompts → generation → audio → edit → QC → repair → final**

The core filmmaking plan is deliberately independent of any one video generator.

## Architecture

```text
Creative Intent
      ↓
Cinematic Execution
      ↓
Universal SHOT_SPEC
      ↓
Model Adapter
      ↓
Video / Image / Audio Generator
```

This means a project can change models without rewriting the underlying story or shot design.

## Repository

```text
.
├── SKILL.md
├── references/
├── templates/
├── schemas/
├── model-adapters/
├── examples/
├── .github/workflows/
├── LICENSE
├── CONTRIBUTING.md
└── CHANGELOG.md
```

## Installation

For an Agent Skills-compatible environment, install or upload the skill directory containing `SKILL.md`.

For OpenAI/Codex-style packaging, use the included plugin package generated alongside this repository.

## Important portability rule

The core skill does **not** assume that any particular provider or model is available.

Model adapters are separate. Before using an adapter, verify the provider's current documentation and capabilities.

## Typical 5–10 minute project

A 5–10 minute film should normally be decomposed into multiple scenes and short shots rather than generated as one giant video request.

The exact shot count depends on pacing, dialogue, action, and generation method.

## Canonical source of truth

The permanent source of truth is:

- project manifest
- story
- character bible
- world/location bible
- style bible
- continuity ledger
- universal shot specifications

Provider-specific prompts are exports, not the canonical project.

## Validation

The repository includes JSON Schemas for project, shot, and model-adapter files.

GitHub Actions validates the repository structure and JSON files on push and pull request.

## License

MIT. See `LICENSE`.
