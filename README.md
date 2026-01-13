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

Here's a sneak peek of the commands available. For a full list, see the [User Manual](docs/USER_MANUAL.md).

*   **`🎬 AICinema`**: A collection of commands to create audio and video stories using generative AI.
*   **`💻 Code`**: Commands for structuring your coding workflow.
*   **`🏃 Common`**: A collection of everyday commands to streamline your workflow, from managing TODOs to checking whereabouts.
*   **`🎼 Conductor`**: Manage and execute Keith's configuration files with ease.
*   **`✍️ Dev`**: Developer-focused commands, starting with a tool to check the writing style of your documentation.
*   **`� DevRel`**: Developer Relations tools, including article feedback and license checking.
*   **`�📁 Filesystem`**: Handy filesystem operations, like recursively grepping through your code.
*   **`🔀 Git`**: Git workflow automation, including commit/push, BitBucket migration, and history recovery.
*   **`🐙 GitHub`**: Interact with GitHub issues and repository management.
*   **`🦊 GitLab`**: Interact with GitLab on issues and other repository tasks.
*   **`☁️ GCP`**: Tools for interacting with Google Cloud Platform, starting with Cloud Build investigations.
*   **`🔄 Self-Reflect`**: Commands to refresh the user manual and manage the extension.
*   **`🗺️️ Plan`**: Helps you plan new features or bug fixes.
*   **`🚨 SRE`**: Site Reliability Engineering tools, including comprehensive postmortem document creation with automated bug filing and timeline management.

## 🧠 Agent Skills

Starting with version `0.0.22`, we are introducing **[Agent Skills](https://geminicli.com/docs/cli/skills/)**! 🚀 These allow Gemini to act more autonomously and precisely.

*   **`check-for-updates`**: Our flagship skill! It replaces the old `/pcc:check-for-updates` command with a robust **Ruby**-based version checker that understands Semantic Versioning. No more "0.0.95 is newer than 0.0.122" confusion!

## Wow Factor


**WARNING**: This project is intended for demonstration purposes only. It is not intended for use in a production environment.


## Thanks

* Arthur Yau for contributing the code/PDA framework.
* Keith B. for the concductor framework.