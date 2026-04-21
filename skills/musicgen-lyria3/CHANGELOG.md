# Changelog

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
