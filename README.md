# Palladius Gemini CLI custom commands (or PCC)

Self: https://github.com/palladius/gemini-cli-custom-commands
Inspired by https://github.com/google-gemini/gemini-cli-security/tree/main

This is a collection of all "Carlessian" commands, packaged into one place.

 ![Version](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/palladius/gemini-cli-custom-commands/main/gemini-extension.json&query=$.version&label=version&color=yellow&labelColor=black) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)


## INSTALL

**Note** *(requires Gemini CLI v0.4.0 or newer):

```bash
# Install
gemini extensions install https://github.com/palladius/gemini-cli-custom-commands
# Update
gemini extensions update palladius-common-commands
gemini extensions update --all
# Uninstall
gemini extensions uninstall palladius-common-commands
```

To see which commands you have installed, for pure curiosity:

`find  ~/.gemini/extensions/palladius-common-commands/commands/ -name \*.toml`

## User Manual

Find the  User Manual under `docs/USER_MANUAL.md`.

### Common Commands (`/common`)

*   **`/common:check_google_license`**: [ricc] Checks for license compliance in pragmatic way.
*   **`/common:find_todos`**: Find TODOs in the codebase
*   **`/common:git_commit_push`**: [ricc] Commit and push changes to the current git repo.
*   **`/common:git_recover_history`**: Reconcile apps in random-apps-ideas/ with JSON in GitHub Pages.
*   **`/common:github_issue`**: Interact with GitHub on Issues on a git repo.
*   **`/common:whereabouts`**: 🦘 Riccardo Whereabouts logic for Gemini commands

### Conductor Commands (`/conductor`)

*   **`/conductor:do`**: Execute Keith's configuration files
*   **`/conductor:install`**: Install Keith's configuration files

### Filesystem Commands (`/fs`)

*   **`/fs:grep-code`**: recursive grepping - from template

### GitHub Commands (`/github`)

*   **`/github:implement`**: Writes the minimal code to make a failing test pass.

### PCC Commands (`/pcc`)

*   **`/pcc:check-for-updates`**: Do I need an update?
*   **`/pcc:refresh-user-manual`**: [internal] refresh the User manual of this repo

## Wow factor

Once installed, run `just check-for-updates`. Or if you don't have `just` installed, you can "just" do `gemini -y -c "/pcc:check-for-updates"`.

Note this functionality has become useless since `0.4.1`'s `gemini extensions update --all`, but still: it's exciting to try genitive over version numbers!

Sample output:

```markdown
# Extension Update Check

## Versions

*   **Local Version:** 0.0.1
*   **Remote Version:** 0.0.3

## Action

The remote version is newer. To update, run the following command: `gemini extensions update palladius-common-commands`

```

This project is intended for demonstration purposes only. It is not intended for use in a production environment.
