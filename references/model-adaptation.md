# Model Adapter Protocol

A model adapter is a translation layer, not the filmmaking brain. It converts the
canonical `SHOT_SPEC` into a specific generator's inputs and records what that generator
could not do.

## Adapter metadata

```json
{
  "adapter_version": "1.1.0",
  "provider": "provider-name",
  "model": "model-name-or-id",
  "model_type": "video | image | audio",
  "verified_at": "YYYY-MM-DD",
  "docs_url": "https://...",
  "capabilities": {
    "text_to_video": "unknown",
    "image_to_video": "unknown",
    "reference_images": "unknown",
    "first_frame": "unknown",
    "last_frame": "unknown",
    "multi_keyframe": "unknown",
    "camera_controls": "unknown",
    "negative_prompt": "unknown",
    "seed": "unknown",
    "audio": "unknown",
    "dialogue": "unknown",
    "batching": "unknown"
  },
  "limits": {
    "duration": [],
    "aspect_ratios": [],
    "resolution": [],
    "max_reference_images": "unknown",
    "prompt_length": "unknown"
  },
  "failure_modes": [],
  "translation_notes": [],
  "degraded_mode": []
}
```

Rules: no capability may be `true` without verification on `verified_at`. When unverified,
use the literal string `"unknown"` — never guess, never inherit from a similar model.

## Verification procedure

1. Read the provider's current documentation; note the date.
2. Confirm: input modes, duration/aspect/resolution limits, reference/keyframe support,
   camera controls, seed, negative prompt, audio, batching.
3. Run one minimal probe per claimed capability if the tooling is available.
4. Record results in `capabilities`, `limits`, and `failure_modes`.
5. Set `verified_at`. Re-verify before reuse if the date is more than ~90 days old.

## Capability tiers

| Tier | Meaning | Consequence for the plan |
|---|---|---|
| verified | tested/documented | may be used to drive SHOT_SPEC fields |
| unknown | not confirmed | must be avoided or declared as a risk |
| unsupported | confirmed absent | adapter must degrade, not pretend |

## Translation

`SHOT_SPEC → capability map → provider syntax.`

- Map each neutral token (`shot-grammar.md`) to provider syntax when documented.
- Unsupported fields are **omitted**, or converted to descriptive prompt text only when
  that text is honest and likely to be honoured.
- Never emit a provider parameter that the provider does not accept.
- Preserve tokens in the export metadata so the mapping can be audited.

## Degraded mode

When a required capability is missing, write the fallback into `degraded_mode`, e.g.:

```text
"degraded_mode": [
  "no last_frame control: chain shots via extracted final frame instead",
  "no camera_controls: express movement as prose and accept lower fidelity",
  "duration max 5s: split 8s shots into two 4s shots with matched reference"
]
```

Degraded mode is a first-class part of the plan, not a failure.

## Adapter lifecycle

1. Create from `model-adapters/adapter-template.json`.
2. Verify and date it.
3. Use it only for the pipeline stage it supports (image vs video vs audio).
4. Re-verify when the provider updates, or when results stop matching the snapshot.
5. Keep old snapshots: shots generated with an older adapter version must still be
   attributable. Never rewrite history to fit a new model.

## Portability

The same `SHOT_SPEC` must be exportable to several models. Provider changes regenerate
the adapter/export, never the creative source of truth.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Export uses unsupported parameters | capability guessed | set `"unknown"`, degrade instead |
| Quality dropped after a provider update | stale adapter | re-verify, bump `verified_at` |
| Two shots behave differently | different adapter versions unrecorded | log `adapter_version` per attempt |
| Plan impossible on the chosen model | capability tier ignored | re-plan shots for the verified tier |
