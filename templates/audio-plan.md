# Audio Plan — {{title}}

## Layers

| Layer | Content | Notes |
|---|---|---|
| dialogue | | speaker, line, start offset, fallback if sync fails |
| voice-over | | |
| foley | | |
| hard effects | | sync to impact frames |
| ambience | | one identifiable bed per location |
| music | | follow beats, not mood |
| silence | | where and why |

## Lines

| shot_id | speaker | text | start_ms | duration_ms | fallback |
|---|---|---|---|---|---|
| | | | | | |

## Ambience per location

| location_id | bed | continuity notes |
|---|---|---|
| | | |

## Music map

| beat_id | cue | intent |
|---|---|---|
| | | |

## Mix targets

Dialogue loudest and intelligible; hard effects near dialogue; music ducked under speech;
ambience continuous and lowest; foley above ambience, below dialogue. Leave true-peak headroom.

## Sync risk

State whether lip-sync is verified for the chosen model. If not, list the coverage used
instead (profile, wide, obstructed mouth, reaction cutaway, ADR dubbing).
