#!/usr/bin/env python3
"""Scaffold a new Universal AI Filmmaker project from the bundled templates.

Usage:
    python scripts/new_project.py projects/rain-platform --title "Rain Platform" --duration 90
    python scripts/new_project.py projects/demo --format trailer --duration 60 --force

Creates the canonical artifact set so a production starts from the same structure every
time, then prints the routing block and the next gate to clear.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import shot_budget  # noqa: E402
import uaf_lib as uaf  # noqa: E402

TEMPLATE_DIR = uaf.REPO_ROOT / "templates"

TEMPLATE_FILES = (
    ("project.json", "project.json"),
    ("story.md", "story.md"),
    ("script.md", "script.md"),
    ("character.md", "characters.md"),
    ("location.md", "locations.md"),
    ("style.md", "style.md"),
    ("continuity-ledger.json", "continuity.json"),
    ("beats.json", "beats.json"),
    ("storyboard.md", "storyboard.md"),
    ("audio-plan.md", "audio-plan.md"),
    ("edit-plan.md", "edit-plan.md"),
    ("qc-report.json", "qc-report.json"),
    ("runs.jsonl", "runs.jsonl"),
    ("project-readme.md", "README.md"),
)

SHOT_SKELETON_DEFAULTS = {
    "beat_id": "",
    "story_purpose": "",
    "subject": "",
    "reference_assets": [],
    "start_state": "",
    "primary_action": "",
    "secondary_motion": "",
    "camera": {"type": "", "position": "", "height": "", "lens_equivalent": ""},
    "composition": {"framing": "", "angle": "", "screen_direction": "center"},
    "lighting": {"direction": "", "quality": "", "ratio": "", "temperature": ""},
    "environment": {"location_id": "", "time": "", "weather": ""},
    "style": {"mode": "", "style_lock_ref": "style:main:v1"},
    "performance": {"behaviour": "", "emotion_start": "", "emotion_end": ""},
    "continuity": {},
    "audio": {"dialogue": "", "ambience": ""},
    "timing": {"pacing": "normal"},
    "end_state": "",
    "negative_constraints": [],
    "prompt_version": 1,
}


def substitute(text, values):
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", str(value))
    return text


def build_shots(plan):
    """Turn a budget plan into SHOT_SPEC skeletons ready to be filled in."""
    shots = []
    for planned in plan["shots"]:
        shot = {
            "id": planned["id"],
            "scene_id": planned["scene_id"],
            "coverage_role": planned["coverage_role"],
            "duration_target": planned["duration_target"],
            "generation_method": planned["generation_method"],
            "risk_level": planned["risk_level"],
            "attempt_budget": planned["attempt_budget"],
        }
        shot.update(SHOT_SKELETON_DEFAULTS)
        shots.append(shot)
    return shots


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("target", help="directory to create")
    parser.add_argument("--title", default="Untitled Film")
    parser.add_argument("--id", dest="project_id", default=None)
    parser.add_argument("--duration", type=float, default=90.0)
    parser.add_argument("--format", default="narrative_short")
    parser.add_argument("--aspect", default=None)
    parser.add_argument("--pacing", default="normal", choices=sorted(shot_budget.PACING_FACTORS))
    parser.add_argument("--force", action="store_true", help="overwrite existing files")
    args = parser.parse_args(argv)

    target = Path(args.target)
    target.mkdir(parents=True, exist_ok=True)

    plan = shot_budget.build_plan(args.duration, args.format, args.pacing)
    project_id = args.project_id or target.name.lower().replace(" ", "-")
    aspect = args.aspect or plan["aspect_ratio"]
    values = {
        "project_id": project_id,
        "title": args.title,
        "duration": f"{args.duration:.0f}",
        "format": plan["format"],
        "aspect_ratio": aspect,
        "scene_count": plan["scene_count"],
        "shot_count": plan["shot_count"],
        "date": "YYYY-MM-DD",
    }

    written, skipped = [], []
    for template_name, destination in TEMPLATE_FILES:
        source = TEMPLATE_DIR / template_name
        out_path = target / destination
        if out_path.exists() and not args.force:
            skipped.append(destination)
            continue
        text = substitute(source.read_text(encoding="utf-8"), values) if source.is_file() else ""
        uaf.write_text(out_path, text)
        written.append(destination)

    shots_path = target / "shots.json"
    if not shots_path.exists() or args.force:
        uaf.dump_json(build_shots(plan), shots_path)
        written.append("shots.json")

    continuity_path = target / "continuity.json"
    ledger = uaf.load_json(continuity_path)
    ledger.setdefault("schema_version", "1.1")
    uaf.dump_json(ledger, continuity_path)

    project_path = target / "project.json"
    project = uaf.load_json(project_path)
    project["target_duration_seconds"] = args.duration
    project["aspect_ratio"] = aspect
    project["format"] = plan["format"]
    uaf.dump_json(project, project_path)

    problems = uaf.validate_instance(project, uaf.load_schema("project"))
    print(f"created {len(written)} file(s) in {target}")
    if skipped:
        print(f"kept {len(skipped)} existing file(s): {', '.join(skipped)}")
    if problems:
        print("\nproject.json findings:")
        uaf.print_findings(problems)

    print(
        "\nROUTING\n"
        "  CLASS:       NEW_FILM\n"
        "  STATE:       IDEA (scaffold only)\n"
        "  ENTRY:       STORY -> SCRIPT\n"
        "  MODE:        cinematic (change if the project is drawn/anime)\n"
        f"  ASSUMPTIONS: {args.duration:.0f}s, {aspect}, "
        f"{plan['scene_count']} scenes, {plan['shot_count']} shots\n"
        "  NEXT GATE:   STORY (logline, theme, ending), then SCRIPT\n"
        "\n"
        "The shot skeletons in shots.json are placeholders: fill story_purpose, subject,\n"
        "primary_action, camera, and continuity before generating anything.\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
