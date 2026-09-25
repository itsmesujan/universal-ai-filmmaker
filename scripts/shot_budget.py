#!/usr/bin/env python3
"""Plan a scene/shot budget that sums to a target runtime.

Usage:
    python scripts/shot_budget.py --duration 480
    python scripts/shot_budget.py --duration 90 --format trailer --pacing brisk --json
    python scripts/shot_budget.py --duration 60 --format commercial --out plan.json

The plan is deterministic: the same arguments always produce the same shot list, so a
plan can be reviewed, diffed, and handed to a generator without drift.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import uaf_lib as uaf  # noqa: E402

FORMAT_PROFILES = {
    "narrative_short": {"avg_shot": 5.0, "scene_seconds": 45, "aspect": "16:9"},
    "anime_episode": {"avg_shot": 4.0, "scene_seconds": 60, "aspect": "16:9"},
    "feature": {"avg_shot": 5.0, "scene_seconds": 90, "aspect": "2.39:1"},
    "trailer": {"avg_shot": 2.5, "scene_seconds": 15, "aspect": "2.39:1"},
    "teaser": {"avg_shot": 3.0, "scene_seconds": 12, "aspect": "16:9"},
    "music_video": {"avg_shot": 4.0, "scene_seconds": 30, "aspect": "16:9"},
    "documentary": {"avg_shot": 8.0, "scene_seconds": 120, "aspect": "16:9"},
    "commercial": {"avg_shot": 3.0, "scene_seconds": 10, "aspect": "16:9"},
    "explainer": {"avg_shot": 6.0, "scene_seconds": 45, "aspect": "16:9"},
    "vertical_short": {"avg_shot": 3.0, "scene_seconds": 12, "aspect": "9:16"},
    "series_pilot": {"avg_shot": 5.0, "scene_seconds": 90, "aspect": "16:9"},
}

PACING_FACTORS = {"brisk": 0.8, "normal": 1.0, "slow": 1.25}

COVERAGE_CYCLE = (
    "establishing",
    "subject",
    "action",
    "reaction",
    "insert",
    "subject",
    "action",
    "reaction",
)

DURATION_PATTERN = (1.0, 1.2, 0.8, 1.0, 0.9, 1.3, 0.85, 1.05)

ALIASES = {
    "short_film": "narrative_short",
    "short": "narrative_short",
    "anime": "anime_episode",
    "episode": "anime_episode",
    "ad": "commercial",
    "vertical": "vertical_short",
}


def normalise_format(name):
    key = str(name).strip().lower().replace("-", "_").replace(" ", "_")
    key = ALIASES.get(key, key)
    if key not in FORMAT_PROFILES:
        raise SystemExit(
            f"unknown format {name!r}; choose one of: {', '.join(sorted(FORMAT_PROFILES))}"
        )
    return key


def build_plan(duration, format_name="narrative_short", pacing="normal"):
    """Return a deterministic scene/shot plan for the target runtime."""
    if duration <= 0:
        raise SystemExit("duration must be greater than zero")
    fmt = normalise_format(format_name)
    if pacing not in PACING_FACTORS:
        raise SystemExit(f"unknown pacing {pacing!r}; choose brisk, normal, or slow")

    profile = FORMAT_PROFILES[fmt]
    effective_avg = profile["avg_shot"] * PACING_FACTORS[pacing]
    shot_count = max(1, round(duration / effective_avg))
    scene_count = max(1, min(shot_count, round(duration / profile["scene_seconds"])))

    weights = [DURATION_PATTERN[index % len(DURATION_PATTERN)] for index in range(shot_count)]
    raw_total = sum(weights)
    durations = [round((duration * weight / raw_total) * 2) / 2 for weight in weights]
    durations[-1] = round((duration - sum(durations[:-1])) * 2) / 2
    if durations[-1] <= 0:
        durations = [round(duration / shot_count, 2)] * shot_count

    scenes = [
        {
            "scene_id": f"scene-{index + 1:02d}",
            "shot_ids": [],
            "planned_seconds": 0.0,
            "purpose": "",
            "turn": "",
        }
        for index in range(scene_count)
    ]

    shots = []
    for index, shot_duration in enumerate(durations):
        scene = scenes[index % scene_count]
        shot_id = f"shot-{index + 1:03d}"
        coverage = COVERAGE_CYCLE[index % len(COVERAGE_CYCLE)]
        scene["shot_ids"].append(shot_id)
        scene["planned_seconds"] = round(scene["planned_seconds"] + shot_duration, 2)
        shots.append(
            {
                "id": shot_id,
                "scene_id": scene["scene_id"],
                "coverage_role": coverage,
                "duration_target": shot_duration,
                "generation_method": "text_to_video" if coverage == "establishing" else "image_to_video",
                "risk_level": "low",
                "attempt_budget": uaf.RISK_ATTEMPT_BUDGET["low"],
            }
        )

    total = round(sum(shot["duration_target"] for shot in shots), 2)
    return {
        "format": fmt,
        "pacing": pacing,
        "aspect_ratio": profile["aspect"],
        "target_duration_seconds": float(duration),
        "planned_duration_seconds": total,
        "drift_percent": round(abs(total - duration) / duration * 100, 2),
        "scene_count": scene_count,
        "shot_count": shot_count,
        "average_shot_seconds": round(total / shot_count, 2),
        "scenes": scenes,
        "shots": shots,
        "notes": [
            "One action and one camera move per shot; split any shot that needs more.",
            "Re-plan shots whose duration_target exceeds the chosen model's clip limit.",
            "Coverage roles are suggestions; replace them with real story function.",
        ],
    }


def render(plan):
    lines = [
        f"format           {plan['format']} ({plan['aspect_ratio']})",
        f"pacing           {plan['pacing']}",
        f"target           {plan['target_duration_seconds']:.1f}s",
        f"planned          {plan['planned_duration_seconds']:.1f}s ({plan['drift_percent']}% drift)",
        f"scenes / shots   {plan['scene_count']} / {plan['shot_count']}",
        f"average shot     {plan['average_shot_seconds']:.1f}s",
        "",
        "scene       shots  seconds",
    ]
    for scene in plan["scenes"]:
        lines.append(
            f"{scene['scene_id']:<11} {len(scene['shot_ids']):>5}  {scene['planned_seconds']:>7.1f}"
        )
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--duration", type=float, required=True, help="target runtime in seconds")
    parser.add_argument("--format", default="narrative_short", help="project format profile")
    parser.add_argument("--pacing", default="normal", choices=sorted(PACING_FACTORS))
    parser.add_argument("--json", action="store_true", help="print the plan as JSON")
    parser.add_argument("--out", metavar="FILE", help="write the plan JSON to FILE")
    args = parser.parse_args(argv)

    plan = build_plan(args.duration, args.format, args.pacing)

    if args.out:
        uaf.dump_json(plan, args.out)
        print(f"wrote plan to {args.out}")
    if args.json:
        print(json.dumps(plan, indent=2))
    else:
        print(render(plan))

    return 0 if plan["drift_percent"] <= 10 else 1


if __name__ == "__main__":
    raise SystemExit(main())
