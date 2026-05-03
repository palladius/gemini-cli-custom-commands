---
name: musicgen-lyria3
description: Generate 30-second music clips (default) or 2-3 minute full songs with the Lyria 3 model from Google GenAI. Supports creating music with lyrics, vocals, and specific genres from text prompts. Now includes metadata/lyrics saving and custom output filenames.
metadata:
  version: 0.0.5
compatibility: Gemini CLI
---

# Musicgen Lyria3

## Overview

This skill enables the generation of high-quality 30-second music previews (default) or full-length 2-3 minute songs using Google's Lyria 3 model via the GenAI SDK. It can produce music in various genres, including tracks with vocals and specific lyrics provided in the text prompt.

## Core Capability

The skill utilizes bundled Python scripts:

- `scripts/musicgen-lyria3-30sec.py` (Default): Interacts with the `lyria-3-clip-preview` model for 30-second clips.
- `scripts/musicgen-lyria3-2min.py`: Interacts with the `lyria-3-pro-preview` model for full-length 2-3 minute songs.

### Workflow

1. **Understand the Request**: Identify if the user wants music, a song, or an audio clip based on a description.
2. **Formulate a Prompt**: Ensure the prompt includes genre, mood, instruments, and any specific lyrics or vocal styles requested.
3. **Execute Generation**: Run the script using `uv run` or `python` (if dependencies are met).
4. **Confirm Output**:
    - The script saves the resulting audio as `clip.mp3` (default) or a custom filename.
    - **New**: Lyrics and metadata are automatically saved to a matching `.txt` file (e.g., `clip.txt`).

### Example Usage

```bash
# Basic 30-sec generation (Default)
uv run scripts/musicgen-lyria3-30sec.py --prompt "A high-energy synth-pop song with female vocals"

# Custom output filename and specific lyrics (30-sec)
uv run scripts/musicgen-lyria3-30sec.py -o "neon-lights" -p "A synth-pop song with these lyrics: 'Electrified, we're living for the night, under neon lights so bright.'"

# Generate a full-length 2-3 minute song
uv run scripts/musicgen-lyria3-2min.py --prompt "An epic cinematic orchestral piece about a journey home, building through sweeping strings."
```

## Guidance for Prompts

To achieve the best results with Lyria 3, be as descriptive as possible:

- **Style & Genre**: "90s grunge", "lo-fi hip hop", "cinematic orchestral".
- **Tempo & Mood**: "120 BPM energetic", "slow and atmospheric".
- **Instruments**: "synthesizers", "distorted guitar", "pounding drums".
- **Vocals & Lyrics**: Explicitly state if vocals are needed and provide the lyrics in quotes.

## Resources

- `scripts/musicgen-lyria3-30sec.py` & `scripts/musicgen-lyria3-2min.py`: The Python scripts that perform the generation using `google-genai`.
