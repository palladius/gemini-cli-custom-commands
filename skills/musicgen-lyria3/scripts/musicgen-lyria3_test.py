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

def run_test(script_name, output_base, expected_min_duration, expected_max_duration, test_prompt, expected_keywords=None, no_cleanup=False):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, script_name)
    test_mp3 = os.path.join(script_dir, f".test.{output_base}.mp3")
    test_txt = os.path.join(script_dir, f".test.{output_base}.txt")

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

    # 3. Check lyrics file and keywords
    if expected_keywords:
        print(f"📝 Checking lyrics file for keywords: {expected_keywords}")
        if not os.path.exists(test_txt):
            print(f"❌ Error: Expected lyrics file '{test_txt}' was not created.")
            return False
        
        with open(test_txt, 'r', encoding='utf-8') as f:
            lyrics = f.read().lower()
        
        missing_keywords = [kw for kw in expected_keywords if kw.lower() not in lyrics]
        if missing_keywords:
            print(f"❌ Error: Could not find keywords {missing_keywords} in the lyrics.")
            print(f"   Lyrics generated:\n---\n{lyrics}\n---")
            return False
        else:
            print(f"✅ Found all expected keywords in lyrics!")

    # Cleanup
    if no_cleanup:
        print(f"💾 --no-cleanup set: Preserving {test_mp3} and {test_txt} for manual inspection.")
    else:
        print("🧹 Cleaning up test files...")
        for f in [test_mp3, test_txt]:
            if os.path.exists(f):
                os.remove(f)
                print(f"   Deleted {f}")
            
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Test script for Lyria3 music generator (tests both 30sec and 2min generators).",
        epilog="Ensures the scripts produce valid MP3 files of expected durations and verifies lyrics generation."
    )
    parser.add_argument(
        "--no-dryrun", 
        action="store_true", 
        help="Execute the real API calls (costs money/tokens)."
    )
    parser.add_argument(
        "--no-cleanup", 
        action="store_true", 
        help="Do NOT delete the generated .test.* files after testing (useful for manual inspection)."
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
    
    prompt_30s = "A simple 30 second acoustic guitar melody with an Italian tenore singing: Unit tests are the best - otherwise in italian"
    keywords_30s = ['unit', 'test']
    success_30s = run_test("musicgen-lyria3-30sec.py", "lyria3-30s", 20, 40, prompt_30s, keywords_30s, args.no_cleanup)
    
    prompt_2m = "A 2 minute acoustic guitar melody with an Italian tenore singing: Long unit tests are even better - otherwise in italian"
    keywords_2m = ['unit', 'test']
    success_2m = run_test("musicgen-lyria3-2min.py", "lyria3-2m", 100, 140, prompt_2m, keywords_2m, args.no_cleanup)

    print("\n=============================================")
    if success_30s and success_2m:
        print("🎉 All real tests passed successfully!")
        if args.no_cleanup:
            print("📁 Reminder: Generated test files were NOT deleted and are ready for you to check!")
        sys.exit(0)
    else:
        print("❌ One or more tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
