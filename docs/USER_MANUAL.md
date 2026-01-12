# User Manual

This document provides a list of all the custom commands available in this extension.

### 🎬 AICinema Commands (`/aicinema`)

*   **`/aicinema:audio_story`**: Create an audio story from a script using GMP Assistant.
*   **`/aicinema:check_install`**: Check if the GoLang installation was done correctly.
*   **`/aicinema:video_storyboard`**: Create an audio/video story from a script using GenAI.

### 💻 Code Commands (`/code`)

*   **`/code:pda`**: Follows the Plan, Define, Act workflow to structure project execution.

### 🏃 Common Commands (`/common`)

*   **`/common:find_todos`**: Find TODOs in the codebase
*   **`/common:whereabouts`**: 🦘 Riccardo Whereabouts logic for Gemini commands

### 🎼 Conductor Commands (`/conductor`)

*   **`/conductor:do`**: Execute Keith's configuration files
*   **`/conductor:install`**: Install Keith's configuration files

### ✍️ Dev Commands (`/dev`)

*   **`/dev:check-writing-style`**: Check writing style for documentation files.

### 📣 DevRel Commands (`/devrel`)

*   **`/devrel:article-feedback`**: Critiques an article, providing detailed feedback on tone, typos, quality, and broken links. Caches the analysis for 5 days.
*   **`/devrel:check_google_license`**: [ricc] Checks for license compliance in pragmatic way.

### 📁 Filesystem Commands (`/fs`)

*   **`/fs:grep-code`**: recursive grepping - from template

### 🔀 Git Commands (`/git`)

*   **`/git:commit_push`**: [ricc] Commit and push changes to the current git repo.
*   **`/git:migrate_bitbucket_to_gitxxb`**: Migrate repo from BitBucket to GitHub or GitLab
*   **`/git:recover_history`**: Reconcile apps in random-apps-ideas/ with JSON in GitHub Pages.

### 🐙 GitHub Commands (`/github`)

*   **`/github:issue`**: Interact with GitHub on Issues on a git repo.

### 🦊 GitLab Commands (`/gitlab`)

*   **`/gitlab:issue`**: Interact with GitLab on Issues on a git repo.

### ☁️ GCP Commands (`/gcp`)

*   **`/gcp:cloud_build_investigation`**: Cloud Build Investigations and Tools (specialized in pushing to Cloud Run)

### 🔄 Self-Reflect Commands (`/pcc`)

*   **`/pcc:check-for-updates`**: Do I need an update?
*   **`/pcc:refresh-user-manual`**: [internal] refresh the User manual of this repo

### 🗺️ Plan Commands (`/plan`)

*   **`/plan:do`**: Plan a new feature or fix a bug

### 🚨 SRE Commands (`/sre`)

*   **`/sre:postmortem-create`**: Create a PostMortem document and file bugs following SRE best practices, with automated timeline management and bug filing.

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
    gemini -p "/git:commit_push Add a new feature"
    ```
*   **Create a postmortem document for an incident:**
    ```bash
    gemini -y -p "/sre:postmortem-create incident_id INC123456"
    ```
