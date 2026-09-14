#!/usr/bin/env python3
"""
extract_codelab.py
Usage:
  python3 extract_codelab.py <url_or_markdown_path> <output_dir>
  python3 extract_codelab.py --sync-readme <base_dir>

Extracts Google Codelab steps into Markdown files (`01.md`, `02.md`, ...) in `<output_dir>`,
copies them to `proposed/`, and dynamically updates the Step-by-Step Scorecard Table
in `<base_dir>/README.md` with the exact number of steps, titles, and durations.
"""

import sys
import urllib.request
import re
import os
import shutil
import glob

def sync_readme_scorecard(base_dir, steps_metadata=None):
    """
    Updates the Step-by-Step Scorecard Table in <base_dir>/README.md
    using either provided `steps_metadata` [(idx, title, duration), ...]
    or by scanning <base_dir>/codelab/original/*.md.
    """
    readme_path = os.path.join(base_dir, "README.md")
    if not os.path.exists(readme_path):
        return

    if not steps_metadata:
        orig_dir = os.path.join(base_dir, "codelab", "original")
        md_files = sorted(glob.glob(os.path.join(orig_dir, "*.md")))
        steps_metadata = []
        for idx, md_file in enumerate(md_files, start=1):
            title = f"Step {idx}"
            duration = "—"
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line_s = line.strip()
                        if line_s.startswith("# ") and title == f"Step {idx}":
                            title = line_s[2:].strip()
                        elif line_s.lower().startswith("duration:"):
                            duration = line_s.split(":", 1)[1].strip()
            except Exception:
                pass
            steps_metadata.append((idx, title, duration))

    if not steps_metadata:
        return

    table_lines = [
        "## 🚦 Step-by-Step Scorecard Table",
        "",
        "| Step # | Codelab Step Title | Vote (`🟢`/`🟡`/`🔴`) | Est. Duration | Empirical Verification & Log Link |",
        "| :---: | :--- | :---: | :---: | :--- |",
    ]
    for idx, title, duration in steps_metadata:
        step_num = f"{idx:02d}"
        dur_str = f"`{duration}m`" if duration.isdigit() else f"`{duration}`"
        table_lines.append(
            f"| **{step_num}** | **{title}** | ⏳ **PENDING** | {dur_str} | [Original](codelab/original/{step_num}.md) \\| [Log](FRICTION_LOG/{step_num}.md) |"
        )

    new_table_block = "\n".join(table_lines) + "\n"

    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    # Replace everything from '## 🚦 Step-by-Step Scorecard Table' to the end or next '##' section
    pattern = r"## 🚦 Step-by-Step Scorecard Table.*?(?=\n## |\Z)"
    if re.search(pattern, readme_content, flags=re.DOTALL):
        updated_content = re.sub(pattern, new_table_block.strip(), readme_content, flags=re.DOTALL) + "\n"
    else:
        updated_content = readme_content.rstrip() + "\n\n" + new_table_block

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
    print(f"📊 Dynamically updated {readme_path} scorecard with {len(steps_metadata)} exact steps!")


def parse_markdown_codelab(md_text):
    """
    Parses a DevSite/Google3 markdown codelab (index.lab.md) where steps are top-level `## Title`
    headers (excluding metadata sections before the first step if applicable).
    Returns list of tuples: [(label, duration, content), ...]
    """
    steps = []
    # Split by level-2 headings `## Step Title`
    chunks = re.split(r"(?m)^##\s+(.+)$", md_text)
    # chunks[0] is header/frontmatter before first ##
    for i in range(1, len(chunks), 2):
        label = chunks[i].strip()
        body = chunks[i + 1] if i + 1 < len(chunks) else ""
        dur_match = re.search(r"(?m)^Duration:\s*(\S+)", body)
        duration = dur_match.group(1) if dur_match else "—"
        steps.append((label, duration, body.strip()))
    return steps


