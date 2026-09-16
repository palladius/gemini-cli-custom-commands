---
name: musicgen-lyria3
description: Generate 30-second music clips (default) or 2-3 minute full songs with the Lyria 3.5 model family from Google GenAI. Supports creating music with lyrics, vocals, and specific genres from text prompts. Automatically saves matching lyrics (.txt) in the same directory.
metadata:
  version: 0.0.13
compatibility: Gemini CLI
---

# Musicgen Lyria 3.5

## Overview

Generate 30-second clips or full-length songs with Google's Lyria 3.5 family via the Gemini Interactions API (44.1 kHz stereo audio, structural coherence, vocals, and lyrics).

## Models & Scripts

| Model | Model ID | Best for | Duration | Bundled Script |
| :--- | :--- | :--- | :--- | :--- |
| **Lyria 3 Clip** | `lyria-3-clip-preview` | Short clips, loops, previews | ⏱️ 30s | `scripts/musicgen-lyria3-30sec.py` (Default) |
| **Lyria 3.5** | `lyria-3.5` | Full songs (verses, choruses, bridges) | 🎵 2–3 min | `scripts/musicgen-lyria3-2min.py` |

- `scripts/musicgen-lyria3-list.py`: List available audio/music models.

## Storage Rules

- Output audio is saved as `<output_path>.mp3`.
- **MANDATORY**: Lyrics and metadata MUST ALWAYS be saved in the **exact same folder** as the audio file with the **exact same base name** (e.g., `assets/song_v2.mp3` ➔ `assets/song_v2.txt`).

## Example Usage

```bash
# 30-sec clip (Default)
uv run scripts/musicgen-lyria3-30sec.py -o "assets/music/clip" -p "A synth-pop song: 'Electrified, living for the night.'"

# Full song with Lyria 3.5
uv run scripts/musicgen-lyria3-2min.py -o "assets/music/song" -p "An energetic pop-rock anthem: 'Full lyrics here...'"
```

## Italian Phonetic Guidelines

AI singing models mispronounce unaccented Italian words. Always use explicit accents or spacing inline: `Nicòla` (not `Nicola`), `Mòdena`, `Dàvide`, `Cacio Cavallo` (spaced), `mattacchióne`, `energìa` (not `energià`), `tecnologìa`, `fantasìa`.
