# Continuity

Continuity is the difference between "forty clips" and "a film". It is tracked in a ledger,
enforced by versioned canon ids, and checked by a script.

## Canon ids

```text
character:hana:v1     location:platform-4:v1     prop:red-umbrella:v1     style:main:v1
```

Rules: lowercase, hyphenated, always versioned. A deliberate change creates a new version;
`v1` is never edited in place once shots reference it.

## The ledger

`continuity.json` (schema: `../schemas/continuity.schema.json`) holds:

| Section | Tracks |
|---|---|
| `characters[]` | appearance, costume version, accessories, voice, movement style, per-scene state |
| `locations[]` | layout reference, landmarks, entrances/exits, light direction |
| `props[]` | owner, condition, position history per shot |
| `time_and_weather[]` | per scene: time, weather, light source and direction |
| `screen_geometry[]` | per scene: axis, screen-left/right, travel directions |
| `object_state[]` | per scene per subject: costume, damage, dirt, wetness, held items |
| `emotional_state[]` | per shot: start and end state (must chain) |
| `violations[]` | logged drift with a decision |

## Three classes of continuity failure

| Class | Question | Typical example |
|---|---|---|
| **Identity** | is it the same character? | face morphs, hair length changes |
| **State** | is it the same moment? | clean shirt after a fight, umbrella reappears |
| **Geography** | is it the same space? | door flips sides, key light flips direction |

Classify first: the class tells you which layer to fix.

## Automatic drift detection

```bash
python scripts/continuity_check.py examples/mini-project
python scripts/continuity_check.py shots.json continuity.json --write --strict
```

It reports:

- references that are not versioned canon ids
- references missing from the ledger
- costume version changes inside one scene (`STATE`)
- key-light direction changes inside one scene (`LIGHTING`)
- screen-direction flips between consecutive shots of a scene (`GEOGRAPHY`)
- emotional-state jumps between consecutive ledger entries (`EMOTIONAL`)
- unresolved violations carried in the ledger

`--write` appends findings to `violations[]`, deduplicated; `--strict` exits non-zero.

## Screen geography rules

1. Lock the axis (180° line) per scene; state who is screen-left and screen-right.
2. Preserve travel direction: a subject moving screen-right keeps moving screen-right.
3. Change the camera side of the action only via a neutral shot (insert, cutaway, or a
   deliberate crossing on a move).
4. Define eyeline targets and match angle/height between reverse angles.

## State changes are events

Anything that changes — wet hair, torn sleeve, blood, a dropped prop — happens at a shot.
Record where, so later shots inherit it. Damage that appears and disappears is the most
common continuity tell after face drift.

## Repair order

Fix the smallest layer that explains the failure:

1. reference asset → 2. keyframe → 3. shot design → 4. adapter/prompt → 5. model/provider

Never rebuild the project to repair a face, and never re-litigate the story to fix a costume.

## Verified example

```bash
$ python scripts/continuity_check.py examples/mini-project
continuity check: 4 shot(s) against examples\mini-project\continuity.json

no drift detected
```

The example is clean because one costume version, one hair version, one prop-state chain,
one key-light direction, and one axis are reused across all four shots.

See also: [`../references/continuity.md`](../references/continuity.md),
[`../references/lighting-color.md`](../references/lighting-color.md),
[`../references/bibles.md`](../references/bibles.md).
