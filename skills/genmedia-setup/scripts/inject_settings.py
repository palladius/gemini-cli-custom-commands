#!/usr/bin/env python3
"""
GenMedia MCP Setup Injector
This script injects the configuration for GenMedia MCP servers 
(veo, imagen, chirp3-hd, lyria, avtool) into the Gemini CLI settings.json.
"""

import argparse
import json
import os
import sys
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Inject GenMedia MCP servers into Gemini CLI settings.")
    parser.add_argument("--project", required=True, help="Your Google Cloud Project ID.")
    parser.add_argument("--bucket", help="Your Google Cloud Storage bucket for GenMedia assets. Defaults to <project>-mediagen-files")
    parser.add_argument("--region", default="us-central1", help="Google Cloud Region (default: us-central1)")
    parser.add_argument("--local", action="store_true", help="Update the local .gemini/settings.json file instead of the global one.")
    
    args = parser.parse_args()

    # Default bucket logic
    bucket_name = args.bucket
    if not bucket_name:
        bucket_name = f"{args.project}-mediagen-files"

    print(f"Checking if bucket gs://{bucket_name} exists...")
    result = subprocess.run(["gsutil", "ls", f"gs://{bucket_name}"], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Creating bucket gs://{bucket_name} in {args.region}...")
        create_res = subprocess.run(["gsutil", "mb", "-l", args.region, f"gs://{bucket_name}"])
        if create_res.returncode != 0:
            print("Warning: Failed to create bucket. You may need to create it manually.", file=sys.stderr)
    else:
        print(f"Bucket gs://{bucket_name} already exists.")

    if args.local:
        settings_file = os.path.join(os.getcwd(), ".gemini", "settings.json")
    else:
        settings_file = os.path.expanduser("~/.gemini/settings.json")

    bin_dir = os.path.expanduser("~/.local/bin")

    genmedia_servers = {
        "veo": {
            "command": os.path.join(bin_dir, "mcp-veo-go"),
            "env": {
                "MCP_REQUEST_MAX_TOTAL_TIMEOUT": "240000",
                "MCP_SERVER_REQUEST_TIMEOUT": "30000",
                "GENMEDIA_BUCKET": bucket_name,
                "PROJECT_ID": args.project,
                "LOCATION": args.region
            }
        },
        "imagen": {
            "command": os.path.join(bin_dir, "mcp-imagen-go"),
            "env": {
                "MCP_SERVER_REQUEST_TIMEOUT": "55000",
                "GENMEDIA_BUCKET": bucket_name,
                "PROJECT_ID": args.project,
                "LOCATION": args.region
            }
        },
        "chirp3-hd": {
            "command": os.path.join(bin_dir, "mcp-chirp3-go"),
            "env": {
                "MCP_SERVER_REQUEST_TIMEOUT": "55000",
                "GENMEDIA_BUCKET": bucket_name,
                "PROJECT_ID": args.project,
                "LOCATION": args.region
            }
        },
        "lyria": {
            "command": os.path.join(bin_dir, "mcp-lyria-go"),
            "env": {
                "GENMEDIA_BUCKET": bucket_name,
                "PROJECT_ID": args.project,
                "LOCATION": args.region,
                "MCP_SERVER_REQUEST_TIMEOUT": "55000"
            }
        },
        "avtool": {
            "command": os.path.join(bin_dir, "mcp-avtool-go"),
            "env": {
                "PROJECT_ID": args.project,
                "LOCATION": args.region,
                "MCP_SERVER_REQUEST_TIMEOUT": "55000"
            }
        }
    }

    data = {}
    if os.path.exists(settings_file):
        try:
            with open(settings_file, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {settings_file} contains invalid JSON. Overwriting.", file=sys.stderr)

    if 'mcpServers' not in data:
        data['mcpServers'] = {}

    data['mcpServers'].update(genmedia_servers)

    os.makedirs(os.path.dirname(settings_file), exist_ok=True)
    with open(settings_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\nSuccessfully updated {settings_file} with GenMedia MCP servers.")
    print("======================================================")
    print(f"Project ID: {args.project}")
    print(f"Bucket:     {bucket_name}")
    print(f"Region:     {args.region}")
    print(f"Servers:    {', '.join(genmedia_servers.keys())}")
    print("======================================================")

if __name__ == "__main__":
    main()
