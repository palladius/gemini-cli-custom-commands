#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "google-genai",
#     "mutagen",
# ]
# ///

import os
import sys
import argparse
import datetime
from google import genai
from google.genai import types
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TCON, USLT, COMM, APIC, TXXX, error

__version__ = "0.1.0"

'''
Lyria 3.5 Music Generation Script
---------------------------------
This script generates full-length songs using Google's Lyria 3.5 model,
and automatically embeds rich ID3 tags (lyrics in USLT/COMM, Artist avatar meme, metadata).

Changelog:
- 0.1.0: Added automatic ID3v2.3 tagging: embedded lyrics (USLT + COMM), custom artist meme cover (APIC), album and AI metadata.
- 0.0.9: Updated default model to lyria-3.5 (with --model flag support and fallback).
- 0.0.8: Fixed silent failure bug: script now exits with 1 if destination directory is missing or on any generation error.
- 0.0.7: Improved API key handling by checking GOOGLE_GENAI_API_KEY and GEMINI_API_KEY environment variables.
- 0.0.6: Added safety filter handling with descriptive errors for LLM prompt redesign.
- 0.0.5: Added 2-minute full-song generator support using lyria-3-pro-preview.
- 0.0.4: Added colorful emojis directly to STDOUT reporting for a cleaner UI output.
- 0.0.3: Requires prompt, prints suggestions if empty, and saves generated lyrics/metadata to a matching .txt file.
- 0.0.2: Added argparse with --prompt and --output-file flags. Auto-append .mp3 extension. Update shebang to uv and add PEP 723 metadata.
- 0.0.1: Initial basic script with hardcoded prompt.
'''

DEFAULT_ARTIST_IMAGE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets",
    "drake_riccardo_artist_default.png"
)

