#!/usr/bin/env python3
"""
extract_codelab.py
Usage: python3 extract_codelab.py <url> <output_dir>

A small utility to attempt extracting codelab steps from Google Codelab URLs.
Because many codelabs are dynamically rendered, this uses a simple heuristic
or acts as a fallback. For AI agents: if this script yields empty files or fails,
fall back to your internal `web_fetch` tool and save the output.
"""

import sys
import urllib.request
import re
import os

def extract_codelab(url, output_dir):
    print(f"Attempting to extract codelab from {url} to {output_dir}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
        # Basic extraction: Google Codelabs often use <google-codelab-step> tags
        steps = re.findall(r'<google-codelab-step.*?label="([^"]+)".*?>(.*?)</google-codelab-step>', html, re.DOTALL)
        
        if not steps:
            print("⚠️ Could not find <google-codelab-step> tags in the raw HTML.")
            print("The codelab might be rendered dynamically via JavaScript.")
            print("AGENT INSTRUCTION: Fall back to your native `web_fetch` tool to read the codelab and create the 01.md, 02.md... files manually.")
            return

        for i, (label, content) in enumerate(steps, start=1):
            filename = os.path.join(output_dir, f"{i:02d}.md")
            with open(filename, 'w') as f:
                f.write(f"# {label}\n\n")
                # Strip out basic HTML tags for a quick and dirty markdown format
                text_content = re.sub(r'<[^>]+>', '', content)
                # Decode basic HTML entities
                text_content = text_content.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                f.write(text_content.strip())
            print(f"✅ Saved step '{label}' to {filename}")
            
    except Exception as e:
        print(f"❌ Error extracting codelab: {e}")
        print("AGENT INSTRUCTION: Fall back to your native `web_fetch` tool.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 extract_codelab.py <url> <output_dir>")
        sys.exit(1)
        
    url = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.exists(output_dir):
        print(f"Error: Output directory '{output_dir}' does not exist.")
        sys.exit(1)
        
    extract_codelab(url, output_dir)
