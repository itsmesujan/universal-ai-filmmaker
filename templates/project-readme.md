# {{title}}

Project id: `{{project_id}}` · Format: {{format}} · Target: {{duration}} s · Aspect: {{aspect_ratio}}

Generated from the Universal AI Filmmaker templates. The shot skeletons in `shots.json`
are placeholders: fill `story_purpose`, `subject`, `primary_action`, `camera`, and
`continuity` before generating anything.

## State

| State | Artifact | Gate |
|---|---|---|
| IDEA | this scaffold | premise accepted |
| STORY | `story.md` | logline, theme, ending |
| SCRIPT | `script.md` | every scene has purpose, turn, location |
| BIBLES | `characters.md`, `locations.md`, `style.md` | every used asset has a canon id |
| BEATS | `beats.json` | story function + visual idea per beat |
| SHOTS | `shots.json` | purpose, one action, one camera move, duration |
| STORYBOARD | `storyboard.md` | framing, axis, staging readable |
| KEYFRAMES | keyframe images | style and identity representative |
| VIDEO | clips + `runs.jsonl` | QC rubric passed |
| AUDIO | `audio-plan.md` | layers mapped per shot |
| EDIT | `edit-plan.md` | cut list with transitions |
| QC | `qc-report.json` | all shots scored and classified |
| FINAL | locked deliverables | continuity clean, provenance complete |

Planned budget: {{scene_count}} scenes, {{shot_count}} shots.

## Commands

```bash
python scripts/validate.py .
python scripts/continuity_check.py shots.json continuity.json
python scripts/prompt_compile.py shots.json --shot shot-001
python scripts/prompt_compile.py shots.json --lint
```

## Rules that matter most

1. One action, one camera move, one environmental motion per shot.
2. Canon ids are versioned (`character:name:v1`); never edit a version in place.
3. Compile prompts from `shots.json`; never write freehand prose per shot.
4. Verify model capabilities before claiming them; record `unknown` otherwise.
5. Score every clip and record the verdict and repair in `qc-report.json`.
6. Append every attempt to `runs.jsonl` (model, seed, prompt hash, references, result).
