#!/bin/bash
# setup_scaffold_test.sh
# Tests the setup_scaffold.sh script to ensure it creates all expected directories and files.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
cd "$SCRIPT_DIR"

TEST_DIR="TEST_SCAFFOLD_DIR_$$"

echo "Running test for setup_scaffold.sh..."
./setup_scaffold.sh "$TEST_DIR"

if [ $? -ne 0 ]; then
  echo "❌ setup_scaffold.sh exited with an error."
  exit 1
fi

# Check if directories exist
for dir in "codelab/original" "codelab/proposed" "FRICTION_LOG" "external-repos"; do
  if [ ! -d "$TEST_DIR/$dir" ]; then
    echo "❌ Missing directory: $dir"
    exit 1
  fi
done

# Check if files exist
for file in "external-repos/.gitignore" ".env" "BUGS.md" ".version"; do
  if [ ! -f "$TEST_DIR/$file" ]; then
    echo "❌ Missing file: $file"
    exit 1
  fi
done

# Check version file content
if ! grep -q "Find me in https://github.com/palladius/gemini-cli-custom-commands" "$TEST_DIR/.version"; then
  echo "❌ .version file does not contain expected text."
  exit 1
fi

# Check .env file content
if ! grep -q "PROJECT_ID=" "$TEST_DIR/.env" || ! grep -q "GEMINI_API_KEY=" "$TEST_DIR/.env" || ! grep -q "REGION=" "$TEST_DIR/.env"; then
  echo "❌ .env file does not contain expected skeleton variables (including REGION)."
  exit 1
fi

echo "✅ All tests passed for setup_scaffold.sh!"
rm -rf "$TEST_DIR"
exit 0
