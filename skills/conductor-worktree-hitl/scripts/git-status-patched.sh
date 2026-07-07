#!/bin/bash
# Code User Manual:
# Wrapper script to execute git_status_patched.py.
# Ensure you are running this from the repository root.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/git_status_patched.py" "$@"
