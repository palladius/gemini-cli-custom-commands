# Riccardo's Custom Antigravity & Gemini CLI Commands 🔄 (🔌)

Self: https://github.com/palladius/gemini-cli-custom-commands

This is a collection of all "Carlessian" custom commands and agent skills, packaged into one place.

![Version](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/palladius/gemini-cli-custom-commands/main/gemini-extension.json&query=$.version&label=version&color=red&labelColor=blue) [![License](https://img.shields.io/badge/License-Apache%202.0-green?labelColor=yellow)](LICENSE)
- 📖 [User Manual](docs/USER_MANUAL.md)
- 📝 [Changelog](CHANGELOG.md)
- 💡 Inspired by [google-gemini/gemini-cli-security](https://github.com/google-gemini/gemini-cli-security) extension.
- 🚀 Referenced in the Official [Gemini CLI Extensions](https://geminicli.com/extensions/browse/) site.

## Plugin & Extension Compatibility

This repository functions as a native plugin/extension across multiple agent ecosystems:

### 1. Antigravity UI & `agy` CLI
*   **Workspace-Level**: Clone or symlink this directory into `.agents/plugins/palladius-common-commands/` at the root of your workspace.
*   **Global-Level**: Clone or symlink this directory into `~/.gemini/config/plugins/palladius-common-commands/`.
*   **Verification**: Check active plugins and skills inside the CLI/UI using:
    ```bash
    agc plugins
    agc skills
    ```

### 2. Claude Code
*   **Workspace-Level**: Place or symlink this repository folder inside `.claude/plugins/palladius-common-commands/` at the root of your workspace.
*   **Global-Level**: Run Claude Code with the plugin directory flag pointing to this repo:
    ```bash
    claude --plugin-dir /path/to/gemini-cli-custom-commands
    ```
*   Claude Code will automatically recognize `.claude-plugin/plugin.json` and load the skills under the `/palladius-common-commands:` namespace.

### 3. OpenAI Codex
*   This extension is fully Codex-compatible (uses the `.codex-plugin/plugin.json` manifest).

### 4. Legacy: Gemini CLI
*   Installable via the classic extension system (requires Gemini CLI v`0.4.0` or newer):
    ```bash
    gemini extensions install https://github.com/palladius/gemini-cli-custom-commands
    ```

## Available Commands

Here's the full list of commands available in this extension. For more details, see the [User Manual](docs/USER_MANUAL.md).

*   **`💻 Code`**: `/code:pda` - Follows the Plan, Define, Act workflow.
*   **`🏃 Common`**: `/common:find_todos` - Find TODOs; `/common:whereabouts` - Riccardo's presence logic.
*   **`✍️ Dev`**: `/dev:check-writing-style` - Check documentation writing style.
*   **`📣 DevRel`**: `/devrel:article-feedback` - Article critique; `/devrel:check_google_license` - License compliance.
*   **`📁 Filesystem`**: `/fs:grep-code` - Recursive grepping.
*   **`🔀 Git`**: `/git:commit_push` - Commit/push automation; `/git:migrate_bitbucket_to_gitxxb` - Repo migration; `/git:recover_history` - History recovery.
*   **`🐙 GitHub`**: `/github:issue` - Manage GitHub issues.
*   **`🦊 GitLab`**: `/gitlab:issue` - Manage GitLab issues.
*   **`🛠️ SRE`**: `/sre:postmortem-create` - [DEPRECATED] Post-Mortem automation.
*   **`☁️ GCP`**: `/gcp:cloud_build_investigation` - Cloud Build/Run debugging.
*   **`🔄 Self-Reflect`**: `/pcc:refresh-user-manual` - Refresh documentation.
*   **`🗺️ Plan`**: `/plan:do` - Plan new features or fixes.

## 🧠 Agent Skills

These allow agents to act more autonomously and precisely within the Antigravity ecosystem:

*   **`cloud-build-investigation`**: 🏗️ Expert-level SRE skill for Google Cloud Build and Cloud Run investigations.
*   **`conductor-worktree-hitl`**: 🔀 Manage asynchronous task implementation in Git Worktrees using Conductor++ and GitHub Issues.
*   **`devrel-frictionlog-codelab`**: 🥑 Automates friction logging for a given Google Codelab URL.
*   **`genmedia-setup`**: 🎨 **[MIGRATED]** Setup and use GenMedia (MCP) tools and related Gemini skills.
*   **`musicgen-lyria3`**: 🎵 Generate 30-second music clips or 2-3 minute full songs with the Lyria 3 model.
*   **`pcc-check-for-updates`**: 🔄 Our flagship skill! A robust **Ruby**-based version checker.

## Thanks

* Arthur Yau for contributing the code/PDA framework.
