# Formats

Pick the format before the story: it sets structure, pacing, aspect, audio emphasis,
and the artifact set you owe the user.

| Format | Duration | Structure | Aspect | Shot range | Audio emphasis |
|---|---|---|---|---|---|
| Narrative short | 3–15 min | 3 acts / 8 sequences | 16:9, 2.39:1 | 30–120 | dialogue + score |
| Anime episode | 8–24 min | cold open + A/B plot + cliffhanger | 16:9 | 150–400 | dialogue, effects, OP/ED |
| Feature-length plan | 60–120 min | full 3-act | 2.39:1 | 600+ | full mix |
| Trailer | 30–150 s | hook → escalation → montage → button | 2.39:1 / 16:9 | 20–60 | rhythmic score, hard cuts |
| Teaser | 15–45 s | one image, one idea | any | 3–10 | sound design, sting |
| Music video | song length | verse/chorus escalation, motif | 16:9 / 9:16 | 40–150 | music-led, sync to beat |
| Documentary | 5–90 min | claim → evidence → complication → synthesis | 16:9 | interview + B-roll | voice-over, nat sound |
| Commercial | 15–60 s | problem → product resolution | 16:9 / 9:16 / 1:1 | 6–20 | music + VO + product SFX |
| Explainer | 60–180 s | question → mechanism → takeaway | 16:9 | 20–60 | VO-led |
| Vertical short | 15–60 s | hook in 2 s, one idea, loop | 9:16 | 5–15 | captions, loud hooks |
| Series pilot | 20–40 min | world + arc + hook | 16:9 | 200+ | full mix |

## Format-specific rules

- **Trailer:** rhythm is content. Cut on music accents, place the title card deliberately,
  and keep shot durations decaying toward the end. Continuity must hold inside each
  montage block even when chronology does not.
- **Music video:** define the beat map first (`beat_id` aligned to musical bars), then
  assign shots. Prioritise strong silhouettes, motif repetition, and performance inserts.
- **Documentary:** plan interview coverage as fixed setups (A/B cameras, interview
  eyeline to an off-camera interviewer) so B-roll and archive stay consistent. Log
  source/rights for every asset.
- **Commercial:** one product idea, one emotive idea. Product shots usually need
  controlled lighting and inserts; plan them as hero shots with extra attempts.
- **Vertical:** assume sound-off first; text/caption plan required, and shot sizes
  must be tighter (faces occupy more of the frame at 9:16).
- **Anime episode:** plan OP/ED, eye-catches, and next-episode previews separately so
  they never contaminate the narrative shot list.

## Deliverable sets by format

| Format | Minimum artifacts |
|---|---|
| Any | `project.json`, `script.md`, bibles, `beats.json`, `shots.json`, `continuity.json`, `qc-report.md` |
| Narrative | + `storyboard.md`, `image-prompts.md`, `video-prompts.md`, `audio-plan.md`, `edit-plan.md` |
| Trailer/commercial | + title card spec, music beat map, caption plan |
| Documentary | + interview plan, archive/rights log, nat-sound plan |
| Series | + episode bible, per-episode shot lists, continuity across episodes |

## Choosing mode per shot set

A single project may mix modes (e.g. photoreal framing with stylised inserts), but the
mix must be declared in the style bible with an explicit rule such as: "live-action
grammar for all human coverage; stylised mode only for flashbacks, marked in `style.mode`."
