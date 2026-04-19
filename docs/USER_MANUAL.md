# User Manual

This document provides a list of all the custom commands available in this extension.

## 💻 Code Commands (`/code`)

*   **`/code:pda`**: Follows the Plan, Define, Act workflow to structure project execution. Ideal for complex tasks requiring careful planning and step-by-step execution.

## 🏃 Common Commands (`/common`)

*   **`/common:find_todos`**: Find TODOs in the codebase. Organizes them into bugs, feature requests, and documentation tasks, and can even help move them to GitHub issues.
*   **`/common:whereabouts`**: 🦘 Riccardo Whereabouts logic for Gemini commands. Helps determine if Riccardo is at his computer or active.

## ✍️ Dev Commands (`/dev`)

*   **`/dev:check-writing-style`**: Check writing style for documentation files. Ensures consistency and quality in technical writing.

## 📣 DevRel Commands (`/devrel`)

*   **`/devrel:article-feedback`**: Critiques an article, providing detailed feedback on tone, typos, quality, and broken links.
*   **`/devrel:check_google_license`**: [ricc] Checks for license compliance in a pragmatic way, ensuring source files have the correct headers.

## 📁 Filesystem Commands (`/fs`)

*   **`/fs:grep-code`**: Recursive grepping - from template. A powerful tool for searching through the codebase with customizable patterns.

## ☁️ GCP Commands (`/gcp`)

*   **`/gcp:cloud_build_investigation`**: Cloud Build Investigations and Tools. Specialized in debugging build failures and pushing to Cloud Run.

## 🔀 Git Commands (`/git`)

*   **`/git:commit_push`**: [ricc] Commit and push changes to the current git repo. Streamlines the standard git workflow.
*   **`/git:migrate_bitbucket_to_gitxxb`**: Migrate repo from BitBucket to GitHub or GitLab. Handles the complexity of repository migration.
*   **`/git:recover_history`**: Reconcile apps in random-apps-ideas/ with JSON in GitHub Pages. Specialized tool for history recovery.

## 🐙 GitHub Commands (`/github`)

*   **`/github:issue`**: Interact with GitHub Issues on a git repo. Create, list, and manage issues directly from the CLI.

## 🦊 GitLab Commands (`/gitlab`)

*   **`/gitlab:issue`**: Interact with GitLab Issues on a git repo. Similar to the GitHub tool but for GitLab environments.

## 🔄 Self-Reflect Commands (`/pcc`)

*   **`/pcc:refresh-user-manual`**: [internal] Refresh the User manual of this repo. Keeps the documentation in sync with the available commands.

## 🗺️ Plan Commands (`/plan`)

*   **`/plan:do`**: Plan a new feature or fix a bug. Helps structure the initial phase of development.

## 🚨 SRE Commands (`/sre`)

*   **`/sre:postmortem-create`**: **[DEPRECATED]** Create a PostMortem document and file bugs. *Please use the SKILL from [palladius/sre](https://github.com/palladius/sre) instead for full functionality.*

## 🧠 Agent Skills

This extension also provides **Agent Skills**, which are specialized capabilities that Gemini can use autonomously.

*   **`cloud-build-investigation`**: 🏗️ Expert-level SRE skill for Google Cloud Build (GCB) and Cloud Run investigations. Correlates git commits with build failures and analyzes logs.
*   **`devrel-frictionlog-codelab`**: 🥑 [DevRel] Automates friction logging for a given Google Codelab URL. Reproduces steps and logs friction points.
*   **`genmedia-setup`**: 🎨 **[MIGRATED]** Setup and use GenMedia MCP tools (Veo, Imagen, Chirp, Lyria). *This skill now includes all former `aicinema` custom command functionality.*
*   **`musicgen-lyria3`**: 🎵 Generates 30-second clips or 2-minute songs using Lyria 3. Supports custom prompts and lyrics.
*   **`pcc-check-for-updates`**: 🔄 Checks for updates to remote GH site for palladius/gemini-cli-custom-commands. Robust version checker using Ruby.
*   **`postmortem-aggregator`**: 💀 **[MIGRATED]** [SRE] This skill has been moved to the official [sre](https://github.com/palladius/sre) extension.
*   **`postmortem-generator`**: 💀 **[MIGRATED]** [SRE] This skill has been moved to the official [sre](https://github.com/palladius/sre) extension.

## Wow Factor

Here are a few examples of how you can use these commands in practice:

*   **Find all the TODOs in your code:**
    ```bash
    gemini -p "/common:find_todos"
    ```
*   **Check for updates to this extension:**
    Ask Gemini: "Is my palladius-common-commands extension up to date?"
*   **Commit and push your changes with a helpful message:**
    ```bash
    gemini -p "/git:commit_push"
    ```
