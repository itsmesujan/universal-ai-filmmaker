# Getting Started

Ten minutes from an idea to a reviewable production plan.

## 1. Install

Agent Skills-compatible hosts: upload or install the directory containing
[`../SKILL.md`](../SKILL.md). Everything else (references, templates, schemas, scripts) is
loaded on demand.

Requirements: any host that can read Markdown files. Python 3.9+ is optional and only
needed for the deterministic tooling in `../scripts/`.

```bash
git clone https://github.com/itsmesujan/universal-ai-filmmaker.git
cd universal-ai-filmmaker
python scripts/run_evals.py        # sanity check, no dependencies
```

## 2. Ask for a film

You do not need to learn the vocabulary first. State the intent:

```text
Make a 90-second cinematic short about a girl who waits for a friend who never arrives
on a rain-soaked night platform. Quiet, melancholic, dialogue-free.
```

The skill will route the request, declare its assumptions, and stop at the first gate:

```text
CLASS:       NEW_FILM
STATE:       IDEA (no approved artifacts found)
ENTRY:       STORY → SCRIPT
MODE:        cinematic
ASSUMPTIONS: 90s runtime, 16:9, dialogue-free, no verified model
NEXT:        story.md, then approval before beats
```

Answer the three questions it may ask (what it is, how long and where it will be seen, what
must not change) — or say "you decide" and it will proceed with the stated defaults.

## 3. Or scaffold a project yourself

```bash
python scripts/new_project.py projects/rain-platform \
    --title "Rain Platform" --duration 90 --format narrative_short

python scripts/shot_budget.py --duration 90                    # scene/shot plan
python scripts/validate.py projects/rain-platform              # schema + semantic checks
python scripts/prompt_compile.py projects/rain-platform/shots.json --shot shot-001
```

The scaffold contains the full artifact set: project manifest, story, script, bibles,
ledger, beats, shot skeletons, storyboard, audio plan, edit plan, QC report, and run log.

## 4. Work the pipeline in order

| # | Gate | Artifact | You leave it when |
|---|---|---|---|
| 1 | STORY | story | logline, theme, and ending are accepted |
| 2 | SCRIPT | script | every scene has a purpose, turn, and location |
| 3 | BIBLES | characters, locations, style | every used asset has a canon id |
| 4 | BEATS | beats | each beat has a story function and a visual idea |
| 5 | SHOTS | shots | each shot has purpose, one action, one camera move, a duration |
| 6 | STORYBOARD | storyboard | framing, axis, and staging are readable |
| 7 | KEYFRAMES | keyframes | style and identity are representative on a cheap shot |
| 8 | VIDEO | clips + run log | every clip is scored, failures classified |
| 9 | AUDIO | audio plan | dialogue, ambience, effects, music, silence are mapped |
| 10 | EDIT | edit plan | the cut list has transitions and timing |
| 11 | QC | QC report | all shots scored; repairs recorded |
| 12 | FINAL | deliverables | continuity is clean and provenance is complete |

Do not jump to step 8 from an idea. Generation is the most expensive place to discover a
story or continuity problem.

## 5. Generate the first shot properly

1. Pick the **cheapest representative** shot (usually a static establish or a close-up).
2. Compile its prompts: `python scripts/prompt_compile.py shots.json --shot shot-001`.
3. Run the linter: `python scripts/prompt_compile.py shots.json --lint` (fix every finding).
4. Generate, then score with the QC scorecard in
   [`../references/qc.md`](../references/qc.md).
5. Fix the bibles — not the shot — if style or identity is wrong.
6. Only then bulk-generate the rest of the scene.

## 6. Example project

`../examples/mini-project/` is a complete four-shot scene (42 s) with a full continuity
ledger. Run the tooling against it to see what "good" looks like:

```bash
python scripts/validate.py examples/mini-project
python scripts/continuity_check.py examples/mini-project
python scripts/prompt_compile.py examples/mini-project/shots.json --shot shot-003
```

## 7. Where things go

```text
project/
├── project.json        manifest: format, duration, scenes, budget
├── story.md            logline, theme, arc, ending
├── script.md           screenplay
├── characters.md       character canon
├── locations.md        world canon
├── style.md            style bible + STYLE_LOCK
├── continuity.json     continuity ledger (canon, states, violations)
├── beats.json          dramatic beats mapped to shots
├── shots.json          canonical SHOT_SPEC records
├── storyboard.md       panels/spec per shot
├── image-prompts.md    compiled image prompts
├── video-prompts.md    compiled video prompts
├── audio-plan.md       dialogue, foley, effects, ambience, music
├── edit-plan.md        cut list, transitions, rhythm
├── qc-report.json      per-shot scores, failure classes, repairs
├── runs.jsonl          one line per generation attempt
└── evaluation.md       delivery rubric score and evidence
```

## Common first mistakes

| Mistake | Consequence | Instead |
|---|---|---|
| Asking for a 10-minute video as one prompt | unusable output, no control | plan scenes and 3–8 s shots |
| Writing prompts by hand per shot | drift, no reproducibility | compile from `SHOT_SPEC` |
| Skipping the continuity ledger | faces and costumes change every cut | write canon ids before generating |
| Generating the hero shot first | budget burned on an unproven look | lock style on a cheap shot first |
| Accepting clips without scoring | quality decays invisibly | score every clip, record the verdict |
