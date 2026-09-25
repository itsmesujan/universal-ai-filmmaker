"""Shared helpers for the Universal AI Filmmaker tooling.

Standard library only. Python 3.9+.

Contains:
  * ``load_json`` / ``dump_json`` helpers with UTF-8 handling
  * a small JSON Schema validator covering the subset used by ``schemas/``
  * canonical asset id helpers
  * prompt compilation and linting for SHOT_SPEC records
  * shot risk scoring
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO_ROOT / "schemas"

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".mypy_cache", "projects"}

CANON_ID_RE = re.compile(r"^(character|location|prop|style|voice|keyframe):[a-z0-9-]+:v[0-9]+$")

RISK_ATTEMPT_BUDGET = {"low": 2, "medium": 4, "high": 8, "critical": 12}

RISK_LEVELS = ("low", "medium", "high", "critical")

FAILURE_CLASSES = (
    "IDENTITY",
    "STYLE",
    "ANATOMY",
    "MOTION",
    "CAMERA",
    "COMPOSITION",
    "PHYSICS",
    "LIGHTING",
    "BACKGROUND",
    "OBJECTS",
    "TEXT",
    "AUDIO",
    "TEMPORAL",
    "CONTINUITY",
    "TOOL_ERROR",
)


# --------------------------------------------------------------------------- io


def load_json(path):
    """Load a UTF-8 JSON file."""
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(data, path, indent=2):
    """Write UTF-8 JSON with LF line endings and a trailing newline.

    ``newline="\\n"`` is required on Windows: default text mode would emit CRLF, which
    then looks like trailing whitespace to ``git diff --check`` and would fight
    ``.gitattributes`` (``eol=lf``).
    """
    write_text(path, json.dumps(data, indent=indent, ensure_ascii=False) + "\n")


def write_text(path, text):
    """Write UTF-8 text with LF line endings regardless of platform."""
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def iter_repo_files(root=None):
    """Yield repository files, skipping VCS/vendored directories."""
    root = Path(root or REPO_ROOT)
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


# --------------------------------------------------------------------- validation


class SchemaError(Exception):
    """Raised when a JSON Schema cannot be used by the mini validator."""


def _type_matches(value, expected):
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    raise SchemaError(f"unsupported type keyword: {expected}")


def _resolve_ref(ref, root):
    if not ref.startswith("#/"):
        raise SchemaError(f"only local $ref is supported: {ref}")
    node = root
    for token in ref[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict) or token not in node:
            raise SchemaError(f"unresolvable $ref: {ref}")
        node = node[token]
    return node


def _check(value, schema, root, path, errors):
    if not isinstance(schema, dict):
        return

    if "$ref" in schema:
        _check(value, _resolve_ref(schema["$ref"], root), root, path, errors)

    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}")

    if "enum" in schema and value not in schema["enum"]:
        allowed = ", ".join(repr(item) for item in schema["enum"][:8])
        errors.append(f"{path}: {value!r} not in enum [{allowed}]")

    types = schema.get("type")
    if types is not None:
        candidates = types if isinstance(types, list) else [types]
        if not any(_type_matches(value, candidate) for candidate in candidates):
            errors.append(f"{path}: expected type {'/'.join(candidates)}, got {type(value).__name__}")
            return

    if isinstance(value, str):
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: {value!r} does not match pattern {schema['pattern']}")
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path}: shorter than minLength {schema['minLength']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path}: longer than maxLength {schema['maxLength']}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: {value} below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: {value} above maximum {schema['maximum']}")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: fewer than minItems {schema['minItems']}")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: more than maxItems {schema['maxItems']}")
        items = schema.get("items")
        if isinstance(items, dict):
            for index, item in enumerate(value):
                _check(item, items, root, f"{path}[{index}]", errors)

    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing required property {key!r}")
        properties = schema.get("properties", {})
        for key, subschema in properties.items():
            if key in value:
                _check(value[key], subschema, root, f"{path}.{key}", errors)
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(f"{path}: unexpected property {key!r}")

    for keyword in ("anyOf", "oneOf"):
        if keyword in schema:
            hits = 0
            for branch in schema[keyword]:
                probe = []
                _check(value, branch, root, path, probe)
                if not probe:
                    hits += 1
            if keyword == "anyOf" and hits == 0:
                errors.append(f"{path}: does not satisfy anyOf")
            if keyword == "oneOf" and hits != 1:
                errors.append(f"{path}: satisfied {hits} oneOf branches, expected exactly 1")


def validate_instance(instance, schema):
    """Return a list of human-readable validation errors (empty when valid)."""
    errors = []
    _check(instance, schema, schema, "$", errors)
    return errors


def load_schema(name):
    """Load ``schemas/<name>.schema.json``."""
    stem = name[:-12] if name.endswith(".schema.json") else name
    return load_json(SCHEMA_DIR / f"{stem}.schema.json")


def detect_schema_name(path, data):
    """Best-effort mapping from a project file to a bundled schema name."""
    name = path.name.lower()
    hints = (
        ("adapter", "model-adapter"),
        ("continuity", "continuity"),
        ("beats", "beats"),
        ("beat", "beats"),
        ("qc", "qc"),
        ("shot", "shots"),
        ("project", "project"),
    )
    for token, schema in hints:
        if token in name:
            return schema

    if isinstance(data, list):
        if data and isinstance(data[0], dict):
            if "beat_id" in data[0]:
                return "beats"
            if "primary_action" in data[0]:
                return "shots"
        return None
    if isinstance(data, dict):
        if {"provider", "model", "verified_at"} <= set(data):
            return "model-adapter"
        if "project_id" in data and "shots" in data:
            return "project"
        if "characters" in data and "schema_version" in data:
            return "continuity"
        if "final_decision" in data or ("shots" in data and "reviewer" in data):
            return "qc"
    return None


# ------------------------------------------------------------------- canon ids


def is_canon_id(value):
    """True when ``value`` is a versioned canonical asset id."""
    return bool(CANON_ID_RE.match(str(value)))


def canon_kind(value):
    """Return the asset kind (``character``/``location``/...) or ``None``."""
    return str(value).split(":", 1)[0] if is_canon_id(value) else None


# ------------------------------------------------------------------ risk model


def _string_values(node, out):
    """Collect only string *values* from a nested structure (never dict keys)."""
    if isinstance(node, dict):
        for value in node.values():
            _string_values(value, out)
    elif isinstance(node, list):
        for item in node:
            _string_values(item, out)
    elif isinstance(node, str):
        out.append(node)
    return out


def score_risk(shot):
    """Score a SHOT_SPEC's risk from 0-12 using the documented axes."""
    axes = {
        "subject_complexity": 0,
        "motion_complexity": 0,
        "continuity_dependency": 0,
        "duration": 0,
        "physics_effects": 0,
        "text_hands_faces": 0,
    }

    subject = str(shot.get("subject", "")).lower()
    if any(word in subject for word in ("crowd", "army", "audience", "group", "swarm")):
        axes["subject_complexity"] = 2
    elif any(word in subject for word in (" and ", "two ", "three ", "pair", "child", "dog", "cat")):
        axes["subject_complexity"] = 1

    action = str(shot.get("primary_action", "")).lower()
    if any(word in action for word in ("fight", "collide", "impact", "explode", "dance", "wrestl")):
        axes["motion_complexity"] = 2
    elif any(word in action for word in ("walk", "run", "turn", "reach", "open", "lift", "lower")):
        axes["motion_complexity"] = 1

    references = shot.get("reference_assets") or []
    if len(references) >= 3:
        axes["continuity_dependency"] = 2
    elif references:
        axes["continuity_dependency"] = 1

    try:
        duration = float(shot.get("duration_target", 0))
    except (TypeError, ValueError):
        duration = 0.0
    if duration >= 10:
        axes["duration"] = 2
    elif duration >= 6:
        axes["duration"] = 1

    environment = " ".join(_string_values(shot.get("environment", {}), [])).lower()
    if any(word in environment for word in ("explosion", "storm", "fire", "flood", "earthquake")):
        axes["physics_effects"] = 2
    elif any(word in environment for word in ("rain", "smoke", "dust", "wind", "snow")):
        axes["physics_effects"] = 1

    blob = " ".join(_string_values(shot, [])).lower()
    has_text = "text" in blob or "sign" in blob or "screen" in blob
    has_hands = "hand" in blob or "holding" in blob
    has_face = "face" in blob or "eyes" in blob or "expression" in blob
    axes["text_hands_faces"] = min(2, int(has_text) + int(has_hands and has_face))

    total = sum(axes.values())
    if total <= 3:
        level = "low"
    elif total <= 6:
        level = "medium"
    elif total <= 9:
        level = "high"
    else:
        level = "critical"

    return {
        "axes": axes,
        "total": total,
        "risk_level": level,
        "suggested_attempt_budget": RISK_ATTEMPT_BUDGET[level],
    }


