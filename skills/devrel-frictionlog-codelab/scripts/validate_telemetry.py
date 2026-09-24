#!/usr/bin/env python3
"""validate_telemetry.py — Validates and autofills devrel.google.com/v2alpha1 FrictionLogRun telemetry.

Validates that a friction_log.json or friction_log.yaml file contains all mandatory fields.
If mandatory fields are missing or empty:
  - If --autofill is specified, fills them with explicit 'UNKNOWN' or safe default values and writes back.
  - If --strict is specified (or by default without --autofill), exits with code 1 and reports all missing fields.

Usage:
  ./validate_telemetry.py <path/to/friction_log.json|yaml> [--autofill] [--strict]
"""

import sys
import os
import json
from datetime import datetime, timezone

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# Mandatory fields hierarchy: (dot_path, default_value, expected_type)
MANDATORY_FIELDS = [
    ("apiVersion", "devrel.google.com/v2alpha1", str),
    ("kind", "FrictionLogRun", str),
    ("metadata.iteration_id", "UNKNOWN_ITERATION", str),
    ("metadata.name", "unknown-codelab-run", str),
    ("metadata.started_at", datetime.now(timezone.utc).isoformat(), str),
    ("metadata.overall_status", "UNKNOWN", str),
    ("environment.git.commit_sha", "unknown", str),
    ("environment.git.commit_timestamp", "unknown", str),
    ("environment.git.branch", "unknown", str),
    ("environment.ai_runner.harness", "Antigravity", str),
    ("environment.ai_runner.model", "unknown-model", str),
    ("environment.gcp.project_id", "unknown-project", str),
    ("human_intervention.prompts_exchanged", 0, int),
    ("human_intervention.manual_unblocks_count", 0, int),
    ("human_intervention.summary", "No human intervention details recorded.", str),
    ("steps", [], list),
]

def get_nested(d, dot_path):
    keys = dot_path.split(".")
    curr = d
    for k in keys:
        if not isinstance(curr, dict) or k not in curr:
            return None
        curr = curr[k]
    return curr

def set_nested(d, dot_path, val):
    keys = dot_path.split(".")
    curr = d
    for k in keys[:-1]:
        if k not in curr or not isinstance(curr[k], dict):
            curr[k] = {}
        curr = curr[k]
    curr[keys[-1]] = val

def load_telemetry(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    if file_path.endswith((".yaml", ".yml")):
        if not HAS_YAML:
            raise RuntimeError("PyYAML not installed. Cannot parse YAML.")
        data = yaml.safe_load(content)
    else:
        data = json.loads(content)
    return data or {}

def save_telemetry(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        if file_path.endswith((".yaml", ".yml")):
            if not HAS_YAML:
                raise RuntimeError("PyYAML not installed. Cannot write YAML.")
            yaml.dump(data, f, sort_keys=False, default_flow_style=False)
        else:
            json.dump(data, f, indent=2)
            f.write("\n")

def validate_and_autofill(data, autofill=False):
    missing = []
    autofilled = []

    for dot_path, default_val, exp_type in MANDATORY_FIELDS:
        val = get_nested(data, dot_path)
        is_missing = val is None or (isinstance(val, str) and not val.strip())

        if is_missing:
            if autofill:
                set_nested(data, dot_path, default_val)
                autofilled.append((dot_path, default_val))
            else:
                missing.append(dot_path)
        else:
            # Type check
            if exp_type == int and not isinstance(val, int):
                try:
                    int_val = int(val)
                    if autofill:
                        set_nested(data, dot_path, int_val)
                except (ValueError, TypeError):
                    missing.append(f"{dot_path} (expected integer, got {type(val).__name__})")
            elif exp_type == list and not isinstance(val, list):
                missing.append(f"{dot_path} (expected list, got {type(val).__name__})")

    # Step validation if steps exist
    steps = data.get("steps")
    if isinstance(steps, list):
        for idx, step in enumerate(steps):
            if not isinstance(step, dict):
                continue
            for step_key, default_s_val in [
                ("step_number", idx),
                ("title", f"Step {idx}"),
                ("status", "UNKNOWN"),
                ("tweet_checkpoint", "Tweet checkpoint not recorded.")
            ]:
                if step_key not in step or step[step_key] is None or (isinstance(step[step_key], str) and not step[step_key].strip()):
                    if autofill:
                        step[step_key] = default_s_val
                        autofilled.append((f"steps[{idx}].{step_key}", default_s_val))
                    else:
                        missing.append(f"steps[{idx}].{step_key}")

    return missing, autofilled

def main():
    if len(sys.argv) < 2:
        print("Usage: ./validate_telemetry.py <path/to/friction_log.json|yaml> [--autofill] [--strict]")
        sys.exit(2)

    file_path = sys.argv[1]
    autofill = "--autofill" in sys.argv
    strict = "--strict" in sys.argv

    if not os.path.exists(file_path):
        print(f"❌ Error: File not found at {file_path}")
        sys.exit(1)

    try:
        data = load_telemetry(file_path)
    except Exception as e:
        print(f"❌ Error loading telemetry from {file_path}: {e}")
        sys.exit(1)

    missing, autofilled = validate_and_autofill(data, autofill=autofill)

    if autofilled:
        print(f"⚠️  Autofilled {len(autofilled)} missing mandatory fields with defaults:")
        for path, val in autofilled:
            print(f"   + {path} = {val!r}")
        save_telemetry(file_path, data)
        print(f"💾 Updated file saved to {file_path}")

    if missing:
        print(f"❌ Validation FAILED — {len(missing)} mandatory fields missing or invalid:")
        for path in missing:
            print(f"   - {path}")
        print("\n👉 To auto-populate missing fields with defaults, run with --autofill.")
        sys.exit(1)

    print(f"✅ Telemetry validation SUCCESS: All mandatory fields present and valid in {file_path}!")
    sys.exit(0)

if __name__ == "__main__":
    main()
