# Audio and Edit

Audio and edit are planned separately from video generation, then joined. Weak audio
undoes strong images.

## Audio architecture

| Layer | Content | Notes |
|---|---|---|
| dialogue | lines, performance, off-screen lines (O.S.) | plan timing per shot; avoid sync risk when unverified |
| voice-over | narration, internal monologue | record separately, cut to picture later |
| foley | footsteps, cloth, props, body movement | the layer that makes images feel real |
| hard effects | doors, impacts, weapons, vehicles | sync to impact frames |
| ambience | room tone, weather, city bed | continuous per location, never absent |
| music | score, stings, themes | follow dramatic beats, not just mood |
| silence | deliberate removal of layers | the most underused tool in AI film |

Rules:

- Every location gets an identifiable ambience bed.
- Never let music start or stop mid-shot without a dramatic reason.
- Silence before an impact increases its weight.
- Dialogue is written to fit `duration_target`: ~2.5 words/second including pauses.
- If lip-sync is unverified for the model, keep mouths off-screen, in profile, obstructed,
  or plan ADR-style dubbing with reaction shots covering the delivery.

## Dialogue and sync plan

Per dialogue shot record: speaker, exact line, start offset within the clip, intended
reaction shot, and the fallback if sync fails (cutaway, back-of-head, or wide).

When generating dialogue audio separately, keep a `lines.json` mapping
`shot_id → {speaker, text, start_ms, duration_ms}`. This is what the edit uses to sync.

## Mixing targets (relative)

| Layer | Typical level |
|---|---|
| dialogue | loudest, intelligible |
| hard effects | near dialogue |
| music | beneath dialogue and effects under speech |
| ambience | lowest, continuous |
| foley | above ambience, below dialogue |

Deliver at consistent loudness with true-peak headroom. Do not clip; fix level in the mix.

## Edit grammar

- Default to cuts. Cuts are invisible when action, eyeline, or direction matches.
- Use `hard_cut_on_action`, `match_cut`, `smash_cut` for energy; `dissolve`/`fade` only
  when time or consciousness changes; `l_cut`/`j_cut` to smooth dialogue scenes.
- Respect `start_state`/`end_state`: if a shot's exit state contradicts the next shot's
  entry state, the cut will read as a jump.
- Keep shot lengths varied: uniform durations feel mechanical.
- Trim to the emotional beat, not to the generated clip length. Shorter is usually better.

## Edit plan artifact

`edit-plan.md` should list: cut order, shot_id, in/out points, duration, transition in,
transition out, audio cue, and music beat alignment where relevant.

## Structure of a sequence

1. establish (orientation)
2. develop (pressure builds)
3. turn (reversal or reveal)
4. resolve/exit (pull to next sequence)

Sound and cut rhythm should tighten as the sequence approaches its turn.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Cuts feel jarring | state mismatch, no axis match | align end_state→start_state, insert cutaway |
| Scene feels flat | no sound design, no silence | add foley, ambience, deliberate silence |
| Music fights dialogue | levels unmanaged | duck music under speech |
| Dialogue looks dubbed | unverified lip-sync | cover with reaction/cutaway, ADR plan |
| Runtime drifts | clips stretched to target | fix the shot budget, cut to beats |
