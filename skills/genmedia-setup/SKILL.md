---
name: genmedia-setup
description: Install, setup and use GenMedia (MCP) tools and related Gemini skills.
metadata:
  version: 0.1.2
compatibility: Gemini CLI
---

# GenMedia Setup & Usage

This skill guides you through setting up and using the GenMedia environment for AI-powered media production.

## 🛠️ Installation & Configuration

For initial setup, follow the [GenMedia Installation Guide](./references/install.md).

### Quick Reference
- **Inject Settings**: `python3 scripts/inject_settings.py --project <PROJECT_ID>`
- **Models**: See [Recommended Models](./references/which_models.md) for a list of supported models and regions.

---

## 🎬 Storyboarding & Production

Use the following guidelines to create high-quality, consistent media stories.

### 1. Project Organization (The Workflow)

Always organize your project into a dedicated folder: `stories/YYYYMMDD_HHMM_(title)/`.
- **PLAN.md**: Before generating assets, create a `PLAN.md` with checkboxes describing acts, scenes, and music. Check them off as you complete tasks.
- **README.md**: When finished, create a `README.md` that lists all generated assets, prompts used (for reproducibility), and any choices or errors encountered.
- **Error Tracking**: If you encounter persistent errors, log them in `doc/GENMEDIA_ERRORS.md`.

### 2. The Four-Act Structure

When creating a storyboard, follow this structure:
*   **Act I: The Setup (30-45s)**: Introduce characters and the world. Establish the conflict.
*   **Act II: Rising Action (1-2m)**: The characters face obstacles. The stakes increase.
*   **Act III: The Climax (30-45s)**: The highest point of tension. The conflict is resolved.
*   **Act IV: Resolution (30s)**: Show the aftermath and the new status quo.
*   **Trailer**: Finally, create an 8-second trailer with a dramatic "movie announcer" voice using Chirp and Veo.

### 3. Characters, Style & Personas

- **Style**: Define a consistent visual style (e.g., "Pixar-style animation", "Noir cinematography").
- **Personas**: If a character name matches a file in `doc/personas/*.md`, use that file's contents to inform the character's description and consistency.
- **Cover Image**: Generate a single `cover.png` for the story. If depicting children, use "Pixar style, 5-7 years old, blonde/blue eyes" (avoid "boy" if API filters trigger).

### 4. Scene Generation & Audio

- **Visuals/Music**: Generate 3-5 scenes per act with matching Imagen visuals and Lyria soundtracks.
- **Multi-lingual Support**: Use suffixes like `_en`, `_it`, `_de` for files (e.g., `story_it.txt`, `story_it.wav`, `story_it.md`).
- **Speech Sanitization**: **CRITICAL:** Remove markdown characters (`#`, `*`) from text before speech generation to ensure natural delivery.
- **File Naming**: Rename MCP-generated files (like `sample_0.mp4` or `chirp_audio_...wav`) to contextually relevant names to avoid overwrites.

---

## 🧪 Testing Your Setup

* **Prompt**: Use chirp3 MCP server to list available voices. If this works, then generate a short audio clip with "it works!".
* **Prompt**: Use veo MCP server to generate a short video clip with a flying donkey singing: "it works!".
* **Prompt**: Show me the content of the GENMEDIA_BUCKET.

## 📜 History & Credits

- See [Skill Changelog](./CHANGELOG.md) for version history.
- Credits: Hussain Chinoy for the GenMedia toolset.
