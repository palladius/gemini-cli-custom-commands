# GenMedia Installation Guide

This guide covers the manual and automated installation of the GenMedia MCP toolset.

## Prerequisites (MANDATORY)

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

Alternatively, if you have Go installed, you can install them manually:
```bash
go install github.com/GoogleCloudPlatform/vertex-ai-creative-studio/experiments/mcp-genmedia/mcp-genmedia-go/mcp-veo-go@latest
# ... and so on for lyria, chirp3, imagen, avtool
```

## Step 2: Install Gemini Skills

Install the associated Gemini skills from the Vertex AI Creative Studio repository.

### Option A: Install All Skills
```bash
gemini skills install https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio.git --path experiments/mcp-genmedia/skills
```

### Option B: Install a Specific Skill
```bash
gemini skills install https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio.git --path experiments/mcp-genmedia/skills/genmedia-producer
```

## Step 3: Configure MCP Settings (JSON Injector)

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

### Storage Permissions
Ensure your account has permissions to use the bucket:
```bash
gcloud storage buckets add-iam-policy-binding gs://<YOUR_BUCKET_NAME> \
  --member=user:<YOUR_EMAIL> \
  --role=roles/storage.objectUser
```

## Troubleshooting

- **Auth Issues**: Ensure `gcloud auth application-default login` was successful.
- **Path Issues**: Ensure the binaries are in your `PATH` or the absolute paths in `settings.json` are correct.
- **API Errors**: Check if the required APIs (Vertex AI, TTS, Storage) are enabled on the specified project.
