# Palladius Gemini CLI custom commands (or PCC)

Self: https://github.com/palladius/gemini-cli-custom-commands

This is a collection of all "Carlessian" commands, packaged into one place.

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

*   **`🏃 Common`**: A collection of everyday commands to streamline your workflow, from checking licenses to managing TODOs and git commits.
*   **`🤖 Conductor`**: Manage and execute Keith's configuration files with ease.
*   **`✍️ Dev`**: Developer-focused commands, starting with a tool to check the writing style of your documentation.
*   **`📁 Filesystem`**: Handy filesystem operations, like recursively grepping through your code.
*   **`☁️ GCP`**: Tools for interacting with Google Cloud Platform, starting with Cloud Build investigations.
*   **`🐙 GitHub`**: All about GitHub, starting with a command to help you implement code to fix failing tests.
*   **`🅿️ PCC`**: Manage this extension itself, with commands to check for updates and refresh the user manual.
*   **`🗺️ Plan`**: Helps you plan new features or bug fixes.


**WARNING**: This project is intended for demonstration purposes only. It is not intended for use in a production environment.

