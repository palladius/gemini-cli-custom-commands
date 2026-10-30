---
trigger: glob
globs: "GEMINI.md,AGENTS.md,CLAUDE.md,CONTRIBUTING.md,SPECS.md,SPEC.md,INSTRUCTIONS.md,SKILL.md,**/GEMINI.md,**/AGENTS.md,**/CLAUDE.md,**/CONTRIBUTING.md,**/SPECS.md,**/SPEC.md,**/INSTRUCTIONS.md,**/SKILL.md"
description: Anti-bloat guardrails and inclusive AGENTS.md best practices when editing or committing agent system prompt markdown files (AGENTS.md, GEMINI.md, CONTRIBUTING.md, SPECS.md, SKILL.md).
---

# Anti-Bloat & Inclusive Prompt Rule (`ai-coding` + `git-coding`)

Whenever you edit, patch, review, or commit changes to an agent system instruction file (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `SPECS.md`, `SPEC.md`, `INSTRUCTIONS.md`, or `SKILL.md`):

1. **Activate the `ai-coding` (and `git-coding`) Skill:**
   - Read and follow `gemini-cli-palladius-public-goodies/skills/ai-coding/SKILL.md` (and Mandate #6 in `gemini-cli-palladius-public-goodies/skills/git-coding/SKILL.md`).
   - **Prefer `AGENTS.md` over `GEMINI.md`:** `AGENTS.md` is vendor-neutral and inclusive across harnesses. If `GEMINI.md` is needed for legacy tooling, symlink `GEMINI.md -> AGENTS.md` instead of duplicating instructions.
2. **Prevent Prompt Bloat:**
   - **Never cram 10 instructions into 1 line** (`CRAMMED_LINE`). Keep rules atomic, readable, and well-structured.
   - **Never add a whole H2/H3 section (`## Heading`) for a single narrow/overfitting concept** (`OVERFITTING_H2_SECTION`). Consolidate into an existing section or move narrow rules into the specific skill/module they belong to.
   - **Avoid blind append-only edits at EOF** (`APPEND_ONLY_EOF`). Read the existing file and integrate or prune rules instead of just appending at the bottom.
3. **Run the Anti-Bloat Analyzer Script (`analyze_bloat_history.py`):**
   - Before committing changes to the file, run:
     ```bash
     python3 gemini-cli-palladius-public-goodies/skills/ai-coding/scripts/analyze_bloat_history.py --uncommitted <FILENAME>
     ```
   - To audit the git commit history of the file for past bloat (deterministic mode or `--llm` JSON mode with `gemini-flash-latest`):
     ```bash
     python3 gemini-cli-palladius-public-goodies/skills/ai-coding/scripts/analyze_bloat_history.py <FILENAME>
     python3 gemini-cli-palladius-public-goodies/skills/ai-coding/scripts/analyze_bloat_history.py --llm <FILENAME>
     ```
