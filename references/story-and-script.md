# Story and Screenplay

Film quality is decided here. A weak story cannot be repaired in the prompt layer.

## Story record (minimum viable)

- logline (one sentence: character + desire + obstacle + stakes)
- theme as a question, not a slogan
- protagonist: want (external), need (internal), flaw, cost of failure
- antagonist/opposing force: pressure that escalates
- world rule that generates conflict
- ending: what changes, and what is proven by the change
- format and runtime target

## Structure that survives short runtimes

- **Short (< 3 min):** one turn. Open in motion, one obstacle, one reversal, resolve.
- **5–10 min:** 3 acts, or 8 sequences. Act 1 ends with commitment, act 2 with
  collapse, act 3 with earned choice.
- **Trailer:** hook (0–10s) → escalation → montage → title/button. Narrative logic is
  secondary to rhythm, but continuity within the montage still holds.
- **Music video:** lyrical/emotional logic, recurring visual motif, chorus escalation.
- **Documentary:** claim → evidence → complication → synthesis, with a through-line subject.
- **Commercial:** problem → product as resolution → single memorable visual idea.

## Scene construction

Every scene needs: a want, an obstacle, a turn, and an exit condition. If a scene has
no turn, cut it or merge it.

Write the scene record (see `workflow.md`) before writing shot lists. Scenes exist to
change something; shots exist to reveal that change.

## Screenplay conventions

- Keep a draft in plain text with slug lines: `INT/EXT. LOCATION - TIME`.
- Action lines: present tense, observable behaviour only, no internal states.
- One idea per paragraph. Direct the camera only when it is dramatically required.
- Dialogue: characters speak to get something, not to explain the plot.
  Cut the last line of most speeches. Subtext over exposition.
- Mark (V.O.), (O.S.), and (CONT'D) consistently so the audio plan can parse them.
- Flag every practical requirement: vehicles, crowds, animals, child actors, water,
  fire, and any element known to break generation. These drive `risk_level`.

## Adapting a screenplay for generation

1. Convert each scene into beats (`beat_id`), tagging the story function and the turn.
2. Choose the *emotionally sufficient* number of shots, not the largest number.
3. Prefer one clear visual idea per beat. Merge beats when shots would be redundant.
4. Convert dialogue-heavy scenes into reaction-driven coverage when audio sync is
   unverified; keep the dialogue in the audio plan, not in the shot text.
5. Compress anything that requires precise choreography into preparation/reaction
   shots instead of one continuous complex action.

## Failure modes and fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| Scenes feel flat | no turn, no pressure | rewrite the scene, do not add shots |
| Story unclear in cuts | theme never visualised | define a visual thesis per scene |
| Endless coverage | shots not tied to beats | cut shots without a story function |
| Emotional whiplash | missing emotional_start/end | re-plan the emotional arc in the beat sheet |
| Confusing geography | screen direction unplanned | fix blocking before generating |