# ------------------------------------------------------------------- prompting


def _camera_text(camera):
    parts = []
    if camera.get("type"):
        parts.append(str(camera["type"]).replace("_", " "))
    if camera.get("lens_equivalent"):
        parts.append(f"{camera['lens_equivalent']} lens")
    if camera.get("position"):
        parts.append(str(camera["position"]).replace("_", " "))
    if camera.get("movement_speed"):
        parts.append(f"{camera['movement_speed']} speed")
    if camera.get("stabilization"):
        parts.append(str(camera["stabilization"]).replace("_", " "))
    return ", ".join(parts)


def _composition_text(composition):
    parts = []
    if composition.get("framing"):
        parts.append(str(composition["framing"]).replace("_", " "))
    if composition.get("angle"):
        parts.append(str(composition["angle"]).replace("_", " "))
    if composition.get("subject_position"):
        parts.append(f"subject {composition['subject_position']}")
    if composition.get("screen_direction"):
        direction = str(composition["screen_direction"])
        parts.append(
            f"moving {direction}" if direction.startswith("moving") else f"screen direction {direction}"
        )
    if composition.get("headroom"):
        parts.append(f"headroom {composition['headroom']}")
    return ", ".join(parts)


def _lighting_text(lighting):
    parts = []
    if lighting.get("direction"):
        parts.append(f"key from {lighting['direction']}")
    if lighting.get("key"):
        parts.append(str(lighting["key"]))
    if lighting.get("quality"):
        parts.append(str(lighting["quality"]))
    if lighting.get("ratio"):
        parts.append(f"{lighting['ratio']} contrast")
    if lighting.get("temperature"):
        parts.append(str(lighting["temperature"]))
    if lighting.get("rim"):
        parts.append(f"rim {lighting['rim']}")
    if lighting.get("practicals"):
        value = lighting["practicals"]
        parts.append(str(value) if isinstance(value, str) else "practicals " + ", ".join(map(str, value)))
    return ", ".join(parts)


