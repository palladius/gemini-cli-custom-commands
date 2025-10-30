# User Manual

This document provides a list of all the custom commands available in this extension.

### 🏃 Common Commands (`/common`)

*   **`/common:check_google_license`**: [ricc] Checks for license compliance in pragmatic way.
*   **`/common:find_todos`**: Find TODOs in the codebase
*   **`/common:git_commit_push`**: [ricc] Commit and push changes to the current git repo.
*   **`/common:git_recover_history`**: Reconcile apps in random-apps-ideas/ with JSON in GitHub Pages.
*   **`/common:github_issue`**: Interact with GitHub on Issues on a git repo.
*   **`/common:whereabouts`**: 🦘 Riccardo Whereabouts logic for Gemini commands

### 🎼 Conductor Commands (`/conductor`)

*   **`/conductor:do`**: Execute Keith's configuration files
*   **`/conductor:install`**: Install Keith's configuration files

### ✍️ Dev Commands (`/dev`)

*   **`/dev:check-writing-style`**: Check writing style for documentation files.

### 📁 Filesystem Commands (`/fs`)

*   **`/fs:grep-code`**: recursive grepping - from template

### 🐙 GitHub Commands (`/github`)

*   **`/github:implement`**: Writes the minimal code to make a failing test pass.

### 🦊 GitLab Commands (`/gitlab`)

*   **`/gitlab:issue`**: Interact with GitLab on Issues on a git repo.

### ☁️ GCP Commands (`/gcp`)

*   **`/gcp:cloud_build_investigation`**:  Cloud Build Investigations and Tools


### 🔄 Self-Reflect Commands (`/pcc`)

*   **`/pcc:check-for-updates`**: Do I need an update?
*   **`/pcc:refresh-user-manual`**: [internal] refresh the User manual of this repo

### 🗺️ Plan Commands (`/plan`)

*   **`/plan:do`**: Plan a new feature or fix a bug


## Wow Factor

Here are a few examples of how you can use these commands in practice:

*   **Find all the TODOs in your code:**
    ```bash
    gemini -p "/common:find_todos"
    ```
*   **Check for updates to this extension:**
    ```bash
    gemini -c "/pcc:check-for-updates"
    ```
*   **Commit and push your changes with a helpful message:**
    ```bash
    gemini -p "/common:git_commit_push Add a new feature"
    ```