def embed_metadata(
    mp3_path: str,
    lyrics_text: str,
    title: str | None = None,
    artist: str = "Riccardo C feat. Google Lyria 3",
    album: str = "Lyria 3.5 Generated Albums",
    genre: str = "AI Music",
    cover_image: str | None = None,
    artist_image: str | None = None,
    model_name: str = "lyria-3.5"
):
    try:
        try:
            tags = ID3(mp3_path)
        except error:
            tags = ID3()

        if not title:
            base = os.path.splitext(os.path.basename(mp3_path))[0]
            title = base.replace("_", " ").replace("-", " ").title()

        tags.delall("TIT2")
        tags.add(TIT2(encoding=3, text=title))

        tags.delall("TPE1")
        tags.add(TPE1(encoding=3, text=artist))

        tags.delall("TALB")
        tags.add(TALB(encoding=3, text=album))

        year = str(datetime.datetime.now().year)
        tags.delall("TDRC")
        tags.add(TDRC(encoding=3, text=year))

        tags.delall("TCON")
        tags.add(TCON(encoding=3, text=genre))

        if lyrics_text and lyrics_text.strip():
            clean_lyrics = lyrics_text.strip()
            tags.delall("USLT")
            tags.add(USLT(encoding=3, lang="ita", desc="", text=clean_lyrics))

            tags.delall("COMM")
            comm_text = f"Generato con Google Lyria 3.5 ({model_name}). Artista: {artist}\n\nLYRICS / TESTO:\n{clean_lyrics}"
            tags.add(COMM(encoding=3, lang="ita", desc="", text=comm_text))

        tags.delall("TXXX:AI_TOOL")
        tags.add(TXXX(encoding=3, desc="AI_TOOL", text=f"Google Lyria 3.5 ({model_name})"))
        tags.delall("TXXX:CREATOR")
        tags.add(TXXX(encoding=3, desc="CREATOR", text=artist))

        # Cover image (Type 3: Front Cover)
        if cover_image and os.path.exists(cover_image):
            with open(cover_image, "rb") as f:
                cdata = f.read()
            mime = "image/png" if cover_image.lower().endswith(".png") else "image/jpeg"
            non_3 = [frame for frame in tags.getall("APIC") if frame.type != 3]
            tags.delall("APIC")
            for a in non_3:
                tags.add(a)
            tags.add(APIC(encoding=3, mime=mime, type=3, desc="Cover Art", data=cdata))

        # Artist picture (Type 8: Artist/performer)
        art_img = artist_image if (artist_image and os.path.exists(artist_image)) else DEFAULT_ARTIST_IMAGE
        if art_img and os.path.exists(art_img):
            with open(art_img, "rb") as f:
                adata = f.read()
            mime = "image/png" if art_img.lower().endswith(".png") else "image/jpeg"
            non_8 = [frame for frame in tags.getall("APIC") if frame.type != 8]
            tags.delall("APIC")
            for a in non_8:
                tags.add(a)
            tags.add(APIC(encoding=3, mime=mime, type=8, desc="Artist (Drake Riccardo Meme Clean)", data=adata))

        tags.save(mp3_path, v2_version=3)
        print(f"🏷️ ID3 metadata & lyrics embedded into: \033[32m{mp3_path}\033[0m")
    except Exception as ex:
        print(f"⚠️ Warning: Could not embed ID3 metadata: {ex}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate full-length Lyria 3.5 songs using Google GenAI with automatic ID3 tagging and lyrics.",
        epilog="Example usage: ./musicgen-lyria3-2min.py --prompt \"A fast-paced EDM track with heavy bass\""
    )
    parser.add_argument(
        "-p", "--prompt", 
        type=str, 
        default=None, 
        help="The text prompt describing the music you want the AI to generate."
    )
    parser.add_argument(
        "-m", "--model",
        type=str,
        default="lyria-3.5",
        help="The Lyria model to use (defaults to lyria-3.5)."
    )
    parser.add_argument(
        "-o", "--output-file", 
        type=str, 
        default="clip.mp3", 
        help="The filename to save the generated audio to. Defaults to clip.mp3."
    )
    parser.add_argument(
        "--title",
        type=str,
        default=None,
        help="Song title for ID3 tag (defaults to output filename without underscores)."
    )
    parser.add_argument(
        "--artist",
        type=str,
        default="Riccardo C feat. Google Lyria 3",
        help="Artist name for ID3 tag (defaults to 'Riccardo C feat. Google Lyria 3')."
    )
    parser.add_argument(
        "--album",
        type=str,
        default="Lyria 3.5 Generated Albums",
        help="Album name for ID3 tag."
    )
    parser.add_argument(
        "--cover",
        type=str,
        default=None,
        help="Path to cover art image (PNG/JPG) to embed as front cover."
    )
    parser.add_argument(
        "--artist-image",
        type=str,
        default=None,
        help="Path to custom artist image to embed (defaults to Drake Riccardo meme)."
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
        print("  ./musicgen-lyria3-2min.py -p \"A fast-paced EDM track with heavy bass\"")
        print("  ./musicgen-lyria3-2min.py -p \"Cinematic orchestral trailer music with thundering drums and sweeping strings\"")
        sys.exit(1)

    output_filename = args.output_file
    if not output_filename.endswith(".mp3"):
        output_filename += ".mp3"

    out_dir = os.path.dirname(output_filename)
    if out_dir and not os.path.exists(out_dir):
        print(f"❌ Error: Output directory does not exist: {out_dir}")
        sys.exit(1)

    api_key = os.environ.get('GOOGLE_GENAI_API_KEY') or os.environ.get('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)

    print(f"🎸 Generating music with model '{args.model}' for prompt: \033[36m'{args.prompt}'\033[0m...")
    try:
        response = client.models.generate_content(
            model=args.model,
            contents=args.prompt,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO", "TEXT"],
            ),
        )

        if response.prompt_feedback and response.prompt_feedback.block_reason:
            print(f"❌ Error: The request was blocked by the safety filter. Reason: {response.prompt_feedback.block_reason}")
            print("💡 HINT for AI Agent: This prompt triggers a safety filter (likely due to names of people or protected terms).")
            print("💡 ACTION: Please redesign the prompt using more generic terms (e.g., 'a hero' instead of a name) and try again.")
            if response.prompt_feedback.block_reason_message:
                print(f"   Message: {response.prompt_feedback.block_reason_message}")
            sys.exit(1)

        text_content = ""
        found_audio = False
        
        if not response.candidates or not response.candidates[0].content.parts:
            print("⚠️ No content was returned in the response candidates.")
            sys.exit(1)

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
            sys.exit(1)

        # Embed ID3 tags and lyrics
        embed_metadata(
            mp3_path=output_filename,
            lyrics_text=text_content,
            title=args.title,
            artist=args.artist,
            album=args.album,
            cover_image=args.cover,
            artist_image=args.artist_image,
            model_name=args.model
        )

    except Exception as e:
        print(f"❌ Error generating music: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
