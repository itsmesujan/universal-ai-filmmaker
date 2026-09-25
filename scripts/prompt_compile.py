#!/usr/bin/env python3
"""Compile model-neutral image and video prompts from SHOT_SPEC records.

Usage:
    python scripts/prompt_compile.py shots.json
    python scripts/prompt_compile.py shots.json --shot shot-001 --format both
    python scripts/prompt_compile.py shots.json --lint           # lint every shot
    python scripts/prompt_compile.py shots.json --json
    python scripts/prompt_compile.py shots.json --write out/

The compilation order is fixed (see references/prompt-compilation.md) so prompts are
diffable, reusable, and stable across a whole film.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import uaf_lib as uaf  # noqa: E402


def load_shots(path):
    data = uaf.load_json(path)
    if isinstance(data, dict):
        shots = data.get("shots")
        if shots is None:
            raise SystemExit(f"{path}: no 'shots' array found")
        return list(shots)
    if isinstance(data, list):
        return data
    raise SystemExit(f"{path}: expected an array of shots or an object with 'shots'")


def known_ids_for(shots_path, shots):
    """Collect canon ids from a sibling continuity ledger or the shots themselves."""
    known = set()
    for shot in shots:
        for reference in shot.get("reference_assets") or []:
            known.add(str(reference))
    ledger = Path(shots_path).resolve().parent / "continuity.json"
    if ledger.is_file():
        try:
            known |= uaf.canon_ids_from_ledger(uaf.load_json(ledger))
        except (ValueError, OSError):
            pass
    return known


def compile_shot(shot, which="both"):
    blocks = {}
    if which in ("image", "both"):
        blocks["image"] = uaf.compile_image_prompt(shot)
    if which in ("video", "both"):
        blocks["video"] = uaf.compile_video_prompt(shot)
    return blocks


def render(shot, blocks, show_risk=False):
    lines = [f"# {shot.get('id', '<unnamed>')} — {shot.get('story_purpose', '')}".rstrip()]
    for label, text in blocks.items():
        lines.append(f"\n## {label} prompt\n")
        lines.append("```text")
        lines.append(text)
        lines.append("```")
    if show_risk:
        risk = uaf.score_risk(shot)
        lines.append(f"\nrisk: {risk['risk_level']} ({risk['total']}/12) budget {risk['suggested_attempt_budget']}")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("shots", help="path to shots.json (or project.json)")
    parser.add_argument("--shot", action="append", default=[], help="shot id to compile (repeatable)")
    parser.add_argument("--format", choices=("image", "video", "both"), default="both")
    parser.add_argument("--lint", action="store_true", help="only lint; do not print prompts")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    parser.add_argument("--write", metavar="DIR", help="write one markdown file per shot into DIR")
    parser.add_argument("--risk", action="store_true", help="include risk scoring")
    args = parser.parse_args(argv)

    shots = load_shots(args.shots)
    wanted = set(args.shot)
    selected = [shot for shot in shots if not wanted or str(shot.get("id")) in wanted]
    if not selected:
        raise SystemExit("no shots selected")

    known = known_ids_for(args.shots, shots)
    findings = []
    payload = {}
    for shot in selected:
        shot_id = str(shot.get("id", "<unnamed>"))
        blocks = compile_shot(shot, args.format)
        for label, text in blocks.items():
            findings.extend(uaf.lint_prompt(f"{shot_id}:{label}", text, shot, known))
        payload[shot_id] = blocks
        if args.write:
            out_dir = Path(args.write)
            out_dir.mkdir(parents=True, exist_ok=True)
            uaf.write_text(out_dir / f"{shot_id}.md", render(shot, blocks, args.risk) + "\n")

    if args.json:
        print(json.dumps({"prompts": payload, "lint": findings}, indent=2))
    elif args.lint:
        print(f"linting {len(selected)} shot(s)")
        uaf.print_findings(findings) if findings else print("  no lint findings")
    else:
        blocks_out = []
        for shot in selected:
            blocks_out.append(render(shot, compile_shot(shot, args.format), args.risk))
        print("\n\n---\n\n".join(blocks_out))
        if findings:
            print("\n## lint findings\n")
            uaf.print_findings(findings)

    if args.write and not args.json:
        print(f"\nwrote {len(selected)} file(s) to {args.write}")

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
