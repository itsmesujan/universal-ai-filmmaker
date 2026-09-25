# Multi-Agent Production

If the host supports subagents or parallel workers, split the work by craft. If not, run the
same roles sequentially — the **artifacts** are the coordination mechanism, not the roles.

## Roles

| Role | Produces | Gate |
|---|---|---|
| SHOWRUNNER | routing decision, artifact plan | gate ownership, conflict resolution |
| STORY_EDITOR | logline, theme, structure, scene list | STORY |
| DIRECTOR | scene intent, performance direction, visual thesis | BEATS |
| CINEMATOGRAPHER | shot grammar, lighting/colour plan, lens choices | SHOTS |
| CHARACTER_DESIGNER | character bibles and references | BIBLES |
| PRODUCTION_DESIGNER | world/location bibles, props | BIBLES |
| STORYBOARD_ARTIST | storyboard frames, keyframe specs | KEYFRAMES |
| PROMPT_ENGINEER | compiled neutral prompts + lint report | pre-generation |
| MODEL_ADAPTER | provider exports, capability map, unknowns | pre-generation |
| AUDIO_DIRECTOR | dialogue, ambience, effects, music plan | AUDIO |
| EDITOR | assembly, timing, transitions | EDIT |
| CONTINUITY_SUPERVISOR | drift report | veto on canon violations |
| QC_AGENT | QC report, failure classes | ACCEPT |

## Rules that prevent merge chaos

1. **One writer per artifact.** Two roles editing `shots.json` guarantees lost work.
2. **Hand off artifacts, not summaries.** A paraphrase loses the field-level detail that
   continuity depends on.
3. **Never re-derive a decision another role owns.** Ask for it.
4. **Serialise canon.** Character/world/style bibles and the ledger are single-writer.
5. **Continuity has a veto** on any shot that violates the ledger.
6. **Showrunner arbitrates** genuine conflicts (e.g. a director wanting an unmotivated light
   flip that the cinematographer's plan forbids).

## Handoff format

```text
FROM: CINEMATOGRAPHER
TO:   PROMPT_ENGINEER
ARTIFACT: shots.json (scene-01..03)
DECISIONS: axis screen-left→right; key light screen-left; 35 mm normal for dialogue
OPEN: whether the model honours camera_controls tokens
BLOCKERS: none
```

## Parallelism

| Safe to parallelise | Must be serial |
|---|---|
| independent scenes | bible and ledger edits |
| per-shot prompt compilation | final edit assembly |
| per-scene audio | QC acceptance decisions |
| QC of distinct clips | continuity decisions across scenes |

Merge order: bibles → shots → compiled prompts → results → QC → edit.

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

Walk the pipeline in order from [`workflow.md`](workflow.md) and write each artifact to disk
before starting the next. You lose parallelism, not structure.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Contradictory shot specs | roles paraphrasing each other | pass artifacts only |
| Look drifts after a merge | two writers on style | single writer per artifact |
| Continuity breaks at merge | ledger written concurrently | serialise canon |
| Slow progress | canon work parallelised by mistake | parallelise scenes, serialise canon |

See also: [`../references/multi-agent.md`](../references/multi-agent.md).
