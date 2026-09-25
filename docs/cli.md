# CLI Reference

All tools are Python 3.9+, standard library only, and run from the repository root.

```bash
python scripts/<tool>.py [options]
```

| Tool | Purpose |
|---|---|
| `../scripts/new_project.py` | scaffold a project from the templates |
| `../scripts/shot_budget.py` | plan scenes/shots that sum to the runtime |
| `../scripts/validate.py` | schema + semantic validation |
| `../scripts/prompt_compile.py` | compile and lint prompts from `shots.json` |
| `../scripts/continuity_check.py` | detect continuity drift |
| `../scripts/manifest.py` | regenerate `MANIFEST.json` |
| `../scripts/lint_skill.py` | package integrity checks |
| `../scripts/run_evals.py` | run the machine evals |

## new_project.py

```bash
python scripts/new_project.py projects/rain-platform \
    --title "Rain Platform" --duration 90 --format narrative_short --pacing normal
```

Creates the full artifact set (manifest, story, script, bibles, ledger, beats, shot
skeletons, storyboard, audio plan, edit plan, QC report, run log, README), then prints the
routing block and the next gate. `--force` overwrites; `--format trailer` switches profile.

## shot_budget.py

```bash
python scripts/shot_budget.py --duration 360
python scripts/shot_budget.py --duration 60 --format commercial --pacing brisk --json
python scripts/shot_budget.py --duration 480 --out plan.json
```

Deterministic: identical arguments always produce an identical plan. Exit code is non-zero
if drift exceeds 10%. Formats: narrative_short, anime_episode, feature, trailer, teaser,
music_video, documentary, commercial, explainer, vertical_short, series_pilot.

## validate.py

```bash
python scripts/validate.py examples/mini-project
python scripts/validate.py shots.json --json
python scripts/validate.py project-dir --strict      # warnings become errors
```

Directories are walked recursively; `*.schema.json` and `*template*` files are skipped.
Beyond schema checks it reports: duplicate ids, unknown scene references, duration drift
> 10%, missing `camera.type`, empty continuity blocks, over-long shots, `risk_level` vs the
risk axes, attempt budgets inconsistent with risk, beats with no mapped shots, QC `PASS`
below threshold, unresolved shots under a final `PASS`, and placeholder adapters.

## prompt_compile.py

```bash
python scripts/prompt_compile.py shots.json --shot shot-003
python scripts/prompt_compile.py shots.json --format video
python scripts/prompt_compile.py shots.json --lint
python scripts/prompt_compile.py shots.json --write video-prompts/ --risk
python scripts/prompt_compile.py shots.json --json
```

Exit code is non-zero when the linter reports findings, so it can gate CI.

## continuity_check.py

```bash
python scripts/continuity_check.py examples/mini-project
python scripts/continuity_check.py shots.json continuity.json --write --strict
python scripts/continuity_check.py . --json
```

Detects unversioned references, references missing from the ledger, costume drift, light
direction drift, axis flips, emotional jumps, and unresolved ledger violations.
`--write` appends deduplicated findings to `violations[]`.

## manifest.py

```bash
python scripts/manifest.py           # rewrite MANIFEST.json
python scripts/manifest.py --check   # verify freshness (exit 1 when stale)
```

`MANIFEST.json` deliberately does not list itself: a file cannot contain its own hash
without a fixed-point iteration, and a stale self-hash is worse than none.

Hashes cover **LF-normalised bytes**, and `.gitattributes` enforces `eol=lf`, so the
manifest gives the same answer on a Windows (CRLF) and a Linux (LF) checkout.

## lint_skill.py

```bash
python scripts/lint_skill.py
python scripts/lint_skill.py --json
```

Checks required files and directories, `SKILL.md` front matter (name, description ≤ 1024
chars, version), backticked repo path references, markdown links, `docs/README.md` coverage,
JSON validity, `MANIFEST.json` freshness, and stray TODO/FIXME markers in references.

## run_evals.py

```bash
python scripts/run_evals.py
python scripts/run_evals.py --only continuity
python scripts/run_evals.py --json
```

See [`evals.md`](evals.md).

## Recommended CI sequence

```bash
python scripts/lint_skill.py
python scripts/manifest.py --check
python scripts/validate.py examples model-adapters
python scripts/run_evals.py
```

Each command exits non-zero on failure, so the sequence is a complete gate for a pull
request. The same steps run in `../.github/workflows/validate.yml`.
