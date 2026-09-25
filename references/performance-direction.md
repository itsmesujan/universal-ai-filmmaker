# Performance Direction

Generators render what is visible. Direct behaviour, not feelings.

## The emotion ladder

Per beat, plan four moments:

1. **neutralise** — the uncommitted starting face/body
2. **build** — micro-signals of the impulse (brow, breath, grip, weight shift)
3. **peak** — the readable emotional event
4. **release** — the residue the next shot inherits (`end_state`)

If the shot only shows "peak", transitions look fake and continuity breaks.

## Playable verbs

Convert internal states into observable behaviour:

| Instead of | Direct |
|---|---|
| she is sad | she keeps her eyes down, jaw tight, breath shallow; she does not lift the cup |
| he is angry | he holds still, knuckles pale on the rail, then turns away |
| she is nervous | she checks the door twice, adjusts her sleeve, swallows |
| he is relieved | his shoulders drop, he exhales, he lets his hand fall |

Every `primary_action` should be a verb phrase with a body. Avoid "feels", "seems",
"looks like".

## Micro-expression and timing

- Anticipation before action, hold at the peak, follow-through after.
- Eyes lead head; head leads body. Direct eyeline before the turn.
- Breath is the cheapest performance cue: it is visible and consistent.
- Restraint reads better than exaggeration on close-ups; exaggeration suits wide
  shots, animation, and stylised modes.

## Eyelines and spatial performance

- Record who looks at whom and at what height (standing/sitting).
- Keep eyeline direction consistent with the 180° line (`continuity.md`).
- Off-screen looks must have a plausible off-screen target; define it in the scene.

## Performance continuity

Carry across shots:

- emotional state at shot start (`start_state`) matches previous `end_state`
- posture, breath rate, and hand positions
- props being held and their grip
- costume state (wet, torn, bloodied) and dirt level
- voice energy and speech rate for dialogue

## Dialogue performance

- Plan reaction shots before line delivery shots; reactions carry the scene.
- Note who is listening, not only who is speaking.
- Keep mouth movement simple when lip-sync is unverified: prefer profile, wide, or
  off-screen delivery, and place lines in the audio plan.
- Match speech duration to `duration_target`; 2.5 spoken words per second is a serviceable estimate.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Emotion unreadable | abstract direction | rewrite with playable verbs |
| Uncanny transitions | only peaks animated | add build and release, restate start_state |
| Puppet feel | no breath or weight | add breath, weight shift, anticipation |
| Incoherent reverse angles | eyeline unplanned | define off-screen targets, keep 180° |
| Sync mismatch | line longer than shot | shorten line or extend duration_target |
