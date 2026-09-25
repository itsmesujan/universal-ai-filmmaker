# Security, Rights, and Safety

Generated media carries real obligations. This page states the non-negotiable rules and the
practical checks that keep a production clean.

## Hard rules

1. **Never fabricate capabilities, credentials, or results.** An unverified capability is
   recorded as `"unknown"`. A tool result that was not produced is a lie.
2. **Respect rights** for source media, voices, characters, music, likenesses, and any
   copyrighted material. If you cannot establish permission, do not use it.
3. **Do not present generated media as real.** Synthetic footage of real people or events
   must be labelled. Never generate a real person's likeness without consent.
4. **State limitations** instead of substituting a weaker undocumented compromise.
5. **Flag content that needs consent or licensing** before generating it, not after.

## Rights checklist

| Asset type | Check before use |
|---|---|
| Source video/audio | licence, territory, duration of rights |
| Reference images | owned, licensed, or public domain |
| Voices / voice cloning | written consent from the speaker |
| Music | licence for the intended distribution and platform |
| Real people's likenesses | written consent, including for synthetic recreation |
| Brands, logos, uniforms | trademark permission where the depiction is commercial |
| Archive / news footage | rights holder, editorial-use limits |
| Fonts, UI, signage in frame | legibility plus licence |

Record the outcome per asset in the project (a simple `rights` table or README section is
enough). "We will sort it out later" is how a finished film becomes undistributable.

## Data hygiene

- Do not commit real API keys, tokens, or personal data. `.gitignore` excludes
  `.env`, `.env.*`, and local agent state.
- Generated media is excluded by default (`*.mp4`, `*.png`, `renders/`, `outputs/`) —
  keep it out of the repository; keep the **specs and logs** that produced it.
- Run logs contain model names, seeds, and paths. Review before sharing a project publicly.
- Provider uploads: assume anything sent to a third-party model may be retained there. Do
  not upload footage you are not permitted to share.

## Provenance and disclosure

Keep per-asset provenance (see [`reproducibility.md`](reproducibility.md)). Disclose
synthetic media where the audience could reasonably be misled — ads, documentaries, news
adjacent content, and anything depicting real people or events.

## Sensitive content

Extra care is required for: minors, violence, sexual content, self-harm, medical content,
political persuasion, and impersonation. If a request needs consent, licensing, or an
age-gate decision, stop and say so — then offer the portable alternative (a design, a
storyboard, or a non-generative version).

## Safety review before delivery

- [ ] every asset has a recorded rights status
- [ ] no unlicensed voice, likeness, music, or archive material
- [ ] no unverified capability claimed in any artifact
- [ ] synthetic media labelled where deception is plausible
- [ ] no secrets, credentials, or personal data in the repository
- [ ] compromises and unknowns listed in the QC report and `evaluation.md`

## Failure protocol

When something blocks a production on rights or safety grounds:

1. name the blocker precisely (what asset, whose right, which rule);
2. state the smallest change that unblocks it (replace, licence, or remove);
3. deliver the artifacts completed so far, marked incomplete;
4. do not silently substitute an unverified capability or an unlicensed asset.
