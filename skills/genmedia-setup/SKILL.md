---
name: genmedia-setup
description: Install, setup and use GenMedia (MCP) tools and related Gemini skills.
version: 0.1.1
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

### 1. The Four-Act Structure

When creating a storyboard, follow this structure to ensure a compelling narrative:

*   **Act I: The Setup (30-45s)**: Introduce characters and the world. Establish the conflict.
*   **Act II: Rising Action (1-2m)**: The characters face obstacles. The stakes increase.
*   **Act III: The Climax (30-45s)**: The highest point of tension. The conflict is resolved.
*   **Act IV: Resolution (30s)**: Show the aftermath and the new status quo.

### 2. Characters & Style Continuity

- **Style**: Define a consistent visual and narrative style (e.g., "Pixar-style animation", "Noir cinematography"). Retain this style across all scenes.
- **Characters**: Describe characters vividly. Use reference images and consistent prompts to maintain character continuity across scenes.

### 3. Scene Generation (3-5 Scenes per Act)

For each act, generate detailed scene descriptions:
- **Visuals**: Use Imagen (Imagen 3 or 4) for high-quality scene visuals.
- **Music**: Use Lyria (002 or 3) to generate a matching soundtrack for each scene.
- **Video**: Use Veo to animate scenes, typically in 5-8 second clips.

### 4. Audio & Voiceover

- **Speech**: Use Chirp (2 or 3) for multi-lingual narration or character voices.
- **Sanitization**: Remove markdown characters (`#`, `*`) from text before speech generation to ensure natural delivery.

---

## 🧪 Testing Your Setup

* **Prompt**: Use chirp3 MCP server to list available voices. If this works, then generate a short audio clip with "it works!".
* **Prompt**: Use veo MCP server to generate a short video clip with a flying donkey singing: "it works!".
* **Prompt**: Show me the content of the GENMEDIA_BUCKET.

## 📜 History & Credits

- See [Skill Changelog](./CHANGELOG.md) for version history.
- Credits: Hussain Chinoy for the GenMedia toolset.
