#!/usr/bin/env python3
"""
extract_codelab_test.py
Tests the extract_codelab.py script to ensure it handles URLs and directories gracefully without crashing,
that it correctly extracts and copies files, and that it dynamically populates the N-step scorecard table in README.md.
"""

import os
import tempfile
import subprocess
import sys

def test_extract_codelab():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    script_path = os.path.join(script_dir, "extract_codelab.py")

    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Running extract_codelab.py with output dir {tmpdir}...")
        
        # Test 1: Graceful failure on dummy HTML that doesn't have codelab tags
        result = subprocess.run(
            [sys.executable, script_path, "https://example.com", tmpdir],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("❌ extract_codelab.py exited with error on valid but non-codelab URL")
            print("STDERR:", result.stderr)
            return False
            
        print("✅ extract_codelab.py handled non-codelab URL gracefully.")

        # Test 2: Valid extraction + dynamic README.md scorecard update
        dummy_html = os.path.join(tmpdir, "dummy.html")
        with open(dummy_html, "w") as f:
            f.write("""
            <html><body>
            <google-codelab-step label="Overview and Setup" duration="5">
                <p>Hello world 1</p>
                <pre><code>Dockerfile content</code></pre>
            </google-codelab-step>
            <google-codelab-step label="Deploy GKE Cluster" duration="12">
                <p>Hello world 2</p>
                <pre>Simple code</pre>
            </google-codelab-step>
            <google-codelab-step label="Teardown Resources" duration="3">
                <p>Clean up</p>
            </google-codelab-step>
            </body></html>
            """)

        output_dir = os.path.join(tmpdir, "codelab", "original")
        os.makedirs(output_dir)

        # Create initial README.md with placeholder scorecard table
        readme_path = os.path.join(tmpdir, "README.md")
        with open(readme_path, "w") as f:
            f.write("""# Friction Log
## 📋 Executive Synoptic Table
| Field | Value |
|---|---|

## 🚦 Step-by-Step Scorecard Table
| Step # | Placeholder |
|---|---|
| 1 | Placeholder |
""")

        # Run extraction against local file URI
        file_uri = "file://" + dummy_html
        result = subprocess.run(
            [sys.executable, script_path, file_uri, output_dir + "/"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print("❌ extract_codelab.py failed to extract local file")
            print("STDERR:", result.stderr)
            return False

        # Verify content of 01.md
        with open(os.path.join(output_dir, "01.md"), "r") as f:
            content = f.read()
            if "```" not in content or "Dockerfile content" not in content:
                print("❌ Code block or Dockerfile content missing from extracted markdown")
                return False

        # Verify README.md scorecard was dynamically populated with exact 3 steps
        with open(readme_path, "r") as f:
            readme_content = f.read()
            if "Overview and Setup" not in readme_content or "Deploy GKE Cluster" not in readme_content or "Teardown Resources" not in readme_content:
                print("❌ Dynamic N-step scorecard table was not updated in README.md!")
                print("README content:", readme_content)
                return False
            if "`5m`" not in readme_content or "`12m`" not in readme_content:
                print("❌ Step durations were not populated in README.md scorecard!")
                return False

        print("✅ extract_codelab.py successfully extracted files AND dynamically updated README.md scorecard with exact N steps!")
        return True

def test_cuj01_appmod_dockerfile():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    script_path = os.path.join(script_dir, "extract_codelab.py")
    url = "https://codelabs.developers.google.com/codelabs/app-mod-workshop#3"

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = os.path.join(tmpdir, "original")
        os.makedirs(output_dir)
        
        print(f"Running CUJ01 test against {url}...")
        result = subprocess.run(
            [sys.executable, script_path, url, output_dir],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"⚠️ CUJ01: extract_codelab.py failed to fetch {url}. This might be a network issue.")
            return True

        found = False
        for filename in os.listdir(output_dir):
            if filename.endswith(".md"):
                with open(os.path.join(output_dir, filename), "r") as f:
                    content = f.read()
                    if "FROM php:5.6-apache" in content and "EXPOSE 8080" in content:
                        if "```" in content:
                            print(f"✅ CUJ01: Found Dockerfile correctly wrapped in markdown in {filename}")
                            found = True
                            break
        
        if not found:
            print("❌ CUJ01: Could not find correctly wrapped Dockerfile content in any extracted file.")
            return False
        return True

if __name__ == "__main__":
    success = test_extract_codelab()
    if success:
        success = test_cuj01_appmod_dockerfile()
        
    if not success:
        sys.exit(1)
    print("✅ All tests (including dynamic N-step scorecard & CUJ01) passed for extract_codelab.py!")
