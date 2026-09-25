# FAQ

**Do I need a specific AI video model to use this?**
No. The core is provider-neutral. Adapters are optional, replaceable snapshots, and one
ships as a deliberately unverified template.

**Do I need Python?**
Only for the tooling (validation, compilation, budgeting, drift detection). The references
and templates work without it; you can reproduce the logic by hand.

**Can I use this for a 10-minute film?**
Yes — that is the design target. Expect roughly 8–15 scenes and 25–80 shots, planned as
3–8 s clips rather than one long request.

**Why not just write good prompts?**
Because a prompt is not a project. Without a spec, canon, and a ledger, shot 27 will not
match shot 3, and you will not be able to tell why.

**Is the SHOT_SPEC provider-specific?**
No. Provider syntax belongs in adapters. The compiler emits neutral prompts with named blocks.

**How many shots should my film have?**
Use `../scripts/shot_budget.py` with your format and pacing. A 6-minute narrative short plans
to about 72 shots at ~5 s each; a 60-second commercial to roughly 20 at ~3 s.

**How do I keep a character consistent?**
Versioned canon id plus a reference sheet, a style lock, and continuity anchors in every
shot; then run `../scripts/continuity_check.py`. Consistency is a written artifact, not luck.

**What if my model can't do something I planned?**
Record `"unknown"` (or unsupported) in the adapter, write the fallback in `degraded_mode`,
and re-plan the affected shots. Never assume a capability to keep the plan pretty.

**Should I generate dialogue with the video?**
Only if lip-sync is verified for that model. Otherwise plan coverage that avoids mouths —
profile, wide, obstructed, or reaction cutaways — and dub in the edit.

**Where do I put prompts?**
Compile them into `image-prompts.md` / `video-prompts.md`. Never hand-edit a compiled prompt
without bumping `prompt_version`, and never treat a prompt as the source of truth.

**How do I know a shot is good enough?**
Score it against the QC scorecard: average ≥ 4.0 with nothing below 3. The rubric is in
[`quality-control.md`](quality-control.md).

**Can I mix cinematic and anime shots?**
Yes, if the style bible declares the mixing rule and each exception is marked in
`style.mode`. Random mixing reads as inconsistency.

**What is the single highest-leverage habit?**
Write canon before generating, and classify failures before repairing. Almost everything
else in this documentation exists to make those two cheap.

**Does the skill need network access or credentials?**
No. It never fabricates tool results; if generation tooling is unavailable it produces
portable artifacts and exact next steps instead.

**How do I contribute?**
See [`../CONTRIBUTING.md`](../CONTRIBUTING.md). Keep the core provider-neutral, add eval cases
for lessons learned, and run the CI sequence before opening a pull request.

**Something is broken. Where do I look first?**
[`troubleshooting.md`](troubleshooting.md), then run
`python scripts/lint_skill.py` and `python scripts/run_evals.py`.
