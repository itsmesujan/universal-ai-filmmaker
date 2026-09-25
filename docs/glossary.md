# Glossary

**Adapter** — a capability snapshot that translates a `SHOT_SPEC` into one generator's inputs;
replaceable, dated, and never the source of truth.

**Attempt budget** — the number of generations allowed for a shot before escalating
(low 2, medium 4, high 8, critical 12).

**Axis / 180° line** — the imaginary line between subjects; the camera stays on one side so
screen direction stays consistent.

**Beat** — the smallest dramatic unit with a turn; mapped to shots in `beats.json`.

**Bible** — canon document for characters, locations, or style. Written once, referenced by
versioned id.

**Canon id** — a versioned asset identifier: `character:hana:v1`, `location:platform-4:v1`.

**Coverage** — the set of shots used for one beat: establishing, subject, action, insert,
reaction, transition.

**Coverage role** — which of those a specific shot provides.

**Degraded mode** — the documented fallback used when a model lacks a planned capability.

**Drift** — any divergence between a generated clip and the ledger: identity, state, or
geography.

**Emotion ladder** — the four performance stages of a beat: neutralise, build, peak, release.

**Gate** — a checkpoint that must pass before the next pipeline state begins.

**Generation ladder** — cheapest-first escalation: text preview → keyframe → image-to-video →
multi-keyframe.

**Ledger** — `continuity.json`: canon, states, geometry, emotional chain, and logged violations.

**Negative constraint** — a prompt restriction traceable to a known risk. Not a generic wall
of "no bad anatomy".

**pipeline state** — position in IDEA → … → FINAL; determines what work resumes.

**Prompt compilation** — deterministic assembly of prompt text from a `SHOT_SPEC` in fixed blocks.

**Provenance** — the record of what produced an asset: model, adapter version, seed, prompt
hash, references.

**QC scorecard** — 0–5 scoring across 15 checks; pass is average ≥ 4.0 with nothing below 3.

**Risk level** — low/medium/high/critical derived from subject, motion, continuity, duration,
physics, and text/hands/faces complexity.

**Run log** — `runs.jsonl`: one JSON object per generation attempt; append-only.

**SHOT_SPEC** — the canonical, provider-neutral record of one shot.

**STYLE_LOCK** — a paragraph reused verbatim in every prompt so the look does not drift.

**Screen direction** — the direction of travel or eyeline in frame; locked per scene.

**Storyboard** — per-shot framing/axis/staging documentation; panels optional, spec required.

**Style bible** — canon for medium, rendering, palette, lens and motion language, plus STYLE_LOCK.

**Template** — a fill-in artifact under `../templates/`; contains placeholders and is not a
valid instance.

**Turn** — what changes in a beat or scene. No turn means it is not a beat.

**Validation** — schema plus semantic checks (`../scripts/validate.py`); shape and sanity.

**Veto (continuity)** — the authority to reject a shot that violates the ledger.

**Workflow state detection** — probing artifacts to find where a project actually is before
producing anything.
