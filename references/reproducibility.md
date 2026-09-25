# Reproducibility and Run Logs

If a great shot cannot be reproduced or re-derived, it is luck, not method.

## Run log (one record per attempt)

```json
{
  "shot_id": "shot-004",
  "attempt": 2,
  "model": "provider/model-version",
  "adapter_version": "1.1.0",
  "adapter_verified_at": "2026-09-20",
  "prompt_hash": "sha256:...",
  "prompt_version": 2,
  "seed": 123456,
  "references": ["character:hana:v1", "keyframe:shot-004:a1"],
  "generation_method": "image_to_video",
  "duration_s": 6,
  "result_path": "renders/shot-004-a2.mp4",
  "qc": { "status": "REPAIR", "failure_class": "IDENTITY", "score": 3.4 },
  "cost_estimate": "1 generation credit",
  "notes": "face drifted on the turn; added identity anchor"
}
```

Store logs as `runs.jsonl` (one JSON object per line). Append-only, never rewritten.

## Determinism ladder

Lock in this order, top-down:

1. **seed lock** — same seed for re-rolls of the same shot
2. **keyframe lock** — approved first frame reused for every retry
3. **reference lock** — same character/location reference set
4. **prompt lock** — compiled prompt hash recorded; edits create a new `prompt_version`
5. **model lock** — provider + model + version recorded (`verified_at`)

If any rung is missing, quality differences cannot be attributed, so improvement becomes
guesswork.

## What to record for outputs

For each accepted asset: what produced it (log line), what it is (`shot_id`, version),
where it lives (path), and what canon it satisfies. Never keep an accepted clip whose
provenance is unknown — re-generate or downgrade it to a placeholder.

## Change control

- Editing a bible bumps its version and lists affected shots.
- Editing a shot bumps `prompt_version`; the previous run log stays.
- Provider/model changes create a new adapter snapshot; existing shots are never
  retro-attributed to the new model.

## Reproducing an old shot

1. Read the run log line.
2. Restore the same references and seed.
3. Recompile the prompt at the recorded `prompt_version`.
4. Compare with the archived result. If the model changed, expect differences: record
   them in the adapter's `known_limits`.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Cannot recreate a shot | no run log | start appending `runs.jsonl` immediately |
| Improvement not measurable | seed/model unrecorded | add seed + model lock |
| Silent creative drift | prompts edited in place | version prompts, keep history |
| Accepted clip of unknown origin | asset not logged | re-generate or mark as placeholder |
