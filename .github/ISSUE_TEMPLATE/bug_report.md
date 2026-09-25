---
name: Bug report
about: Report an issue with the skill, its schemas, its tooling, or its documentation
title: "[Bug] "
labels: bug
---

## Description

What is wrong, and where (file, reference, script, or schema)?

## Reproduction

Exact commands and inputs. For tooling, paste the full output.

```bash
python scripts/validate.py project-dir
```

## Expected behavior

## Actual behavior

## Environment

- Skill version (from `SKILL.md` front matter):
- Python version (`python --version`), if tooling is involved:
- Host/agent used:
- Project format (trailer, narrative short, anime episode, …):

## Relevant files

Paste the smallest artifact that reproduces it. Do not paste credentials or licensed media.

## Checks already run

- [ ] `python scripts/lint_skill.py`
- [ ] `python scripts/manifest.py --check`
- [ ] `python scripts/validate.py <path>`
- [ ] `python scripts/run_evals.py`

\n
