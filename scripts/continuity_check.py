#!/usr/bin/env python3
"""Detect continuity drift between SHOT_SPEC records and the continuity ledger.

Usage:
    python scripts/continuity_check.py shots.json continuity.json
    python scripts/continuity_check.py examples/mini-project
    python scripts/continuity_check.py shots.json continuity.json --json
    python scripts/continuity_check.py shots.json continuity.json --write

Checks: unresolved canon references, per-scene costume/state drift, per-scene light
direction drift, axis/screen-direction flips, emotional jumps, and open ledger violations.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import uaf_lib as uaf  # noqa: E402

CANON_KIND_TO_CLASS = {
    "character": "IDENTITY",
    "location": "GEOGRAPHY",
    "prop": "OBJECTS",
    "style": "STYLE",
    "voice": "IDENTITY",
}


def load_inputs(paths):
    """Load shots and ledger from explicit paths or a project directory."""
    shots_path = ledger_path = None
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            candidate = path / "shots.json"
            if candidate.is_file():
                shots_path = candidate
            candidate = path / "continuity.json"
            if candidate.is_file():
                ledger_path = candidate
        elif path.name.lower().startswith("shot"):
            shots_path = path
        elif path.name.lower().startswith("continuity"):
            ledger_path = path

    if not shots_path:
        raise SystemExit("no shots file found (expected shots.json)")
    shots = uaf.load_json(shots_path)
    if isinstance(shots, dict):
        shots = shots.get("shots") or []
    ledger = uaf.load_json(ledger_path) if ledger_path else {}
    return shots, ledger, shots_path, ledger_path


def canon_checks(shots, ledger, violations):
    known = uaf.canon_ids_from_ledger(ledger)
    for shot in shots:
        shot_id = str(shot.get("id", "<unnamed>"))
        for reference in shot.get("reference_assets") or []:
            reference = str(reference)
            kind = uaf.canon_kind(reference)
            if kind is None:
                violations.append(
                    {
                        "shot_id": shot_id,
                        "class": "OTHER",
                        "decision": "open",
                        "notes": f"reference {reference!r} is not a versioned canon id",
                    }
                )
                continue
            if known and reference not in known:
                violations.append(
                    {
                        "shot_id": shot_id,
                        "class": CANON_KIND_TO_CLASS.get(kind, "OTHER"),
                        "decision": "open",
                        "notes": f"reference {reference!r} is missing from the continuity ledger",
                    }
                )


def scene_drift_checks(shots, violations):
    by_scene = {}
    for shot in shots:
        by_scene.setdefault(str(shot.get("scene_id", "scene-unknown")), []).append(shot)

    for scene_id, scene_shots in by_scene.items():
        costume_values = {}
        light_directions = {}
        for shot in scene_shots:
            shot_id = str(shot.get("id", "<unnamed>"))
            for key, value in (shot.get("continuity") or {}).items():
                if "costume" in key.lower() and isinstance(value, str) and value.strip():
                    costume_values.setdefault(value, []).append(shot_id)
            direction = (shot.get("lighting") or {}).get("direction")
            if isinstance(direction, str) and direction.strip():
                light_directions.setdefault(direction, []).append(shot_id)

        if len(costume_values) > 1:
            violations.append(
                {
                    "shot_id": scene_shots[0].get("id", "<unnamed>"),
                    "class": "STATE",
                    "decision": "open",
                    "notes": (
                        f"{scene_id}: costume versions differ between shots "
                        + "; ".join(f"{value}={ids}" for value, ids in sorted(costume_values.items()))
                    ),
                }
            )
        if len(light_directions) > 1:
            violations.append(
                {
                    "shot_id": scene_shots[0].get("id", "<unnamed>"),
                    "class": "LIGHTING",
                    "decision": "open",
                    "notes": (
                        f"{scene_id}: key light direction changes between shots "
                        + "; ".join(f"{value}={ids}" for value, ids in sorted(light_directions.items()))
                    ),
                }
            )


def axis_checks(shots, violations):
    by_scene = {}
    for shot in shots:
        by_scene.setdefault(str(shot.get("scene_id", "scene-unknown")), []).append(shot)

    for scene_id, scene_shots in by_scene.items():
        for index in range(1, len(scene_shots)):
            previous = (scene_shots[index - 1].get("composition") or {}).get("screen_direction")
            current = (scene_shots[index].get("composition") or {}).get("screen_direction")
            if not previous or not current or previous == current:
                continue
            if "center" in (previous, current):
                continue
            violations.append(
                {
                    "shot_id": scene_shots[index].get("id", "<unnamed>"),
                    "class": "GEOGRAPHY",
                    "decision": "open",
                    "notes": (
                        f"{scene_id}: screen direction flips {previous!r} -> {current!r}; "
                        "insert a neutral shot or lock the axis"
                    ),
                }
            )
            break


def emotional_chain_checks(ledger, violations):
    entries = [entry for entry in (ledger.get("emotional_state") or []) if isinstance(entry, dict)]
    for index in range(1, len(entries)):
        previous, current = entries[index - 1], entries[index]
        previous_end = str(previous.get("end", "")).strip().lower()
        current_start = str(current.get("start", "")).strip().lower()
        if previous_end and current_start and previous_end != current_start:
            violations.append(
                {
                    "shot_id": str(current.get("shot_id", "<unnamed>")),
                    "class": "EMOTIONAL",
                    "decision": "open",
                    "notes": (
                        f"emotional state jumps: previous end {previous_end!r} "
                        f"!= current start {current_start!r}"
                    ),
                }
            )


def open_ledger_violations(ledger, violations):
    for entry in ledger.get("violations") or []:
        if isinstance(entry, dict) and entry.get("decision") in (None, "open"):
            violations.append(
                {
                    "shot_id": str(entry.get("shot_id", "<unnamed>")),
                    "class": str(entry.get("class", "OTHER")),
                    "decision": "open",
                    "notes": "carried over from the ledger: " + str(entry.get("notes", "")),
                }
            )


def dedupe(violations):
    seen = set()
    unique = []
    for violation in violations:
        key = (violation.get("shot_id"), violation.get("class"), violation.get("notes"))
        if key in seen:
            continue
        seen.add(key)
        unique.append(violation)
    return unique


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("paths", nargs="+", help="shots.json + continuity.json, or a project directory")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--write", action="store_true", help="append findings to the ledger")
    parser.add_argument("--strict", action="store_true", help="exit non-zero when drift is found")
    args = parser.parse_args(argv)

    shots, ledger, shots_path, ledger_path = load_inputs(args.paths)

    violations = []
    canon_checks(shots, ledger, violations)
    scene_drift_checks(shots, violations)
    axis_checks(shots, violations)
    emotional_chain_checks(ledger, violations)
    open_ledger_violations(ledger, violations)
    violations = dedupe(violations)

    if args.write:
        if not ledger_path:
            raise SystemExit("--write requires a continuity.json path")
        existing = ledger.setdefault("violations", [])
        keys = {(item.get("shot_id"), item.get("class"), item.get("notes")) for item in existing}
        added = 0
        for violation in violations:
            key = (violation.get("shot_id"), violation.get("class"), violation.get("notes"))
            if key not in keys:
                existing.append(violation)
                keys.add(key)
                added += 1
        uaf.dump_json(ledger, ledger_path)
        print(f"appended {added} violation(s) to {ledger_path}")

    if args.json:
        print(json.dumps({"shots": str(shots_path), "violations": violations}, indent=2))
    else:
        print(f"continuity check: {len(shots)} shot(s) against {ledger_path or 'no ledger'}")
        if violations:
            print(f"\nDRIFT ({len(violations)})")
            for violation in violations:
                print(f"  [{violation['class']}] {violation['shot_id']}: {violation['notes']}")
        else:
            print("\nno drift detected")

    return 1 if (violations and args.strict) else 0


if __name__ == "__main__":
    raise SystemExit(main())
