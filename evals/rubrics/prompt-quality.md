# Rubric — Prompt Quality

Score each dimension 0–5 for a sample of compiled prompts (at least one per risk band).

| Dimension | 0 | 3 | 5 |
|---|---|---|---|
| Specificity | adjectives and superlatives | observable nouns and verbs | measurable, checkable description |
| Block discipline | blocks mixed or missing | required blocks present | consistent order, no duplicated or conflicting blocks |
| Action primacy | style dominates the opening | action present | action and motion lead, style constrains without swallowing the event |
| Continuity anchors | absent | costume/identity restated | exactly the anchors that can drift, nothing redundant |
| Constraint quality | generic negative spam | a few specific constraints | constraints traceable to a known risk or QC failure |
| Provenance | no version recorded | prompt saved | prompt hash, version, references, and adapter recorded |
| Linting | not run | warnings noted | zero lint findings, or each finding explicitly justified |

**Ship** at ≥ 28/35. A prompt that cannot be recompiled from `SHOT_SPEC` fails the rubric
regardless of how it reads: hand-written prompts cannot be maintained across 40 shots.

## Automatic checks

```bash
python scripts/prompt_compile.py shots.json --lint
```

Machine lint covers provider syntax, quality spam, abstract emotion, unversioned
references, and duplicate blocks. Everything else here requires judgement.
