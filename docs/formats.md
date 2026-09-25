# Formats

The format decides structure, pacing, aspect ratio, and what "done" means.

| Format | Runtime | Structure | Aspect | Shots | Audio emphasis |
|---|---|---|---|---|---|
| Narrative short | 3–15 min | 3 acts / 8 sequences | 16:9, 2.39:1 | 30–120 | dialogue + score |
| Anime episode | 8–24 min | cold open + A/B plot + hook | 16:9 | 150–400 | dialogue, effects |
| Feature plan | 60–120 min | full 3-act | 2.39:1 | 600+ | full mix |
| Trailer | 30–150 s | hook → escalation → montage → button | 2.39:1 / 16:9 | 20–60 | rhythmic score |
| Teaser | 15–45 s | one image, one idea | any | 3–10 | sting, design |
| Music video | song length | verse/chorus escalation | 16:9 / 9:16 | 40–150 | music-led |
| Documentary | 5–90 min | claim → evidence → complication → synthesis | 16:9 | interview + B-roll | voice-over, nat sound |
| Commercial | 15–60 s | problem → product resolution | 16:9 / 9:16 / 1:1 | 6–20 | music + VO |
| Explainer | 60–180 s | question → mechanism → takeaway | 16:9 | 20–60 | VO-led |
| Vertical short | 15–60 s | hook in 2 s, one idea, loop | 9:16 | 5–15 | captions, hooks |
| Series pilot | 20–40 min | world + arc + hook | 16:9 | 200+ | full mix |

## Planning a budget per format

```bash
python scripts/shot_budget.py --duration 90 --format trailer --pacing brisk
python scripts/shot_budget.py --duration 30 --format commercial
python scripts/shot_budget.py --duration 45 --format vertical_short
```

Shot counts and average shot length come from the format profile, so a trailer does not get
planned like a documentary.

## Format-specific rules

**Narrative short** — one turn minimum. If the structure has no reversal, it is a scene, not
a film.

**Trailer** — rhythm *is* the content. Cut on musical accents, decay shot lengths toward the
end, place the title card deliberately. Continuity must hold inside each montage block even
though chronology does not.

**Music video** — define the beat map first, then assign shots. Motif repetition beats
narrative logic; performance inserts are the connective tissue.

**Documentary** — plan fixed interview setups (A/B cameras, eyeline to an off-camera
interviewer) so B-roll stays consistent. Log source and rights for every asset.

**Commercial** — one product idea, one emotional idea. Product shots are hero shots: give
them extra attempts and controlled lighting.

**Vertical** — assume sound-off first; plan captions. Faces must fill more of the frame at
9:16, so tighten shot sizes.

**Anime episode** — plan OP/ED, eye-catches, and next-episode previews separately so they
never contaminate the narrative shot list.

## Deliverable sets

| Format | Minimum artifacts |
|---|---|
| Any | manifest, script, bibles, ledger, beats, shots, QC report |
| Narrative | + storyboard, image prompts, video prompts, audio plan, edit plan, run log |
| Trailer / commercial | + title card spec, music beat map, caption plan |
| Documentary | + interview plan, archive/rights log, nat-sound plan |
| Series | + episode bible, per-episode shot lists, cross-episode continuity |

## Mixing modes

A project may mix cinematic coverage with stylised inserts, but the rule must be declared in
the style bible (for example: "live-action grammar for all human coverage; stylised mode
only for flashbacks, marked in `style.mode`"). Random per-shot mixing reads as inconsistency,
not style.

See also: [`../references/formats.md`](../references/formats.md),
[`../references/cinematic-mode.md`](../references/cinematic-mode.md),
[`../references/anime-mode.md`](../references/anime-mode.md).
