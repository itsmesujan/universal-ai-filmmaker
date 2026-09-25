# Action and Choreography

Complex continuous action is the highest-risk thing you can ask a video model to do.
Design action as coverage, not as one long take.

## The four-beat unit

`PREPARATION → ACTION/IMPACT → REACTION → CONSEQUENCE`

Expand into shots when the action matters:

| # | Shot | Purpose | Typical grammar |
|---|---|---|---|
| 1 | readiness | establish positions, intent, stakes | wide or medium_full, static |
| 2 | wind-up | anticipation, tension | close on hands/eyes, slow push |
| 3 | launch | committed movement | tracking or whip pan, short lens |
| 4 | impact | the collision itself | insert or extreme close, high shutter feel |
| 5 | reaction | who is affected and how | medium_close, handheld micro-shake |
| 6 | consequence | environment/state change | wide, static, dust settling |
| 7 | aftermath | emotional residue | close, held longer than comfortable |
| 8 | button | turn or next objective | any, ends on new information |

Rules: never put launch + impact + reaction in a single generated shot. Keep one
physical event per shot so failures stay local and cheap.

## Screen direction in action

- Lock the axis: attacker screen-left → defender screen-right for the whole sequence.
- Reversals require a neutral shot (impact insert, cutaway, or camera crossing on a move).
- Preserve the direction of travel (moving_left stays moving_left) across cuts.
- Record weapon/prop hand (left/right) and keep it stable through the sequence.

## Motion design

- Speed: normal, slow_motion, fast_motion, speed_ramp (ramp needs 2+ shots, not one).
- Effects: impact frames, speed lines, dust, debris, sparks, water spray, shockwave,
  cloth flutter, hair whip, smoke. Assign each effect to a specific shot.
- Add one environmental response to every impact (rain splashes, papers scatter, glass shakes).
- Physical plausibility beats spectacle: weight, follow-through, and recoil sell the hit.

## Anime and stylised action

- Use smear frames, hold frames, impact frames, and speed lines deliberately.
- Push exaggeration in poses and silhouettes; keep anatomy count correct.
- Separate effect layers from character layers in the plan so they can be regenerated alone.
- Match line weight and shading to the style lock; stylised action must not drift photoreal.

## Action continuity ledger

Track per shot: damage state, dirt/blood/wetness, prop position, where each character
stands, and how much has been destroyed. Consequence shots must inherit exactly that state.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Limbs melt during fast motion | too much action in one shot | split into preparation/impact/reaction |
| Gravity looks wrong | airborne complexity | ground the action, add weight and recoil |
| Direction flips mid-sequence | axis not locked | lock axis, insert neutral shot for reversals |
| Damage appears/disappears | no damage ledger | record damage per shot, restate in continuity |
| Impact has no weight | missing environment response | add debris/dust/splash to impact shot |
| Effects obliterate character | effect layer overload | isolate effects, reduce count per shot |