def extract_codelab(url_or_path, output_dir):
    print(f"Attempting to extract codelab from {url_or_path} to {output_dir}")
    try:
        raw_text = ""
        is_local_md = False

        if os.path.exists(url_or_path) and url_or_path.endswith(".md"):
            is_local_md = True
            with open(url_or_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
        else:
            req = urllib.request.Request(url_or_path, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                raw_text = response.read().decode('utf-8')

        output_dir = os.path.normpath(output_dir)
        proposed_dir = os.path.join(os.path.dirname(output_dir), "proposed")
        base_dir = os.path.dirname(os.path.dirname(output_dir))
        if not os.path.exists(proposed_dir):
            os.makedirs(proposed_dir)

        steps_metadata = []

        if is_local_md:
            md_steps = parse_markdown_codelab(raw_text)
            if not md_steps:
                print("⚠️ Could not find `## Step` headings in local markdown file.")
                return
            for i, (label, duration, body) in enumerate(md_steps, start=1):
                filename = os.path.join(output_dir, f"{i:02d}.md")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(f"# {label}\n\n{body}\n")
                shutil.copy(filename, os.path.join(proposed_dir, f"{i:02d}.md"))
                steps_metadata.append((i, label, duration))
                print(f"✅ Saved markdown step '{label}' ({duration}) to {filename}")
        else:
            # Basic extraction: Google Codelabs often use <google-codelab-step> tags
            steps = re.findall(
                r'<google-codelab-step([^>]*)>(.*?)</google-codelab-step>',
                raw_text,
                re.DOTALL
            )

            if not steps:
                print("⚠️ Could not find <google-codelab-step> tags in the raw HTML.")
                print("The codelab might be rendered dynamically via JavaScript.")
                print("AGENT INSTRUCTION: Fall back to your native `web_fetch` tool to read the codelab and create the 01.md, 02.md... files manually, then run:")
                print(f"  python3 {sys.argv[0]} --sync-readme {base_dir}")
                return

            for i, (attrs, content) in enumerate(steps, start=1):
                label_m = re.search(r'label="([^"]+)"', attrs)
                dur_m = re.search(r'duration="([^"]+)"', attrs)
                label = label_m.group(1) if label_m else f"Step {i}"
                duration = dur_m.group(1) if dur_m else "0"

                filename = os.path.join(output_dir, f"{i:02d}.md")
                with open(filename, 'w', encoding="utf-8") as f:
                    f.write(f"# {label}\nDuration: {duration}\n\n")

                    # Heuristic for code blocks: wrap <pre> content in triple backticks
                    content = re.sub(
                        r'<pre.*?(?:class="lang-([^"]+)")?.*?><code.*?>(.*?)</code></pre>',
                        lambda m: f"\n```{' ' + m.group(1) if m.group(1) else ''}\n{m.group(2).strip()}\n```\n",
                        content,
                        flags=re.DOTALL
                    )
                    content = re.sub(r'<pre.*?>(.*?)</pre>', r'\n```\n\1\n```\n', content, flags=re.DOTALL)
                    content = re.sub(r'<code>(.*?)</code>', r'`\1`', content, flags=re.DOTALL)
                    content = re.sub(r'<(b|strong).*?>(.*?)</\1>', r'**\2**', content, flags=re.DOTALL)
                    content = re.sub(r'<(i|em).*?>(.*?)</\1>', r'*\2*', content, flags=re.DOTALL)

                    text_content = re.sub(r'<[^>]+>', '', content)
                    text_content = (
                        text_content.replace('&lt;', '<')
                        .replace('&gt;', '>')
                        .replace('&amp;', '&')
                        .replace('&quot;', '"')
                        .replace('&#39;', "'")
                    )

                    f.write(text_content.strip() + "\n")

                shutil.copy(filename, os.path.join(proposed_dir, f"{i:02d}.md"))
                steps_metadata.append((i, label, duration))
                print(f"✅ Saved step '{label}' (duration={duration}) to {filename} (and copied to proposed/)")

        # Automatically update README.md scorecard if README.md exists in base_dir
        sync_readme_scorecard(base_dir, steps_metadata)

    except Exception as e:
        print(f"❌ Error extracting codelab: {e}")
        print("AGENT INSTRUCTION: Fall back to your native `web_fetch` tool.")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--sync-readme":
        sync_readme_scorecard(sys.argv[2])
        sys.exit(0)

    if len(sys.argv) != 3:
        print("Usage:")
        print("  python3 extract_codelab.py <url_or_markdown_path> <output_dir>")
        print("  python3 extract_codelab.py --sync-readme <base_dir>")
        sys.exit(1)

    url_or_path = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(output_dir):
        print(f"Error: Output directory '{output_dir}' does not exist.")
        sys.exit(1)

    extract_codelab(url_or_path, output_dir)
