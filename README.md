# Palladius Gemini CLI custom commands (or 🔄)

Self: https://github.com/palladius/gemini-cli-custom-commands

This is a collection of all "Carlessian" commands, packaged into one place.

**TL;DR** `$ gemini extensions install https://github.com/palladius/gemini-cli-custom-commands`

 ![Version](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/palladius/gemini-cli-custom-commands/main/gemini-extension.json&query=$.version&label=version&color=red&labelColor=blue) [![License](https://img.shields.io/badge/License-Apache%202.0-green?labelColor=yellow)](LICENSE)
- 📖 [User Manual](docs/USER_MANUAL.md)
- 📝 [Changelog](CHANGELOG.md)
- 💡 Inspired by [google-gemini/gemini-cli-security](https://github.com/google-gemini/gemini-cli-security) extension.
- 🚀 Referenced in the Official [Gemini CLI Extensions](https://geminicli.com/extensions/browse/) site (wOOt!)

## INSTALL

**Note** *(requires Gemini CLI v`0.4.0` or newer)*:

```bash
# 🔍 Check version >= 0.4.0
gemini -v
# 💛 Install
gemini extensions install https://github.com/palladius/gemini-cli-custom-commands
# 🔄 Update
gemini extensions update palladius-common-commands
gemini extensions update --all
# 🤢 Uninstall
gemini extensions uninstall palladius-common-commands
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
*   **`☁️ GCP`**: `/gcp:cloud_build_investigation` - Cloud Build/Run debugging.
*   **`🔄 Self-Reflect`**: `/pcc:refresh-user-manual` - Refresh documentation.
*   **`🗺️ Plan`**: `/plan:do` - Plan new features or fixes.
*   **`🚨 SRE`**: `/sre:postmortem-create` - **[DEPRECATED]** Create postmortems (use the `sre` extension skills instead).

## 🧠 Agent Skills

Starting with version `0.0.22`, we are introducing **[Agent Skills](https://geminicli.com/docs/cli/skills/)**! 🚀 These allow Gemini to act more autonomously and precisely.

*   **`cloud-build-investigation`**: Expert-level SRE skill for Google Cloud Build and Cloud Run investigations.
*   **`devrel-frictionlog-codelab`**: Automates friction logging for a given Google Codelab URL.
*   **`genmedia-setup`**: 🎨 **[MIGRATED]** Setup and use GenMedia MCP tools (Veo, Imagen, Chirp, Lyria).
*   **`musicgen-lyria3`**: 🎵 Generate 30-second music clips or 2-3 minute full songs with the Lyria 3 model.
*   **`pcc-check-for-updates`**: Our flagship skill! A robust **Ruby**-based version checker.
*   **`postmortem-aggregator`**: 🚨 **[MIGRATED]** [SRE] Moved to the official [sre extension](https://github.com/palladius/sre).
*   **`postmortem-generator`**: 🚨 **[MIGRATED]** [SRE] Moved to the official [sre extension](https://github.com/palladius/sre).

## Wow Factor


**WARNING**: This project is intended for demonstration purposes only. It is not intended for use in a production environment.


## Thanks





* Arthur Yau for contributing the code/PDA framework.

