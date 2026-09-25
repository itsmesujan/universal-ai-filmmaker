# Shot Grammar (Canonical Vocabulary)

Use these tokens in `SHOT_SPEC`. They are provider-neutral: adapters translate tokens
into provider syntax, and unknown tokens fall back to descriptive text. Consistency of
vocabulary is what makes 40 shots feel like one film — and what makes exports mappable.

## Shot size

`extreme_wide`, `wide`, `full`, `medium_full`, `medium`, `medium_close`, `close`,
`extreme_close`, `insert`, `over_shoulder`, `pov`, `two_shot`, `three_shot`, `group`,
`aerial`, `top_down`.

## Camera angle and height

`eye_level`, `low_angle`, `high_angle`, `bird_eye`, `worm_eye`, `dutch`, `profile`,
`three_quarter`, `frontal`, `behind`.

## Lens

| Token | Look | Practical use |
|---|---|---|
| `ultra_wide` (≈18 mm) | distorted, immersive | scale, chaos, interiors |
| `wide` (≈24–28 mm) | environmental | establishing, geography |
| `normal` (≈35–50 mm) | natural | dialogue, neutral coverage |
| `portrait` (≈85 mm) | flattering compression | intimacy, isolation |
| `telephoto` (≈135 mm+) | flattened, compressed | voyeurism, crowd crush |
| `macro` | surface detail | inserts, texture, clues |

## Movement (choose one primary per shot)

`static`, `slow_push_in`, `push_in`, `pull_out`, `dolly_in`, `dolly_out`,
`truck_left`, `truck_right`, `pan_left`, `pan_right`, `tilt_up`, `tilt_down`,
`crane_up`, `crane_down`, `arc_left`, `arc_right`, `handheld`, `steadicam`,
`tracking_follow`, `orbit`, `whip_pan`, `zoom_in`, `zoom_out`, `dolly_zoom`,
`crash_zoom`, `reveal_pan`.

Rules:

1. One primary movement per shot. A second movement must be motivated and recorded in `secondary_motion`.
2. Movement must have a reason: reveal, follow, escalate, or withhold.
3. Static is a valid, often stronger choice. Constant movement reads as amateur.
4. Fast movement plus complex subject action multiplies failure risk; split the shot.

## Composition

`center_symmetry`, `rule_of_thirds`, `negative_space`, `frame_in_frame`, `layered`,
`silhouette`, `low_horizon`, `high_horizon`, `foreground_occlusion`, `leading_lines`,
`deep_focus`, `shallow_focus`.

Track headroom, lead_room/nose_room, screen_direction, and subject position:
`left`, `right`, `center`, `moving_left`, `moving_right`.

## Lighting tokens

Direction → `front`, `three_quarter`, `side`, `back`, `top`, `under`, `ambient`.
Quality → `hard`, `soft`, `diffused`, `dappled`, `harsh`.
Ratio → `low`, `medium`, `high` (contrast between key and fill).
Temperature → `warm`, `neutral`, `cool`, or Kelvin (`3200K`, `5600K`).
Sources → `practical`, `motivated`, `available`, `firelight`, `screen_glow`,
`neon`, `moonlight`, `overcast`, `golden_hour`, `blue_hour`.

## Transitions

`cut`, `hard_cut_on_action`, `match_cut`, `smash_cut`, `dissolve`, `cross_dissolve`,
`fade_in`, `fade_out`, `whip_pan_transition`, `l_cut`, `j_cut`, `whip_to_black`.

## Emotion → grammar cheatsheet

| Intent | Grammar |
|---|---|
| tension | tighten framing, static or micro-push, high contrast, longer holds |
| isolation | portrait/telephoto, negative space, static, off-centre |
| threat | low angle, backlight, slow creep-in, foreground occlusion |
| chaos | handheld, short lens, fast cuts, layered motion |
| revelation | reveal_pan or push_in landing on the subject, sound drop-out |
| grief | static wide, subject small in frame, soft light, long take |
| nostalgia | warm 3200K, soft diffusion, gentle drift, shallow focus |
| power | low angle, centre symmetry, slow crane, deep focus |

## Compliance rules

- Every `SHOT_SPEC` must declare `camera.type`, `composition.framing`, and `lens_equivalent`.
- Screen direction is locked per scene; a reversal must be a deliberate, recorded decision.
- Adapters must not invent tokens. Unsupported tokens are omitted or rendered as prose.
