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
touch "$BASE_DIR/.env"
touch "$BASE_DIR/BUGS.md"

cat <<EOF > "$BASE_DIR/.version"
Created with skill devrel-frictionlog-codelab v0.2.0
Find me in https://github.com/palladius/gemini-cli-custom-commands
EOF

echo "✅ Scaffold created successfully in $BASE_DIR"
