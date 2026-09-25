# Multi-Agent Production

If the host supports subagents or parallel workers, split by craft. If not, run the
same roles sequentially and produce the same artifacts.

## Role contracts

Every role has inputs, outputs, and a gate. One writer per artifact.

| Role | Inputs | Outputs | Gate |
|---|---|---|---|
| SHOWRUNNER | user intent, project state | routing decision, artifact plan | gate ownership |
| STORY_EDITOR | idea/script | logline, theme, structure, scene list | STORY |
| DIRECTOR | script, beats | scene intent, performance direction, visual thesis | BEATS |
| CINEMATOGRAPHER | beats, style bible | shot grammar, lighting/colour plan, lens choices | SHOTS |
| CHARACTER_DESIGNER | script | character bibles + references | BIBLES |
| PRODUCTION_DESIGNER | script | world/location bibles, props | BIBLES |
| STORYBOARD_ARTIST | shots | storyboard frames, keyframe specs | KEYFRAMES |
| PROMPT_ENGINEER | SHOT_SPEC | compiled neutral prompts + lint report | pre-generation |
| MODEL_ADAPTER | neutral prompts, capabilities | provider exports, capability map, unknowns | pre-generation |
| AUDIO_DIRECTOR | script, edit plan | dialogue, ambience, SFX, music plan | AUDIO |
| EDITOR | accepted clips, audio plan | assembly, timing, transitions | EDIT |
| CONTINUITY_SUPERVISOR | ledger vs clips | drift report | veto on acceptance |
| QC_AGENT | clips, rubric | QC report, failure classes | ACCEPT |

## Handoff protocol

Each handoff is a small, machine-readable artifact plus a one-paragraph rationale:

```text
FROM: CINEMATOGRAPHER
TO:   PROMPT_ENGINEER
ARTIFACT: shots.json (scene-01..03)
DECISIONS: axis screen-left→right; key light screen-left; 35 mm normal for dialogue
OPEN: whether model supports camera_controls tokens
BLOCKERS: none
```

Rules: pass artifacts, not paraphrase. Never re-derive a decision another role owns.
Conflicts escalate to SHOWRUNNER; CONTINUITY_SUPERVISOR holds veto on canon violations.

## Parallelism rules

- Safe to parallelise: independent scenes, per-shot prompt compilation, per-scene audio, QC of distinct clips.
- Never parallelise: bible edits, continuity ledger writes, final edit assembly.
- Merge order: bibles → shots → compiled prompts → results → QC → edit.

## Subagent prompt template

```text
ROLE: <role>
PROJECT: <project_id> v<schema_version>
READ: <exact files>
PRODUCE: <exact artifacts>
CONSTRAINTS: provider-neutral; do not invent capabilities; do not edit canon
DONE WHEN: <gate condition>
```

## Without subagents

Run roles in the pipeline order of `SKILL.md` and, after each role, emit its artifact to
disk before starting the next. The artifacts are the coordination mechanism; the roles
are only a way of thinking.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Two roles fight over the look | no artifact ownership | one writer per artifact |
| Contradictory shot specs | roles paraphrasing each other | pass artifacts, not summaries |
| Continuity breaks at merge | ledger not single-writer | serialise ledger writes |
| Slow progress | sequential work parallelised wrongly | parallelise scenes, serialise canon |
