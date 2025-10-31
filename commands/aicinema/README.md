These commands are part of Riccardo's "AI Cinema" Demo Show around Europe in 2025,
built in collaboration with the amazing Hussain, maitainer of MCP Vertex AI GenMedia in golang.

Note that these commands will NOT WORK unless you pre-install MCP `go` packages in `~/go/bin`.

## INSTALL

1. Follow manual instructions in https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/blob/main/experiments/mcp-genmedia/README.md
2. Or simply ask Gemini: `gemini -p /aicinema:check_install Help me install GenMedia on this machine.`
3. Ensure to log in with `gcloud auth`. Note that the execution of the MCP server is authenticated when it's launched, and from Gemini CLI
   this happens at launch time. If you authenticate AFTER launching Gemini CLI, the MCP from this session will fail until you restart *GianCarlo*.

## About

Allow you to:

1. Check the installation is correct.
2. Create an audio story from a script.
3. Create a video storyboard from a script.

## Commands

-   `aicinema:audio_story`: Create an audio story from a script using GMP Assistant.
-   `aicinema:check_install`: Check if the GoLang installation was done correctly.
-   `aicinema:video_storyboard`: Create an audio/video story from a script using GenAI.

## Troubleshooting

* if MCP servers dont start, the most probable cause is gcloud auth: `just gcloud-auth`.
* If MCP bin cant be found -> check PATH: `export PATH=$PATH:~/go/bin`
* when everything works, BEFORE testing gemini cli, try this: `just chirp-io-amo-la-pizza`: it runs a chirp model to say a sentence in italian. If it works, it should generate a WAV file and print a JSON like:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Speech synthesized successfully with voice it-IT-Chirp3-HD-Zephyr. Audio saved to: chirp_audio-it-IT-Chirp3-HD-Zephyr-20251031-163404.wav (111404 bytes)."
      }
    ]
  }
}
```

## Notes

These prompts were moved on 20251031 (spooky!) from https://github.com/palladius/gemini-cli-demos/ (under `demos/mcp-video-creation/.gemini/commands`).