def _environment_text(environment):
    parts = []
    for key in ("location_id", "time", "weather", "dressing"):
        if environment.get(key):
            parts.append(str(environment[key]).replace("_", " "))
    return ", ".join(parts)


def _style_text(style):
    parts = []
    if style.get("mode"):
        parts.append(f"{style['mode']} mode")
    if style.get("rendering"):
        parts.append(str(style["rendering"]))
    if style.get("style_lock_ref"):
        parts.append(str(style["style_lock_ref"]))
    return ", ".join(parts)


def _continuity_text(continuity):
    parts = []
    for key in sorted(continuity):
        value = continuity[key]
        if isinstance(value, (str, int, float)) and str(value).strip():
            parts.append(f"{key.replace('_', ' ')} {value}")
    return ", ".join(parts)


def _performance_text(performance):
    parts = []
    for key in ("behaviour", "beat_stage", "emotion_start", "emotion_end"):
        if performance.get(key):
            parts.append(str(performance[key]))
    return ", ".join(parts)


def _timing_text(timing):
    preferred = ("pacing", "holds", "speed")
    parts = [f"{key} {timing[key]}" for key in preferred if timing.get(key)]
    if not parts:
        parts = [f"{key} {timing[key]}" for key in sorted(timing)]
    return ", ".join(parts)


