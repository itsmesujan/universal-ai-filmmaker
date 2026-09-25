# Troubleshooting

Symptom → likely cause → fix. Fix the smallest layer that explains the failure.

## Tooling

**`validate.py` reports "invalid JSON"**
The file has a trailing comma, a comment, or smart quotes. Fix the JSON, not the schema.

**`validate.py` says "expected type array" for a shots file**
Shot files are arrays. Wrap a single shot in `[ … ]`.

**`validate.py` says `MANIFEST.json is stale` (via `lint_skill.py`)**
Run `python scripts/manifest.py` — the hashes no longer match the files on disk.

**`prompt_compile.py` exits 1**
The linter found something. Read the findings: provider syntax, quality spam, abstract
emotion, unversioned reference, multi-action `primary_action`, or duplicate blocks.

**`continuity_check.py` reports references missing from the ledger**
Either the id is spelled differently or the asset is genuinely absent from the bibles. Add
it to the ledger before generating; do not "fix" it by removing the reference.

**`shot_budget.py` exits 1**
Duration drift exceeds 10%. Re-plan rather than stretching clips in the edit.

**`new_project.py` says "kept N existing file(s)"**
Files already exist. Use `--force` to overwrite, or work with what is there.

## Production

**Faces change between shots (`IDENTITY`)**
The identity anchor is weak or the reference sheet is not representative. Restate the canon
id, strengthen the reference set, re-keyframe. Do not rewrite the story to fix a face.

**Costume or damage changes mid-scene (`STATE`)**
A state change was never recorded as an event. Add it to `object_state` and restate the
costume version in the affected shots.

**The light direction flips between cuts (`LIGHTING`)**
The scene has a lighting plan but no continuity rule. Fix the direction per scene and restate
`lighting.direction` in every shot of it.

**The location looks like a different place after a cut (`GEOGRAPHY`)**
No axis, landmarks, or key light were specified. Re-keyframe against the location bible's
plan view.

**Motion is frozen or the clip is a slideshow (`MOTION`)**
`primary_action` describes a state, not an action. Rewrite it as an observable event with a
defined `end_state`.

**Camera does something random (`CAMERA`)**
Two movements were implied, or the movement was unmotivated. One move, with a reason.

**Anatomy breaks in fast motion (`ANATOMY`)**
Too much simultaneous action. Split into preparation → impact → reaction.

**Text or signage is garbled (`TEXT`)**
Do not generate text. Remove it, add it in the edit as a graphic.

**Effects swallow the character (`STYLE` / `ANATOMY`)**
Too many effect layers or an over-long style block. Shorten style, isolate effects into
their own layer and regenerate that layer alone.

**`end_state` of a shot conflicts with `start_state` of the next**
The beat sheet was edited without re-deriving the chain. Recompute states from the beat
sheet, then re-keyframe the affected shots.

**Budget burned with no usable shots**
The hero shot was attempted first. Reorder: cheap representative shot → lock style and
identity → bulk low-risk → hero shots last.

**Three failures, same class, no progress**
Change the layer: keyframe → method → model → shot redesign. More prompt wording will not help.

## Process

**The agent jumped straight to prompts**
The routing block was skipped. Ask for state detection first: "what state is this project in,
and what is the next gate?"

**Artifacts contradict each other**
Two writers or two sources of truth. Pick one authority per artifact (see
[`multi-agent.md`](multi-agent.md)) and re-derive the rest.

**A project validates but still feels wrong**
Schemas check shape, not judgement. Apply the delivery rubric in
[`../references/evaluation.md`](../references/evaluation.md) and repair the weakest
dimensions.

**Nothing seems to improve over time**
Nothing is being measured. Start with `runs.jsonl`, then `../evals/rubrics/`, then
`python scripts/run_evals.py` after each change to the skill.

## Getting unstuck

```bash
python scripts/lint_skill.py                     # package integrity
python scripts/validate.py project-dir --strict  # every warning becomes an error
python scripts/continuity_check.py project-dir
python scripts/prompt_compile.py shots.json --lint
python scripts/run_evals.py                      # is the skill itself healthy?
```
