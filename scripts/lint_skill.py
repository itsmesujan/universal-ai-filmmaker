#!/usr/bin/env python3
"""Lint the skill package itself: structure, front matter, links, docs, manifest.

Usage:
    python scripts/lint_skill.py
    python scripts/lint_skill.py --json

Exit code 1 means the package is broken (missing files, invalid front matter, broken
references, or a stale MANIFEST.json), so CI can gate on it.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import manifest  # noqa: E402
import uaf_lib as uaf  # noqa: E402

REQUIRED_FILES = (
    "SKILL.md",
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "MANIFEST.json",
    "docs/README.md",
    "references/intent-routing.md",
    "references/workflow.md",
    "references/qc.md",
    "schemas/project.schema.json",
    "schemas/shots.schema.json",
    "templates/project.json",
    "examples/mini-project/project.json",
    "evals/README.md",
)

REQUIRED_DIRS = (
    "references",
    "templates",
    "schemas",
    "model-adapters",
    "examples",
    "docs",
    "scripts",
    "evals",
)

REPO_PATH_RE = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|json|jsonl|yml|yaml|py|txt))`")

PLACEHOLDER_RE = re.compile(r"\b(TODO|FIXME|TBD)\b")


def check_required(errors, warnings):
    for relative in REQUIRED_FILES:
        if not (uaf.REPO_ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")
    for relative in REQUIRED_DIRS:
        if not (uaf.REPO_ROOT / relative).is_dir():
            errors.append(f"missing required directory: {relative}")


def check_front_matter(errors, warnings):
    skill = uaf.REPO_ROOT / "SKILL.md"
    if not skill.is_file():
        return
    text = skill.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        errors.append("SKILL.md: missing YAML front matter")
        return
    try:
        end = lines.index("---", 1)
    except ValueError:
        errors.append("SKILL.md: front matter is not closed")
        return
    front = lines[1:end]

    name = next((line.split(":", 1)[1].strip() for line in front if line.startswith("name:")), None)
    description = next(
        (line.split(":", 1)[1].strip() for line in front if line.startswith("description:")), None
    )
    if name != "universal-ai-filmmaker":
        errors.append(f"SKILL.md: name must be 'universal-ai-filmmaker' (found {name!r})")
    if not description:
        errors.append("SKILL.md: description is required")
    elif len(description) > 1024:
        errors.append(f"SKILL.md: description is {len(description)} chars (max 1024)")
    if not any(line.startswith("license:") for line in front):
        warnings.append("SKILL.md: no license field in front matter")
    if not any(line.strip().startswith("version:") for line in front):
        warnings.append("SKILL.md: no metadata.version in front matter")
    if len(front) > 12:
        warnings.append("SKILL.md: front matter is longer than expected")


def check_referenced_paths(errors):
    """Backticked repo paths (those with a directory part) must resolve.

    A bare filename such as ``shots.json`` is a *project artifact produced upstream*, not a
    repository path, so only directory-qualified references are checked. Relative
    references are resolved against both the repository root and the referring file.
    """
    roots = [
        uaf.REPO_ROOT / "SKILL.md",
        uaf.REPO_ROOT / "README.md",
        uaf.REPO_ROOT / "CONTRIBUTING.md",
        uaf.REPO_ROOT / "evals" / "README.md",
    ]
    roots.extend(sorted((uaf.REPO_ROOT / "references").glob("*.md")))
    roots.extend(sorted((uaf.REPO_ROOT / "docs").glob("*.md")))
    for path in roots:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for candidate in REPO_PATH_RE.findall(text):
            if candidate.startswith(("http", "www")) or "*" in candidate:
                continue
            if "/" not in candidate:
                continue
            if (uaf.REPO_ROOT / candidate).exists() or (path.parent / candidate).exists():
                continue
            errors.append(
                f"{path.relative_to(uaf.REPO_ROOT).as_posix()}: broken path reference {candidate!r}"
            )


def check_markdown_links(errors):
    link_re = re.compile(r"\[[^\]]+\]\((?!https?:)([^)#]+)(?:#[^)]*)?\)")
    for path in sorted((uaf.REPO_ROOT / "docs").glob("*.md")) + [uaf.REPO_ROOT / "README.md"]:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for target in link_re.findall(text):
            target = target.strip()
            if not target or target.startswith("mailto:"):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{path.relative_to(uaf.REPO_ROOT).as_posix()}: broken link {target!r}")


def check_manifest(errors, warnings):
    if not manifest.MANIFEST_PATH.is_file():
        errors.append("MANIFEST.json is missing; run python scripts/manifest.py")
        return
    existing = json.loads(manifest.MANIFEST_PATH.read_text(encoding="utf-8"))
    added, removed, changed = manifest.diff_entries(existing.get("files", []), manifest.build_entries())
    if added or removed or changed:
        errors.append(
            "MANIFEST.json is stale "
            f"(added={len(added)}, removed={len(removed)}, changed={len(changed)}); "
            "run python scripts/manifest.py"
        )
    listed = {entry["path"] for entry in existing.get("files", [])}
    for name in ("SKILL.md", "README.md", "docs/README.md"):
        if name not in listed:
            errors.append(f"MANIFEST.json does not list {name}")


def check_docs_index(errors, warnings):
    index = uaf.REPO_ROOT / "docs" / "README.md"
    if not index.is_file():
        return
    text = index.read_text(encoding="utf-8")
    for path in sorted((uaf.REPO_ROOT / "docs").glob("*.md")):
        if path.name == "README.md":
            continue
        if path.name not in text:
            errors.append(f"docs/README.md does not link {path.name}")
    for path in sorted((uaf.REPO_ROOT / "references").glob("*.md")):
        if path.name not in text:
            warnings.append(f"docs/README.md does not index references/{path.name}")


def check_json(errors):
    for path in uaf.iter_repo_files():
        if path.suffix != ".json":
            continue
        text = path.read_text(encoding="utf-8")
        if "{{" in text:
            # Template placeholder, not a valid instance by design.
            continue
        try:
            json.loads(text)
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(uaf.REPO_ROOT).as_posix()}: invalid JSON ({exc})")


def check_placeholders(errors, warnings):
    for path in sorted((uaf.REPO_ROOT / "references").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if PLACEHOLDER_RE.search(text):
            warnings.append(f"{path.relative_to(uaf.REPO_ROOT).as_posix()}: contains TODO/FIXME/TBD")


def check_line_endings(errors, warnings):
    """Report CRLF in the working tree without failing the package.

    Working-tree line endings are cosmetic: ``.gitattributes`` normalises on commit,
    ``manifest.py`` hashes LF-normalised bytes, and Linux checkouts are LF. Contributors
    on Windows with ``core.autocrlf=true`` legitimately see CRLF, so this is a warning
    that nudges them to align, not an error that blocks them.
    """
    crlf_files = [
        path.relative_to(uaf.REPO_ROOT).as_posix()
        for path in uaf.iter_repo_files()
        if b"\r\n" in path.read_bytes()
    ]
    if crlf_files:
        warnings.append(
            f"{len(crlf_files)} file(s) use CRLF in the working tree "
            f"(e.g. {crlf_files[0]}); harmless, but `git add --renormalize .` or "
            "`git config core.autocrlf input` keeps it LF like the repository"
        )


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    errors, warnings = [], []
    check_required(errors, warnings)
    check_front_matter(errors, warnings)
    check_referenced_paths(errors)
    check_markdown_links(errors)
    check_manifest(errors, warnings)
    check_docs_index(errors, warnings)
    check_json(errors)
    check_placeholders(errors, warnings)
    check_line_endings(errors, warnings)

    if args.json:
        print(json.dumps({"errors": errors, "warnings": warnings, "ok": not errors}, indent=2))
    else:
        if warnings:
            print(f"WARNINGS ({len(warnings)})")
            uaf.print_findings(warnings)
        if errors:
            print(f"ERRORS ({len(errors)})")
            uaf.print_findings(errors)
        print(f"\nskill lint: {len(errors)} errors, {len(warnings)} warnings")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
