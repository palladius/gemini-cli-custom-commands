#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "google-genai",
# ]
# ///

import os
import sys
import argparse
from google import genai
from google.genai import types

__version__ = "0.0.7"

'''
Lyria 3 Music Generation Script
-------------------------------
This script generates 30-second music clips using Google's Lyria 3 model.

Changelog:
- 0.0.7: Improved API key handling by checking GOOGLE_GENAI_API_KEY and GEMINI_API_KEY environment variables.
- 0.0.6: Added safety filter handling with descriptive errors for LLM prompt redesign.
- 0.0.5: Added 2-minute full-song generator support using lyria-3-pro-preview and renamed script to musicgen-lyria3-30sec.py.
- 0.0.4: Added colorful emojis directly to STDOUT reporting for a cleaner UI output.
- 0.0.3: Requires prompt, prints suggestions if empty, and saves generated lyrics/metadata to a matching .txt file.
- 0.0.2: Added argparse with --prompt and --output-file flags. Auto-append .mp3 extension. Update shebang to uv and add PEP 723 metadata.
- 0.0.1: Initial basic script with hardcoded prompt.
'''

def main():
    parser = argparse.ArgumentParser(
        description="Generate 30-second Lyria 3 music clips using Google GenAI.",
        epilog="Example usage: ./musicgen-lyria3-30sec.py --prompt \"A fast-paced EDM track with heavy bass\""
    )
    parser.add_argument(
        "-p", "--prompt", 
        type=str, 
        default=None, 
        help="The text prompt describing the music you want the AI to generate."
    )
    parser.add_argument(
        "-o", "--output-file", 
        type=str, 
        default="clip.mp3", 
        help="The filename to save the generated audio to. Defaults to clip.mp3."
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()

    if not args.prompt:
        print("❌ Error: The script will not generate anything without a prompt.")
        print("\nTry using one of these prompts:")
        print("  ./musicgen-lyria3-30sec.py -p \"A fast-paced EDM track with heavy bass\"")
        print("  ./musicgen-lyria3-30sec.py -p \"Cinematic orchestral trailer music with thundering drums and sweeping strings\"")
        sys.exit(1)

    output_filename = args.output_file
    if not output_filename.endswith(".mp3"):
        output_filename += ".mp3"

    api_key = os.environ.get('GOOGLE_GENAI_API_KEY') or os.environ.get('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)

    print(f"🎸 Generating music for prompt: \033[36m'{args.prompt}'\033[0m...")
    try:
        response = client.models.generate_content(
            model="lyria-3-clip-preview",
            contents=args.prompt,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO", "TEXT"],
            ),
        )

        # Handle safety filters / blocked content
        if response.prompt_feedback and response.prompt_feedback.block_reason:
            print(f"❌ Error: The request was blocked by the safety filter. Reason: {response.prompt_feedback.block_reason}")
            print("💡 HINT for AI Agent: This prompt triggers a safety filter (likely due to names of people or protected terms).")
            print("💡 ACTION: Please redesign the prompt using more generic terms (e.g., 'a hero' instead of a name) and try again.")
            if response.prompt_feedback.block_reason_message:
                print(f"   Message: {response.prompt_feedback.block_reason_message}")
            return

        # Parse the response
        text_content = ""
        found_audio = False
        
        if not response.candidates or not response.candidates[0].content.parts:
            print("⚠️ No content was returned in the response candidates.")
            return

        for part in response.candidates[0].content.parts:
            if part.text is not None:
                text_content += part.text + "\n"
            elif part.inline_data is not None:
                with open(output_filename, "wb") as f:
                    f.write(part.inline_data.data)
                print(f"🎵 Audio saved to \033[32m{output_filename}\033[0m")
                found_audio = True

        if text_content.strip():
            text_filename = output_filename[:-4] + ".txt"
            with open(text_filename, "w") as f:
                f.write(text_content.strip() + "\n")
            print(f"📝 Lyrics and metadata saved to \033[34m{text_filename}\033[0m")
        
        if not found_audio:
            print("⚠️ No audio was generated in the response.")

    except Exception as e:
        print(f"❌ Error generating music: {str(e)}")

if __name__ == "__main__":
    main()
