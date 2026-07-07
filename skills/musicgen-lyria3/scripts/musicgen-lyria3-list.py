#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "google-genai",
#     "tabulate",
# ]
# ///

"""
List music/audio capable models available in Google GenAI.
"""

import sys
import argparse
from google import genai
from tabulate import tabulate

__version__ = "0.0.1"

def main():
    parser = argparse.ArgumentParser(
        description="List music/audio capable models available in Google GenAI.",
        epilog="Example usage: ./musicgen-lyria3-list.py"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()

    try:
        client = genai.Client()
        print("🔍 Querying Google GenAI models...")
        models = client.models.list()
        
        found_models = []
        for m in models:
            name = m.name.lower()
            description = m.description.lower() if m.description else ""
            display_name = m.display_name.lower() if m.display_name else ""
            
            # Check if any audio/music/lyria keywords match
            if any(k in name or k in description or k in display_name for k in ["lyria", "music", "audio", "sound"]):
                # Format supported actions
                actions = ", ".join(m.supported_actions) if m.supported_actions else "None"
                
                found_models.append([
                    m.display_name or "N/A",
                    m.name,
                    actions
                ])

        if not found_models:
            print("🤷 No specific Lyria or music/audio models were returned by list().")
            print("💡 Note: Some preview models (like 'lyria-3-clip-preview' or 'lyria-3-pro-preview') may still be accessible even if not explicitly returned in the active catalog list.")
        else:
            print(f"\n✅ Found {len(found_models)} music/audio capable model(s):")
            print(tabulate(found_models, headers=["Display Name", "Model Name / ID", "Supported Actions"], tablefmt="grid"))
            
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
