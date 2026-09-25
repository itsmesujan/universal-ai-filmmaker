# Model Adapters

An adapter is a **translation layer with a verification date**, not the filmmaking brain.
It maps a canonical `SHOT_SPEC` onto one generator's inputs and records what that generator
cannot do.

## Anatomy

```json
{
  "adapter_version": "1.1.0",
  "provider": "provider-name",
  "model": "model-name",
  "model_type": "video",
  "verified_at": "2026-09-26",
  "docs_url": "https://…",
  "capabilities": { "image_to_video": true, "camera_controls": "unknown" },
  "limits": { "duration": [4, 6, 8], "aspect_ratios": ["16:9", "9:16"] },
  "failure_modes": ["face drift on fast turns"],
  "translation_notes": ["movement is expressed as prose, not parameters"],
  "degraded_mode": ["no last_frame control: chain via extracted final frame"]
}
```

Start from `../model-adapters/adapter-template.json`; validate with
`../scripts/validate.py`.

## Capability tiers

| Tier | Meaning | Consequence |
|---|---|---|
| verified | documented or probed, dated | may drive `SHOT_SPEC` fields |
| `"unknown"` | not confirmed | must be avoided or declared as a risk |
| unsupported | confirmed absent | adapter degrades, never pretends |

**Rule:** no capability may be `true` without a verification date. The validator raises an
error for a claimed capability on a placeholder date, and warns on placeholder snapshots.

## Verification procedure

1. Read the provider's current docs; note today's date.
2. Confirm input modes, duration/aspect/resolution limits, reference and keyframe support,
   camera controls, seed, negative prompt, audio, batching.
3. Probe one minimal call per capability if tooling is available.
4. Record results, limits, and failure modes.
5. Re-verify when the provider updates or when the date is older than ~90 days.

## Translation

```text
SHOT_SPEC → capability map → provider syntax
```

- Map neutral tokens from `../references/shot-grammar.md` to provider syntax when documented.
- Omit unsupported fields; convert to prose only when the prose is honest.
- Never emit a provider parameter the provider does not accept.
- Keep the mapping auditable: record the tokens used and the export they produced.

## Degraded mode — worked example

A model with no last-frame control and a 5 s cap:

```text
"degraded_mode": [
  "no last_frame: extract the final frame and use it as the next shot's first frame",
  "max 5s: split an 8s reaction into 5s + 3s with matched references and an insert cutaway",
  "no camera_controls: express movement as prose and accept lower fidelity"
]
```

Degraded mode is a first-class part of the plan. Hiding a missing capability behind
optimistic prose is how a production fails late and expensively.

## Multi-model productions

Different shots may use different models. Track:

```text
shot → model → adapter version → result → verdict
```

while keeping one story, one set of bibles, one ledger, and one `SHOT_SPEC` list. There is
no permanent "best model": choose per shot requirement and verified capability, and record
the choice in the run log.

## Lifecycle

1. Create from the template.
2. Verify and date.
3. Use only for the stage it supports (image vs video vs audio).
4. Re-verify on provider change.
5. Keep old snapshots: shots generated under an older adapter must remain attributable.
   Never retro-attribute an old shot to a new model.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Export uses unsupported parameters | capability guessed | set `"unknown"`, degrade instead |
| Quality dropped after an update | stale adapter | re-verify, bump `verified_at` |
| Two shots behave differently | adapter versions unrecorded | log `adapter_version` per attempt |
| Plan impossible on the chosen model | tier ignored | re-plan shots for the verified tier |

See also: [`../references/model-adaptation.md`](../references/model-adaptation.md),
[`reproducibility.md`](reproducibility.md).
