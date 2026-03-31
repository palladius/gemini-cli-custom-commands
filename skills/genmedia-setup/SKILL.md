---
name: genmedia-setup
description: Install and setup GenMedia (MCP) tools and related Gemini skills. Use when you need to install the GenMedia Go binary, inject MCP configurations, or install the specialized Gemini skills (Producer, etc.) from the Vertex AI Creative Studio.
version: 0.0.3
---

# GenMedia Setup

This skill provides a three-step process for setting up the GenMedia environment, including configuring the MCP servers into your Gemini CLI.

## Prerequisites (MANDATORY)

Before running the setup, ensure you have the following requirements:

1. **FFmpeg & FFprobe**: Required for media manipulation (e.g. `mcp-avtool-go`).
   ```bash
   sudo apt update && sudo apt install -y ffmpeg
   ```
2. **Application Default Credentials (ADC)**: The MCP servers use ADC for authentication.
   ```bash
   gcloud auth application-default login
   ```

## Step 1: Install the GenMedia Binary

Install the precompiled Go binaries for the GenMedia toolset:

```bash
bash scripts/install-genmedia.sh
```

## Step 2: Install Gemini Skills

Once the binary is installed, you can install the associated Gemini skills.

### Option A: Install All Skills
```bash
gemini skills install https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio.git --path experiments/mcp-genmedia/skills
```

### Option B: Install a Specific Skill
```bash
gemini skills install https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio.git --path experiments/mcp-genmedia/skills/genmedia-producer
```

### Configuration and Model References

For a full list of recommended models for each service, refer to [which_models.md](./references/which_models.md).

To automatically inject the required `mcpServers` into your `~/.gemini/settings.json`, run the injection script.

The script will automatically:
- Enable required Google Cloud APIs (`Vertex AI`, `Text-to-Speech`, `Storage`).
- Create a GCS bucket if it doesn't exist.
- Inject server configurations with absolute binary paths.

Run the injector script (only `PROJECT_ID` is mandatory):

```bash
# Minimal required execution (defaults apply)
python3 scripts/inject_settings.py --project <YOUR_PROJECT_ID>

# Specify custom bucket, region, and bin path
python3 scripts/inject_settings.py --project <YOUR_PROJECT_ID> --bucket <YOUR_BUCKET_NAME> --region us-central1 --path-to-scripts ~/.local/bin
```

### Important: Storage Permissions
Ensure your account has permissions to use the bucket:
```bash
gcloud storage buckets add-iam-policy-binding gs://<YOUR_BUCKET_NAME> \
  --member=user:<YOUR_EMAIL> \
  --role=roles/storage.objectUser
```

## Testing

* **Prompt**: Use chirp3 MCP server to list available voices. If this works, then generate a short audio clip with "it works!".
* **Prompt**: Use veo MCP server to generate a short video clip with a flying donkey singing: "it works!".
* **Prompt**: Show me the content of the GENMEDIA_BUCKET.

## Credits

- Hussain Chinoy for the [mcp-genmedia-go](https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/tree/main/experiments/mcp-genmedia/mcp-genmedia-go) project.
