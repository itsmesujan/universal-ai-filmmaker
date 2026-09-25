#!/usr/bin/env python3
"""Validate Universal AI Filmmaker artifacts against the bundled JSON Schemas.

Usage:
    python scripts/validate.py <file-or-directory> [...]
    python scripts/validate.py examples/mini-project
    python scripts/validate.py shots.json --json

Schema validation is structural; the semantic checks catch planning mistakes a schema
cannot express (missing canon references, unbudgeted risk, stale adapters, unrepairable
QC verdicts).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import uaf_lib as uaf  # noqa: E402

PLACEHOLDER_DATES = {"", "YYYY-MM-DD", "unknown", "TBD"}
KNOWN_FILES = ("project.json", "shots.json", "beats.json", "continuity.json", "qc-report.json")


def collect_targets(paths):
    """Expand CLI paths into the JSON files that should be validated.

    Directories are walked recursively; schema files and ``*template*`` files are skipped
    (a template contains placeholders and is not a valid instance).
    """
    targets = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            for candidate in sorted(path.rglob("*.json")):
                if candidate.name.endswith(".schema.json"):
                    continue
                if "template" in candidate.name:
                    continue
                targets.append(candidate)
        else:
            targets.append(path)
    unique = []
    for target in targets:
        if target not in unique:
            unique.append(target)
    return unique


def _id_set(entries):
    ids = set()
    for entry in entries or []:
        if isinstance(entry, dict) and entry.get("id"):
            ids.add(str(entry["id"]))
        elif isinstance(entry, str):
            ids.add(entry)
    return ids


def semantic_project(data, shots, warnings, errors):
    scene_ids = _id_set(data.get("scenes") or [])
    inline_shots = [shot for shot in (data.get("shots") or []) if isinstance(shot, dict)]
    all_shots = list(shots) + inline_shots

    ids = [str(shot.get("id")) for shot in all_shots if shot.get("id")]
    for duplicate in sorted({item for item in ids if ids.count(item) > 1}):
        errors.append(f"project: duplicate shot id {duplicate!r}")

    if scene_ids:
        for shot in all_shots:
            scene_id = shot.get("scene_id")
            if scene_id and str(scene_id) not in scene_ids:
                errors.append(f"project: shot {shot.get('id')!r} references unknown scene {scene_id!r}")

    total = 0.0
    for shot in all_shots:
        try:
            total += float(shot.get("duration_target", 0))
        except (TypeError, ValueError):
            continue
    target = data.get("target_duration_seconds")
    if all_shots and isinstance(target, (int, float)) and target:
        drift = abs(total - float(target)) / float(target)
        if drift > 0.10:
            warnings.append(
                f"project: planned {total:.1f}s is {drift * 100:.0f}% from target "
                f"{float(target):.1f}s (keep within ±10%)"
            )


def semantic_shots(shots, warnings, errors):
    ids = [str(shot.get("id")) for shot in shots if isinstance(shot, dict) and shot.get("id")]
    for duplicate in sorted({item for item in ids if ids.count(item) > 1}):
        errors.append(f"shots: duplicate id {duplicate!r}")

    for shot in shots:
        if not isinstance(shot, dict):
            continue
        shot_id = shot.get("id", "<unnamed>")
        if not (shot.get("camera") or {}).get("type"):
            warnings.append(f"shots: {shot_id} has no camera.type (one camera behaviour is required)")
        if not (shot.get("continuity") or {}):
            warnings.append(f"shots: {shot_id} has an empty continuity block")
        try:
            duration = float(shot.get("duration_target", 0))
        except (TypeError, ValueError):
            duration = 0.0
        if duration > 12:
            warnings.append(f"shots: {shot_id} duration {duration}s is very long for one generation")

        scored = uaf.score_risk(shot)
        declared = shot.get("risk_level")
        if declared and declared != scored["risk_level"]:
            warnings.append(
                f"shots: {shot_id} declares risk_level {declared!r} but the risk axes score "
                f"{scored['risk_level']!r} ({scored['total']}/12)"
            )
        budget = shot.get("attempt_budget")
        if isinstance(budget, int) and isinstance(declared, str) and declared in uaf.RISK_ATTEMPT_BUDGET:
            expected = uaf.RISK_ATTEMPT_BUDGET[declared]
            if budget > expected * 2:
                warnings.append(
                    f"shots: {shot_id} attempt_budget {budget} far exceeds the {declared} budget {expected}"
                )


def semantic_beats(beats, shot_ids, warnings):
    for beat in beats:
        if not isinstance(beat, dict):
            continue
        beat_id = beat.get("beat_id", "<unnamed>")
        mapped = beat.get("shot_ids") or []
        if not mapped:
            warnings.append(f"beats: {beat_id} maps to no shots")
        for shot_id in mapped:
            if shot_ids and str(shot_id) not in shot_ids:
                warnings.append(f"beats: {beat_id} references unknown shot {shot_id!r}")


def semantic_qc(data, warnings, errors):
    threshold = data.get("pass_threshold", 4)
    entries = [entry for entry in (data.get("shots") or []) if isinstance(entry, dict)]
    for entry in entries:
        shot_id = entry.get("shot_id", "<unnamed>")
        status = entry.get("status")
        score = entry.get("score")
        if status == "PASS" and isinstance(score, (int, float)) and score < threshold:
            errors.append(f"qc: {shot_id} marked PASS with score {score} below threshold {threshold}")
        if status in {"REPAIR", "REGENERATE", "REPLACE"}:
            if not entry.get("repair"):
                warnings.append(f"qc: {shot_id} is {status} without a recorded repair action")
            if not entry.get("failure_class"):
                warnings.append(f"qc: {shot_id} is {status} without a failure_class")
    if data.get("final_decision") == "PASS":
        unresolved = [
            entry.get("shot_id")
            for entry in entries
            if entry.get("status") in {"REPAIR", "REGENERATE", "REPLACE"}
        ]
        if unresolved:
            errors.append(f"qc: final_decision PASS with unresolved shots {unresolved}")


def semantic_adapter(data, warnings, errors):
    verified = str(data.get("verified_at", ""))
    if data.get("placeholder") is True:
        warnings.append(
            "adapter: placeholder snapshot - capabilities unverified, do not use for generation"
        )
        return
    if verified in PLACEHOLDER_DATES:
        errors.append("adapter: verified_at is a placeholder; adapters must record a verification date")
    capabilities = data.get("capabilities") or {}
    claimed = [key for key, value in capabilities.items() if value is True]
    if claimed and verified in PLACEHOLDER_DATES:
        errors.append(f"adapter: capabilities {claimed} claimed true without verification")
    if all(value == "unknown" for value in capabilities.values()) and not data.get("degraded_mode"):
        warnings.append("adapter: capabilities unknown; document fallbacks in degraded_mode")


def semantic_continuity(data, warnings):
    for violation in data.get("violations") or []:
        if isinstance(violation, dict) and violation.get("decision") in (None, "open"):
            warnings.append(
                f"continuity: violation on {violation.get('shot_id')!r} has no resolution decision"
            )


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("paths", nargs="+", help="files or project directories to validate")
    parser.add_argument("--json", action="store_true", help="emit machine-readable results")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args(argv)

    targets = collect_targets(args.paths)
    if not targets:
        print("validate: no JSON artifacts found", file=sys.stderr)
        return 2

    errors, warnings, checked, skipped = [], [], [], []

    for target in targets:
        if target.name.endswith(".schema.json"):
            skipped.append(str(target))
            continue
        try:
            data = uaf.load_json(target)
        except json.JSONDecodeError as exc:
            errors.append(f"{target}: invalid JSON ({exc})")
            continue
        schema_name = uaf.detect_schema_name(target, data)
        if not schema_name:
            skipped.append(str(target))
            continue
        for problem in uaf.validate_instance(data, uaf.load_schema(schema_name)):
            errors.append(f"{target} [{schema_name}] {problem}")
        checked.append((target, schema_name, data))

    # Cross-file checks run per directory: a project only relates to the artifacts that
    # sit beside it, never to another example or project in the repository.
    per_dir = {}
    for target, schema_name, data in checked:
        per_dir.setdefault(target.parent.resolve(), {})[schema_name] = data

    for artifacts in per_dir.values():
        shots = artifacts.get("shots")
        if isinstance(shots, dict):
            shots = shots.get("shots") or []
        shots = shots or []
        if "project" in artifacts:
            semantic_project(artifacts["project"], shots, warnings, errors)
        if "shots" in artifacts:
            semantic_shots(shots, warnings, errors)
        if "beats" in artifacts:
            semantic_beats(artifacts["beats"], uaf.shot_ids_from(shots), warnings)
        if "qc" in artifacts:
            semantic_qc(artifacts["qc"], warnings, errors)
        if "model-adapter" in artifacts:
            semantic_adapter(artifacts["model-adapter"], warnings, errors)
        if "continuity" in artifacts:
            semantic_continuity(artifacts["continuity"], warnings)

    if args.strict:
        errors.extend(warnings)
        warnings = []

    if args.json:
        print(
            json.dumps(
                {
                    "checked": [{"file": str(t), "schema": s} for t, s, _ in checked],
                    "skipped": skipped,
                    "errors": errors,
                    "warnings": warnings,
                    "ok": not errors,
                },
                indent=2,
            )
        )
    else:
        for target, schema_name, _data in checked:
            print(f"OK   {target} [{schema_name}]")
        for path in skipped:
            print(f"SKIP {path}")
        if warnings:
            print(f"\nWARNINGS ({len(warnings)})")
            uaf.print_findings(warnings)
        if errors:
            print(f"\nERRORS ({len(errors)})")
            uaf.print_findings(errors)
        print(f"\n{len(checked)} checked, {len(errors)} errors, {len(warnings)} warnings")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
