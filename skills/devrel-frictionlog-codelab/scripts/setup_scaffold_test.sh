#!/bin/bash
# setup_scaffold_test.sh
# Tests the setup_scaffold.sh script to ensure it creates all expected directories and files.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
cd "$SCRIPT_DIR"

TEST_DIR="TEST_SCAFFOLD_DIR_$$"
TEST_URL="https://example.com/codelab"
TEST_BUG="b/12345"
TEST_VER="v1.2.3"
TEST_GDOC="https://docs.google.com/document/d/mock-gdoc-id"

echo "Running test for setup_scaffold.sh..."
./setup_scaffold.sh "$TEST_DIR" "$TEST_URL" "$TEST_BUG" "$TEST_VER" "$TEST_GDOC"

if [ $? -ne 0 ]; then
  echo "❌ setup_scaffold.sh exited with an error."
  exit 1
fi

# Check if directories exist
for dir in "codelab/original" "codelab/proposed" "FRICTION_LOG" "friction_log/by-page" "workbench" "external-repos"; do
  if [ ! -d "$TEST_DIR/$dir" ]; then
    echo "❌ Missing directory: $dir"
    exit 1
  fi
done

# Check if files exist
for file in "external-repos/.gitignore" ".env" "BUGS.md" ".version" "friction_log.yaml"; do
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
if ! grep -q "PROJECT_ID=" "$TEST_DIR/.env" || ! grep -q "GEMINI_API_KEY=" "$TEST_DIR/.env"; then
  echo "❌ .env file does not contain expected skeleton variables."
  exit 1
fi

# Check friction_log.yaml file content
if ! grep -q "apiVersion: devrel.google.com/v1alpha1" "$TEST_DIR/friction_log.yaml" || \
   ! grep -q "kind: FrictionLog" "$TEST_DIR/friction_log.yaml" || \
   ! grep -q "name: $TEST_DIR" "$TEST_DIR/friction_log.yaml" || \
   ! grep -q "codelabUrl: \"$TEST_URL\"" "$TEST_DIR/friction_log.yaml" || \
   ! grep -q "codelabVersion: \"$TEST_VER\"" "$TEST_DIR/friction_log.yaml" || \
   ! grep -q "bugId: \"$TEST_BUG\"" "$TEST_DIR/friction_log.yaml" || \
   ! grep -q "startedAt:" "$TEST_DIR/friction_log.yaml" || \
   ! grep -q "outputGdocUrl: \"$TEST_GDOC\"" "$TEST_DIR/friction_log.yaml"; then
  echo "❌ friction_log.yaml does not contain expected k8s-like metadata and spec."
  cat "$TEST_DIR/friction_log.yaml"
  exit 1
fi

echo "✅ All tests passed for setup_scaffold.sh!"
rm -rf "$TEST_DIR"
exit 0
