# Model Adapter Protocol

A model adapter is a translation layer, not the filmmaking brain.

## Adapter metadata

provider
model
model_type
verified_at
text_to_video
image_to_video
reference_images
first_frame
last_frame
multi_keyframe
duration_options
aspect_ratios
resolutions
camera_controls
seed
negative_prompt
audio
dialogue
batching
known_limits
known_failure_modes

## Translation

SHOT_SPEC → capability map → provider syntax.

Unsupported fields are omitted or converted into descriptive prompt text only when appropriate.

Never claim a feature is supported without verification.

## Versioning

Keep provider/model adapters replaceable. The same SHOT_SPEC should be exportable to multiple models.
