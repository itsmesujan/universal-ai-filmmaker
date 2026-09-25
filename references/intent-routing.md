# Intent Routing and State Detection

Read this before producing any artifact. The most common cause of weak output is
starting at the wrong production state. Route first, generate second.

## 1. Classify the request

| Class | Signals | Entry state |
|---|---|---|
| `NEW_FILM` | idea, logline, "make me a film", genre only | IDEA |
| `CONTINUE` | "next", "keep going", existing artifacts | first incomplete state |
| `SCRIPT_IN` | user pastes a script, treatment, or story | SCRIPT (validate → BIBLES) |
| `SINGLE_SHOT` | "one shot of ...", "a 5s clip of ..." | SHOTS |
| `REPAIR` | "this clip is wrong", "fix the face" | QC |
| `ADAPT` | "make it work for model X", "export for Y" | MODEL ADAPTATION |
| `REVIEW` | "critique", "evaluate", "what's wrong" | current state, read-only |
| `PLAN_ONLY` | "just the plan", "no generation", "docs only" | stop before generation |

State the class in a single line so the user can correct you cheaply.

## 2. Probe the production state

Check artifacts in pipeline order and stop at the first missing or incomplete one:

1. project manifest → 2. story/logline → 3. screenplay → 4. character bible →
5. world/location bible → 6. style bible → 7. continuity ledger → 8. beats →
9. shot list → 10. storyboard/keyframes → 11. images → 12. video →
13. voice → 14. music/SFX → 15. edit → 16. QC → 17. repair → 18. final.

If artifacts are unavailable, ask for them or reconstruct the missing earlier state.
Never silently invent an approved screenplay because a shot list exists.

## 3. Bounded clarification

Ask **at most three** questions, and only questions whose answers change the plan:

1. What is it? (format, subject, tone)
2. How long is it, and where will it be seen? (runtime + aspect/platform)
3. What must not change? (canon, rights, cast, references, deadline)

Never ask a question you can answer with a safe, stated default. If the user says
"you decide", pick the default below, label it as an assumption, and proceed.

| Unknown | Default |
|---|---|
| runtime | 60–120 s unless "trailer", "music video", or "film" implies otherwise |
| aspect | 16:9; 9:16 for social/vertical; 2.39:1 for trailer/anamorphic intent |
| mode | cinematic unless characters are drawn/anime-coded |
| language | user's language |
| dialogue | minimal; prefer visual storytelling when live audio/sync is unverified |
| model | unknown → produce portable artifacts only |

## 4. Choose the mode

- `cinematic-mode.md` for live-action-style photoreal or grounded drama.
- `anime-mode.md` for drawn, cel-shaded, or stylised animation.
- `formats.md` for trailer, music video, documentary, commercial, explainer, vertical.
- Mixing modes inside one project is allowed, but lock the mixing rule in the
  style bible and never mix per shot at random.

## 5. Declare the routing decision

Before the first artifact, emit a compact routing block:

```text
CLASS:      NEW_FILM
STATE:      IDEA (no approved artifacts found)
ENTRY:      STORY → SCRIPT
MODE:       cinematic
ASSUMPTIONS: 90s runtime, 16:9, dialogue-light, no verified model
NEXT:       story.md, then approval gate before beats
```

## 6. Quality gates

Never pass a gate without explicit evidence:

| Gate | Pass condition |
|---|---|
| STORY | logline + theme + ending are stated and accepted |
| SCRIPT | every scene has purpose, turn, and a location that exists in the bible |
| BIBLES | every character/location used by the script is defined with canon IDs |
| BEATS | every beat maps to a story function and at least one visual idea |
| SHOTS | every shot has purpose, one action, one camera behaviour, duration target |
| KEYFRAMES | style and identity are representative before bulk generation |
| VIDEO | QC rubric passed or a repair plan recorded |
| FINAL | continuity ledger clean, audio/edit plan complete, QC report signed |

If a gate fails, stop and report the blocker. Do not generate the next stage "to save time".

## 7. Cost discipline

Validate the riskiest assumption on the cheapest artifact. Lock style on a
representative shot, not on the hero shot, and never bulk-generate before the
KEYFRAMES gate passes. See `risk-cost.md`.
