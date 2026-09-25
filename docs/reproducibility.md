# Reproducibility

A great shot you cannot reproduce is luck. Reproducibility is a small amount of logging
discipline applied consistently.

## The run log

Append one JSON object per attempt to `runs.jsonl` (never rewrite history):

```json
{"shot_id":"shot-003","attempt":2,"model":"provider/model-version",
 "adapter_version":"1.1.0","adapter_verified_at":"2026-09-20",
 "prompt_hash":"sha256:…","prompt_version":1,"seed":123456,
 "references":["character:hana:v1","keyframe:shot-003:a1"],
 "generation_method":"image_to_video","duration_s":12,
 "result_path":"renders/shot-003-a2.mp4",
 "qc":{"status":"REPAIR","failure_class":"IDENTITY","score":3.4},
 "notes":"face drifted on the turn; added identity anchor"}
```

## Determinism ladder

Lock from the top down; a missing rung means quality differences cannot be attributed, so
"improvement" becomes guesswork.

1. **seed lock** — reuse the seed when re-rolling the same shot
2. **keyframe lock** — reuse the approved first frame for every retry
3. **reference lock** — same character/location reference set
4. **prompt lock** — record the compiled prompt hash; edits create a new `prompt_version`
5. **model lock** — provider + model + version, with `verified_at`

## Provenance for accepted assets

Every accepted clip must be answerable: what produced it, what it is, where it lives, what
canon it satisfies. A clip whose provenance is unknown is a placeholder — regenerate it or
mark it as such.

## Change control

| Change | Action |
|---|---|
| bible edit | bump the version, list affected shots |
| prompt edit | bump `prompt_version`, keep the previous run log |
| adapter/model change | create a new snapshot; never retro-attribute old shots |
| shot redesign | new spec, new log lines; old attempts remain for the record |

## Recreating an old shot

1. Find the run-log line.
2. Restore the same references and seed.
3. Recompile the prompt at the recorded `prompt_version`.
4. Compare with the archived result. If the model changed, record the differences in the
   adapter's `known_limits` instead of pretending they did not happen.

## Verifying a project is reproducible

```bash
python scripts/validate.py project-dir
python scripts/continuity_check.py shots.json continuity.json
python scripts/prompt_compile.py shots.json --json | head -40   # same spec → same prompt
```

If two compiles of the same spec differ, something is being edited outside the spec — find
it and move it into the spec.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Cannot recreate a shot | no run log | start appending to `runs.jsonl` today |
| Improvement unmeasurable | seed/model unrecorded | add seed + model locks |
| Silent creative drift | prompts edited in place | version prompts, keep history |
| Accepted clip of unknown origin | asset not logged | regenerate or mark as placeholder |

See also: [`../references/reproducibility.md`](../references/reproducibility.md),
[`../references/risk-cost.md`](../references/risk-cost.md).