def compile_image_prompt(shot):
    """Compile the neutral image prompt for a SHOT_SPEC."""
    blocks = [
        ("SUBJECT", str(shot.get("subject", "")).strip()),
        ("APPEARANCE", ", ".join(str(item) for item in (shot.get("reference_assets") or []))),
        ("POSE", str(shot.get("start_state", "")).strip()),
        ("ACTION", str(shot.get("primary_action", "")).strip()),
        ("COMPOSITION", _composition_text(shot.get("composition") or {})),
        ("ENVIRONMENT", _environment_text(shot.get("environment") or {})),
        ("LIGHTING", _lighting_text(shot.get("lighting") or {})),
        ("CAMERA", _camera_text(shot.get("camera") or {})),
        ("STYLE", _style_text(shot.get("style") or {})),
        ("PERFORMANCE", _performance_text(shot.get("performance") or {})),
        ("CONTINUITY", _continuity_text(shot.get("continuity") or {})),
        ("CONSTRAINTS", ", ".join(str(item) for item in (shot.get("negative_constraints") or []))),
    ]
    return "\n".join(f"{label}: {text}" for label, text in blocks if text)


def compile_video_prompt(shot):
    """Compile the neutral video prompt for a SHOT_SPEC."""
    audio = shot.get("audio") or {}
    audio_text = ", ".join(f"{key} {audio[key]}" for key in sorted(audio) if str(audio[key]).strip())
    blocks = [
        ("START STATE", str(shot.get("start_state", "")).strip()),
        ("SUBJECT MOTION", str(shot.get("primary_action", "")).strip()),
        ("SECONDARY MOTION", str(shot.get("secondary_motion", "")).strip()),
        ("CAMERA MOTION", _camera_text(shot.get("camera") or {})),
        ("PERFORMANCE", _performance_text(shot.get("performance") or {})),
        ("TIMING", _timing_text(shot.get("timing") or {})),
        ("END STATE", str(shot.get("end_state", "")).strip()),
        ("CONTINUITY", _continuity_text(shot.get("continuity") or {})),
        ("AUDIO", audio_text),
        ("CONSTRAINTS", ", ".join(str(item) for item in (shot.get("negative_constraints") or []))),
    ]
    return "\n".join(f"{label}: {text}" for label, text in blocks if text)


PROVIDER_SYNTAX_TOKENS = ("--ar", "--motion", "--seed", "--stylize", "cfg_scale", "num_frames")

QUALITY_SPAM = ("4k", "8k", "masterpiece", "best quality", "ultra detailed", "hyperrealistic")

ABSTRACT_EMOTION = ("is sad", "is happy", "is angry", "is nervous", "is scared", "feels ")


def lint_prompt(shot_id, prompt, shot, known_ids=None):
    """Return a list of lint findings for a compiled prompt."""
    findings = []
    lowered = prompt.lower()

    if not prompt.strip():
        findings.append(f"{shot_id}: empty prompt")

    for token in PROVIDER_SYNTAX_TOKENS:
        if token in lowered:
            findings.append(f"{shot_id}: provider syntax {token!r} in a neutral prompt")

    for phrase in QUALITY_SPAM:
        if phrase in lowered:
            findings.append(f"{shot_id}: quality spam {phrase!r}")

    for phrase in ABSTRACT_EMOTION:
        if phrase in lowered:
            findings.append(f"{shot_id}: abstract emotion {phrase!r} without observable behaviour")

    known = set(known_ids or [])
    for reference in shot.get("reference_assets") or []:
        if not is_canon_id(reference):
            findings.append(f"{shot_id}: reference {reference!r} is not a versioned canon id")
        elif known and str(reference) not in known:
            findings.append(f"{shot_id}: reference {reference!r} not found in bibles/ledger")

    action = str(shot.get("primary_action", ""))
    if len(action.split(" and ")) > 2:
        findings.append(f"{shot_id}: primary_action reads as multiple actions")

    lines = [line for line in prompt.splitlines() if line.strip()]
    labels = [line.split(":", 1)[0] for line in lines]
    for label in sorted({label for label in labels if labels.count(label) > 1}):
        findings.append(f"{shot_id}: duplicate prompt block {label!r}")

    return findings


def shot_ids_from(shots):
    return {str(shot.get("id")) for shot in shots if isinstance(shot, dict) and shot.get("id")}


def canon_ids_from_ledger(ledger):
    ids = set()
    for key in ("characters", "locations", "props"):
        for entry in ledger.get(key) or []:
            if isinstance(entry, dict) and entry.get("id"):
                ids.add(str(entry["id"]))
    return ids


def print_findings(findings, prefix="  "):
    for finding in findings:
        print(f"{prefix}{finding}")
