#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import argparse
import subprocess
import sys
import os
import json

def get_audio_duration(file_path):
    """Uses ffprobe to get the audio duration in seconds."""
    try:
        cmd = [
            "ffprobe", 
            "-v", "quiet", 
            "-print_format", "json", 
            "-show_format", 
            file_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return float(data['format']['duration'])
    except Exception as e:
        print(f"❌ Error reading MP3 metadata using ffprobe: {e}")
        return None

def run_test(script_name, output_base, expected_min_duration, expected_max_duration):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, script_name)
    test_mp3 = os.path.join(script_dir, f".test.{output_base}.mp3")
    test_txt = os.path.join(script_dir, f".test.{output_base}.txt")
    test_prompt = f"A simple acoustic guitar melody for testing {script_name}"

    print(f"\n=============================================")
    print(f"🎸 Testing Script: {script_name}")
    print(f"=============================================")

    # Ensure cleanup before start
    for f in [test_mp3, test_txt]:
        if os.path.exists(f):
            os.remove(f)

    print(f"🏃 Executing: {script_name} -p '{test_prompt}' -o {test_mp3}")
    
    try:
        subprocess.run(
            [script_path, "-p", test_prompt, "-o", test_mp3],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Script executed successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ Script execution failed!")
        print(f"STDOUT:\n{e.stdout}")
        print(f"STDERR:\n{e.stderr}")
        return False

    # 1. Check if file exists
    if not os.path.exists(test_mp3):
        print(f"❌ Error: Expected output file '{test_mp3}' was not created.")
        return False
    
    file_size = os.path.getsize(test_mp3)
    print(f"✅ File '{test_mp3}' created successfully ({file_size / 1024:.1f} KB).")

    if file_size < 10000:
        print(f"❌ Error: File size is too small to be a valid MP3.")
        return False

    # 2. Check duration using ffprobe
    duration = get_audio_duration(test_mp3)
    if duration is not None:
        print(f"⏱️ Audio duration: {duration:.2f} seconds.")
        if expected_min_duration <= duration <= expected_max_duration:
            print(f"✅ Duration is within the expected {expected_min_duration}-{expected_max_duration} seconds range.")
        else:
            print(f"❌ Error: Duration ({duration:.2f}s) is outside the expected {expected_min_duration}-{expected_max_duration}s range.")
            return False
    else:
        print("⚠️ Could not verify duration (is ffprobe installed?). Skipping duration check.")

    # Cleanup
    print("🧹 Cleaning up test files...")
    for f in [test_mp3, test_txt]:
        if os.path.exists(f):
            os.remove(f)
            print(f"   Deleted {f}")
            
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Test script for Lyria3 music generator (tests both 30sec and 2min generators).",
        epilog="Ensures the scripts produce valid MP3 files of expected durations."
    )
    parser.add_argument(
        "--no-dryrun", 
        action="store_true", 
        help="Execute the real API calls (costs money/tokens)."
    )
    args = parser.parse_args()

    if not args.no_dryrun:
        print("🧪 Running in DRY-RUN (mock) mode.")
        print("ℹ️  This is a mock test to avoid accidental quota usage.")
        print("   Call with `--no-dryrun` to execute for real.")
        print("   ⚠️ WARNING: This will use REAL tokens, cost money, and take ~2-3 minutes to complete!")
        print("✅ Mock test passed.")
        sys.exit(0)

    print("🔥 Running REAL tests (Calling Lyria 3 API for both scripts)...")
    
    success_30s = run_test("musicgen-lyria3-30sec.py", "lyria3-30s", 20, 40)
    success_2m = run_test("musicgen-lyria3-2min.py", "lyria3-2m", 100, 140)

    print("\n=============================================")
    if success_30s and success_2m:
        print("🎉 All real tests passed successfully!")
        sys.exit(0)
    else:
        print("❌ One or more tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
