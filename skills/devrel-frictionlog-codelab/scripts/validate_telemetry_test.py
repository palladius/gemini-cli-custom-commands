#!/usr/bin/env python3
"""validate_telemetry_test.py
Automated test suite verifying validate_telemetry.py strict validation,
autofill behavior, and JSON/YAML support.
"""

import os
import sys
import tempfile
import subprocess
import json
import yaml

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
VALIDATOR = os.path.join(SCRIPT_DIR, "validate_telemetry.py")

def test_full_valid_yaml():
    valid_data = {
        "apiVersion": "devrel.google.com/v2alpha1",
        "kind": "FrictionLogRun",
        "metadata": {
            "iteration_id": "20260924-fl101",
            "name": "rails8-on-google-cloud-fl101",
            "started_at": "2026-09-24T15:00:00Z",
            "overall_status": "GREEN"
        },
        "environment": {
            "git": {
                "commit_sha": "af8a83f",
                "commit_timestamp": "2026-09-24 14:39:37",
                "branch": "main"
            },
            "ai_runner": {
                "harness": "Antigravity",
                "model": "gemini-2.5-pro"
            },
            "skill": {
                "name": "devrel-frictionlog-codelab",
                "version": "0.3.2"
            },
            "gcp": {
                "project_id": "rails8-ws-fl101"
            }
        },
        "human_intervention": {
            "prompts_exchanged": 5,
            "manual_unblocks_count": 0,
            "summary": "Autonomous run"
        },
        "steps": [
            {
                "step_number": 0,
                "title": "Prerequisites",
                "status": "GREEN",
                "tweet_checkpoint": "Step 0 verified green"
            }
        ]
    }

    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
        yaml.dump(valid_data, f)
        path = f.name

    try:
        res = subprocess.run([sys.executable, VALIDATOR, path], capture_output=True, text=True)
        assert res.returncode == 0, f"Expected returncode 0, got {res.returncode}. Output:\n{res.stdout}\n{res.stderr}"
        assert "SUCCESS" in res.stdout
    finally:
        os.remove(path)
    print("✅ test_full_valid_yaml passed")

def test_missing_mandatory_fails_strict():
    sparse_data = {
        "metadata": {
            "iteration_id": "20260924-fl101"
        }
    }

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(sparse_data, f)
        path = f.name

    try:
        res = subprocess.run([sys.executable, VALIDATOR, path], capture_output=True, text=True)
        assert res.returncode == 1, f"Expected returncode 1, got {res.returncode}"
        assert "Validation FAILED" in res.stdout
        assert "environment.git.commit_sha" in res.stdout
        assert "environment.ai_runner.model" in res.stdout
    finally:
        os.remove(path)
    print("✅ test_missing_mandatory_fails_strict passed")

def test_autofill_recovers_missing_fields():
    sparse_data = {
        "metadata": {
            "iteration_id": "20260924-fl101"
        },
        "steps": [
            {"title": "Overview"}
        ]
    }

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(sparse_data, f)
        path = f.name

    try:
        # Run with --autofill
        res = subprocess.run([sys.executable, VALIDATOR, path, "--autofill"], capture_output=True, text=True)
        assert res.returncode == 0, f"Autofill failed: {res.stdout}\n{res.stderr}"
        assert "Autofilled" in res.stdout

        # Verify populated content
        with open(path) as f:
            updated = json.load(f)
        assert updated["apiVersion"] == "devrel.google.com/v2alpha1"
        assert updated["environment"]["git"]["commit_sha"] == "unknown"
        assert updated["environment"]["ai_runner"]["harness"] == "Antigravity"
        assert updated["human_intervention"]["prompts_exchanged"] == 0
        assert updated["steps"][0]["status"] == "UNKNOWN"

        # Now re-running without --autofill must pass cleanly
        res2 = subprocess.run([sys.executable, VALIDATOR, path], capture_output=True, text=True)
        assert res2.returncode == 0
        assert "SUCCESS" in res2.stdout
    finally:
        os.remove(path)
    print("✅ test_autofill_recovers_missing_fields passed")

if __name__ == "__main__":
    test_full_valid_yaml()
    test_missing_mandatory_fails_strict()
    test_autofill_recovers_missing_fields()
    print("\n🎉 ALL VALIDATOR TESTS PASSED!")
