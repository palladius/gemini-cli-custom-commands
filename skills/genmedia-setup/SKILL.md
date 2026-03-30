---
name: genmedia-setup
description: Install and setup Hussain Chinoy's GenMedia (MCP) tools and related Gemini skills. Use when you need to install the GenMedia Go binary, inject MCP configurations, or install the specialized Gemini skills (Producer, etc.) from the Vertex AI Creative Studio.
version: 0.0.2
# v0.0.2 - add optional --path-to-scripts argument to inject_settings.py and also made PATH work automagically.
# v0.0.1 - Initial Vibecoded while talking to Hussain Chinoy :)
---

# GenMedia Setup

This skill provides a three-step process for setting up the GenMedia environment, including configuring the MCP servers into your Gemini CLI.

## Step 1: Install the GenMedia Binary

Install the precompiled Go binaries for the GenMedia toolset:

```bash
bash scripts/install-genmedia.sh
```

## Step 2: Install Gemini Skills

Once the binary is installed, you can install the associated Gemini skills.

### Option A: Install All Skills
To install all skills in the GenMedia directory:

```bash
gemini skills install https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio.git --path experiments/mcp-genmedia/skills
```

### Option B: Install a Specific Skill
To install a specific skill (e.g., the Producer skill):

```bash
gemini skills install https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio.git --path experiments/mcp-genmedia/skills/genmedia-producer
```

When in doubt, install ALL of them.

This will install the binaries in `~/.local/bin/`

## Step 3: Configure MCP Settings (JSON Injector)

To automatically inject the required `mcpServers` (like `mcp-veo-go`, `mcp-imagen-go`) into your `~/.gemini/settings.json`, run the injection script.

You only *strictly* need your Google Cloud Project ID. 
- If a Bucket Name is not provided, the script creates `gs://<YOUR_PROJECT_ID>-mediagen-files`.
- If a Region is not provided, the script defaults to `us-central1`.
- The MCP binaries paths default to `~/.local/bin/`. You can override this using `--path-to-scripts`.

Run the injector script:

```bash
# Minimal required execution (defaults apply)
python3 scripts/inject_settings.py --project <YOUR_PROJECT_ID>

# Specify custom bucket, region, and bin path
python3 scripts/inject_settings.py --project <YOUR_PROJECT_ID> --bucket <YOUR_BUCKET_NAME> --region us-central1 --path-to-scripts ~/.local/bin
```

> **Note:** If you prefer to add them manually, a reference configuration block is provided in `references/sample_settings.json`.

## Testinf the installation

Let's start with something cheap and fast:

* **Prompt**: Use chirp3-hd MCP server to list voices in "en-US" language.

Note this should use the MCP server defined in your settings.json, pointing to the script  `PROJECT_ID=XXXXX ~/.local/bin/mcp-chirp3-go`. Ensure ~/.local/bin/ is added to your PATH before running Gemini CLI again.

## Credits

- Hussain Chinoy for the [mcp-genmedia-go](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/tree/main/experiments/mcp-genmedia/mcp-genmedia-go) project.
