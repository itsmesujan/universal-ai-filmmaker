# Provider-Neutral Prompting

A useful prompt describes observable requirements.

## Image prompt

SUBJECT
APPEARANCE / REFERENCES
POSE
COMPOSITION
ENVIRONMENT
LIGHTING
CAMERA
STYLE
MOOD
CONTINUITY ANCHORS
CONSTRAINTS

## Video prompt

SUBJECT MOTION
CAMERA MOTION
ENVIRONMENT MOTION
TIMING
PERFORMANCE
START STATE
END STATE
CONTINUITY
CONSTRAINTS

For image-to-video, do not redundantly restate details already locked by the reference image unless the target model benefits from it.

Avoid generic quality spam. Prefer concrete visual and temporal instructions.

## Negative constraints

Use only constraints that address a known risk. Do not create a huge generic negative prompt.
