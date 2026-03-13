#!/bin/bash
# setup_scaffold.sh
# Usage: ./setup_scaffold.sh <YYYYMMDD-frictionlog-CODELAB_TITLE>

if [ -z "$1" ]; then
  echo "Usage: $0 <YYYYMMDD-frictionlog-CODELAB_TITLE>"
  exit 1
fi

BASE_DIR="$1"

echo "Creating scaffold in $BASE_DIR..."

mkdir -p "$BASE_DIR/codelab/original"
mkdir -p "$BASE_DIR/codelab/proposed"
mkdir -p "$BASE_DIR/FRICTION_LOG"
mkdir -p "$BASE_DIR/external-repos"

echo "*" > "$BASE_DIR/external-repos/.gitignore"

# Attempt to load .env template from the skill's references folder
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
TEMPLATE_PATH="$SCRIPT_DIR/../references/env.template"

if [ -f "$TEMPLATE_PATH" ]; then
  cp "$TEMPLATE_PATH" "$BASE_DIR/.env"
else
  # Fallback if template is missing
  cat <<EOF > "$BASE_DIR/.env"
# This should be provided by user.
PROJECT_ID=

# this is very useful for Gemini API invocations. Can also be created with a bunch of gcloud scripts.
GEMINI_API_KEY=

# This is usually good enough for most people, 
# but feel free to localize to something close to the user.
GOOGLE_CLOUD_REGION="us-central1"

# Optional, in case a project is not given a BAID needs to be given
BILLING_ACCOUNT_ID=
EOF
fi

touch "$BASE_DIR/BUGS.md"

cat <<EOF > "$BASE_DIR/.version"
Created with skill devrel-frictionlog-codelab v0.0.3
Find me in https://github.com/palladius/gemini-cli-custom-commands
EOF

echo "✅ Scaffold created successfully in $BASE_DIR"
