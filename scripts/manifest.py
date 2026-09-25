#!/usr/bin/env python3
"""Regenerate MANIFEST.json with a sha256 hash and byte size per repository file.

Usage:
    python scripts/manifest.py            # rewrite MANIFEST.json
    python scripts/manifest.py --check    # verify the manifest is current (exit 1 if stale)

MANIFEST.json deliberately does not list itself: a file cannot contain its own hash
without a fixed-point iteration, and listing a stale self-hash is worse than omitting it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import uaf_lib as uaf  # noqa: E402

MANIFEST_PATH = uaf.REPO_ROOT / "MANIFEST.json"
EXCLUDED_NAMES = {"MANIFEST.json"}


def _normalized_bytes(path):
    """Read a file with line endings normalised to LF.

    Line endings must not affect the manifest: the same file checked out on Windows
    (CRLF) and Linux (LF) has to produce the same hash, otherwise ``manifest.py --check``
    passes locally and fails in CI (or the reverse). Files in this repository are small
    text artifacts, so a whole-file read is deliberate and safe.
    """
    data = path.read_bytes()
    if b"\r" not in data:
        return data
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha256_of(path):
    digest = hashlib.sha256()
    digest.update(_normalized_bytes(path))
    return digest.hexdigest()


def size_of(path):
    """Byte size after LF normalisation, so sizes match across platforms."""
    return len(_normalized_bytes(path))


def build_entries(root=None):
    root = Path(root or uaf.REPO_ROOT)
    entries = []
    for path in uaf.iter_repo_files(root):
        if path.name in EXCLUDED_NAMES:
            continue
        relative = path.relative_to(root).as_posix()
        entries.append(
            {
                "path": relative,
                "sha256": sha256_of(path),
                "bytes": size_of(path),
            }
        )
    return sorted(entries, key=lambda entry: entry["path"])


def build_manifest(version, root=None):
    return {
        "repository": "universal-ai-filmmaker",
        "version": version,
        "generated_by": "scripts/manifest.py",
        "hash_scheme": "sha256 of LF-normalised bytes",
        "note": "MANIFEST.json is not self-listed; regenerate with scripts/manifest.py.",
        "files": build_entries(root),
    }


def read_version():
    """Read metadata.version from SKILL.md front matter, falling back to 1.1.0."""
    skill = uaf.REPO_ROOT / "SKILL.md"
    if skill.is_file():
        for line in skill.read_text(encoding="utf-8").splitlines()[:12]:
            stripped = line.strip()
            if stripped.startswith("version:"):
                return stripped.split(":", 1)[1].strip().strip('"').strip("'")
    return "1.1.0"


def diff_entries(existing, current):
    old = {entry["path"]: entry for entry in existing}
    new = {entry["path"]: entry for entry in current}
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    changed = sorted(
        path for path in set(old) & set(new) if old[path].get("sha256") != new[path].get("sha256")
    )
    return added, removed, changed


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--check", action="store_true", help="verify instead of writing")
    parser.add_argument("--version", default=None, help="override the manifest version")
    parser.add_argument("--root", default=None, help="repository root (defaults to the repo)")
    args = parser.parse_args(argv)

    version = args.version or read_version()
    entries = build_entries(args.root)

    if args.check:
        if not MANIFEST_PATH.is_file():
            print("manifest: MANIFEST.json is missing")
            return 1
        existing = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        added, removed, changed = diff_entries(existing.get("files", []), entries)
        if not (added or removed or changed):
            print(f"manifest: up to date ({len(entries)} files)")
            return 0
        print("manifest: STALE")
        for label, items in (("added", added), ("removed", removed), ("changed", changed)):
            if items:
                print(f"  {label}: {', '.join(items[:10])}{' …' if len(items) > 10 else ''}")
        print("  run: python scripts/manifest.py")
        return 1

    manifest = build_manifest(version, args.root)
    uaf.dump_json(manifest, MANIFEST_PATH)
    total_bytes = sum(entry["bytes"] for entry in manifest["files"])
    print(f"manifest: wrote {len(manifest['files'])} entries ({total_bytes} bytes) as version {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
