# Changelog

## [0.1.0] - 2026-09-18
- 🏷️✨ Auto-embed ID3v2.3 tags into generated MP3s:
  - 📜 **Lyrics**: Stored in `USLT` frame and mirrored in `COMM` comment frame for 100% media player compatibility.
  - 👤 **Artist Avatar**: Embedded the official **Drake Riccardo Clean NO** meme (`assets/drake_riccardo_artist_default.png`) as `APIC` Type 8 (Artist/performer).
  - 🎵 **Metadata**: Title (auto-cleaned from filename), Artist (`Riccardo C feat. Google Lyria 3`), Album, Year (`2026`), and `TXXX:AI_TOOL`.
  - 🎛️ **CLI Flags**: Added `--title`, `--artist`, `--album`, `--cover`, `--artist-image` to both `musicgen-lyria3-30sec.py` and `musicgen-lyria3-2min.py`.

## [0.0.9] - 2026-05-30
- ✨ Added generated music and text files for Seby 6 anni. (-- made with Gemini CLI by gc-skillume-bot-v0_2)

## [0.0.8] - 2026-05-19
- ✨ Added generated music and text files for Sebi (lido estensi, hot wheels). (-- made with Gemini CLI by gc-skillume-bot-v0_2)

## [0.0.7] - 2026-04-21
- Improved API key handling by checking `GOOGLE_GENAI_API_KEY` and `GEMINI_API_KEY` environment variables.

## [0.0.6] - 2026-04-15
- Added safety filter handling with descriptive errors for LLM prompt redesign.

## [0.0.5] - 2026-03-29
- Added 2-minute full-song generator support using `lyria-3-pro-preview` model.
- Renamed default 30-sec script to `musicgen-lyria3-30sec.py`.
- Updated `SKILL.md` to document the option for longer tracks.

## [0.0.4] - 2026-03-27
- Added colorful emojis directly to STDOUT reporting for a cleaner UI output.

## [0.0.3] - 2026-03-27
- Requires prompt, prints suggestions if empty, and saves generated lyrics/metadata to a matching `.txt` file.

## [0.0.2] - 2026-03-27
- Added `argparse` with `--prompt` and `--output-file` flags.
- Auto-append `.mp3` extension.
- Update shebang to use `uv` and add PEP 723 metadata.

## [0.0.1] - 2026-03-27
- Initial basic script with hardcoded prompt.
