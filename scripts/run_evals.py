#!/usr/bin/env python3
"""Run the deterministic skill evals in ``evals/cases/``.

Usage:
    python scripts/run_evals.py
    python scripts/run_evals.py --json
    python scripts/run_evals.py --only continuity

Case types: ``validate``, ``prompt_compile``, ``shot_budget``, ``continuity``, ``risk``.
Creative quality is graded by the human rubrics in ``evals/rubrics/`` instead.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import continuity_check  # noqa: E402
import prompt_compile  # noqa: E402
import shot_budget  # noqa: E402
import uaf_lib as uaf  # noqa: E402
import validate as validate_mod  # noqa: E402

CASES_DIR = uaf.REPO_ROOT / "evals" / "cases"


def _resolve(relative):
    return (uaf.REPO_ROOT / relative).resolve()


def eval_validate(case, failures):
    target = _resolve(case["path"])
    targets = validate_mod.collect_targets([str(target)])
    errors, checked = [], 0
    for path in targets:
        data = uaf.load_json(path)
        schema_name = uaf.detect_schema_name(path, data)
        if not schema_name:
            continue
        checked += 1
        errors.extend(uaf.validate_instance(data, uaf.load_schema(schema_name)))
    expectation = case.get("expect", {})
    if checked < expectation.get("min_checked", 1):
        failures.append(f"checked only {checked} artifact(s)")
    if len(errors) != expectation.get("errors", 0):
        failures.append(
            f"expected {expectation.get('errors', 0)} schema errors, got {len(errors)}: {errors[:3]}"
        )
    return {"checked": checked, "errors": errors}


def eval_prompt_compile(case, failures):
    shots = prompt_compile.load_shots(_resolve(case["shots"]))
    wanted = case["shot"]
    shot = next((item for item in shots if str(item.get("id")) == wanted), None)
    if shot is None:
        failures.append(f"shot {wanted!r} not found")
        return {}
    image = uaf.compile_image_prompt(shot)
    video = uaf.compile_video_prompt(shot)
    for block in case.get("expect_image_blocks", []):
        if f"{block}:" not in image:
            failures.append(f"image prompt missing block {block!r}")
    for block in case.get("expect_video_blocks", []):
        if f"{block}:" not in video:
            failures.append(f"video prompt missing block {block!r}")
    findings = uaf.lint_prompt(wanted, image, shot) + uaf.lint_prompt(wanted, video, shot)
    if case.get("expect_no_lint") and findings:
        failures.append(f"lint findings: {findings}")
    if case.get("expect_lint_contains"):
        if not any(case["expect_lint_contains"] in finding for finding in findings):
            failures.append(f"expected a lint finding containing {case['expect_lint_contains']!r}")
    return {"lint": findings}


def eval_shot_budget(case, failures):
    plan = shot_budget.build_plan(
        case["duration"], case.get("format", "narrative_short"), case.get("pacing", "normal")
    )
    expectation = case.get("expect", {})
    if plan["drift_percent"] > expectation.get("max_drift_percent", 10):
        failures.append(f"drift {plan['drift_percent']}% exceeds limit")
    if plan["shot_count"] < expectation.get("min_shots", 1):
        failures.append(f"shot_count {plan['shot_count']} below minimum")
    if plan["shot_count"] > expectation.get("max_shots", 10000):
        failures.append(f"shot_count {plan['shot_count']} above maximum")
    if abs(plan["planned_duration_seconds"] - case["duration"]) > 1.0:
        failures.append("planned duration does not match the target")
    return {"shot_count": plan["shot_count"], "scene_count": plan["scene_count"]}


def eval_continuity(case, failures):
    shots = uaf.load_json(_resolve(case["shots"]))
    if isinstance(shots, dict):
        shots = shots.get("shots") or []
    ledger = uaf.load_json(_resolve(case["ledger"])) if case.get("ledger") else {}
    violations = []
    continuity_check.canon_checks(shots, ledger, violations)
    continuity_check.scene_drift_checks(shots, violations)
    continuity_check.axis_checks(shots, violations)
    continuity_check.emotional_chain_checks(ledger, violations)
    classes = {violation["class"] for violation in violations}
    for expected in case.get("expect_classes", []):
        if expected not in classes:
            failures.append(f"expected a {expected!r} violation, got {sorted(classes)}")
    for forbidden in case.get("forbid_classes", []):
        if forbidden in classes:
            failures.append(f"unexpected {forbidden!r} violation")
    return {"classes": sorted(classes), "count": len(violations)}


def eval_risk(case, failures):
    scored = uaf.score_risk(case["shot"])
    expectation = case.get("expect", {})
    if "risk_level" in expectation and scored["risk_level"] != expectation["risk_level"]:
        failures.append(f"expected risk {expectation['risk_level']!r}, got {scored['risk_level']!r}")
    if "min_total" in expectation and scored["total"] < expectation["min_total"]:
        failures.append(f"risk total {scored['total']} below {expectation['min_total']}")
    if "attempt_budget" in expectation and scored["suggested_attempt_budget"] != expectation["attempt_budget"]:
        failures.append("attempt budget mismatch")
    return scored


RUNNERS = {
    "validate": eval_validate,
    "prompt_compile": eval_prompt_compile,
    "shot_budget": eval_shot_budget,
    "continuity": eval_continuity,
    "risk": eval_risk,
}


def load_cases(only=None):
    cases = []
    for path in sorted(CASES_DIR.glob("*.json")):
        case = uaf.load_json(path)
        case.setdefault("type", "validate")
        if only and only not in case["id"] and only != case.get("type"):
            continue
        cases.append(case)
    return cases


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--json", action="store_true", help="emit JSON results")
    parser.add_argument("--only", default=None, help="filter by case id or type substring")
    args = parser.parse_args(argv)

    cases = load_cases(args.only)
    results = []
    for case in cases:
        runner = RUNNERS.get(case["type"])
        failures = []
        if runner is None:
            failures.append(f"unknown case type {case['type']!r}")
        else:
            try:
                runner(case, failures)
            except Exception as exc:  # noqa: BLE001 - evals must report, not crash
                failures.append(f"{type(exc).__name__}: {exc}")
        results.append(
            {"id": case["id"], "type": case["type"], "passed": not failures, "failures": failures}
        )

    passed = sum(1 for result in results if result["passed"])
    total = len(results)

    if args.json:
        print(json.dumps({"passed": passed, "total": total, "results": results}, indent=2))
    else:
        for result in results:
            mark = "PASS" if result["passed"] else "FAIL"
            print(f"{mark}  {result['id']} ({result['type']})")
            uaf.print_findings(result["failures"], prefix="        ")
        print(f"\nevals: {passed}/{total} passed")

    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
