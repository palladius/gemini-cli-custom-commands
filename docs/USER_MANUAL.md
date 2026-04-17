# User Manual

This document provides a list of all the custom commands available in this extension.

## 💻 Code Commands (`/code`)

*   **`/code:pda`**: Follows the Plan, Define, Act workflow to structure project execution.

## 🏃 Common Commands (`/common`)

*   **`/common:find_todos`**: Find TODOs in the codebase
*   **`/common:whereabouts`**: 🦘 Riccardo Whereabouts logic for Gemini commands

## ✍️ Dev Commands (`/dev`)

*   **`/dev:check-writing-style`**: Check writing style for documentation files.

## 📣 DevRel Commands (`/devrel`)

*   **`/devrel:article-feedback`**: Critiques an article, providing detailed feedback on tone, typos, quality, and broken links. Caches the analysis for 5 days.
*   **`/devrel:check_google_license`**: [ricc] Checks for license compliance in pragmatic way.

## 📁 Filesystem Commands (`/fs`)

*   **`/fs:grep-code`**: recursive grepping - from template

## ☁️ GCP Commands (`/gcp`)

*   **`/gcp:cloud_build_investigation`**: Cloud Build Investigations and Tools (specialized in pushing to Cloud Run)

## 🔀 Git Commands (`/git`)

*   **`/git:commit_push`**: [ricc] Commit and push changes to the current git repo.
*   **`/git:migrate_bitbucket_to_gitxxb`**: Migrate repo from BitBucket to GitHub or GitLab
*   **`/git:recover_history`**: Reconcile apps in random-apps-ideas/ with JSON in GitHub Pages.

## 🐙 GitHub Commands (`/github`)

*   **`/github:issue`**: Interact with GitHub on Issues on a git repo.

## 🦊 GitLab Commands (`/gitlab`)

*   **`/gitlab:issue`**: Interact with GitLab Issues on a git repo.

## 🔄 Self-Reflect Commands (`/pcc`)

*   **`/pcc:refresh-user-manual`**: [internal] refresh the User manual of this repo

## 🗺️ Plan Commands (`/plan`)

*   **`/plan:do`**: Plan a new feature or fix a bug

## 🚨 SRE Commands (`/sre`)

*   **`/sre:postmortem-create`**: Create a PostMortem document and file bugs [DEPRECATED - please use the SKILL from https://github.com/palladius/sre instead]

## 🧠 Agent Skills

This extension also provides **Agent Skills**, which are specialized capabilities that Gemini can use autonomously.

*   **`cloud-build-investigation`**: 🏗️ Expert-level SRE skill for Google Cloud Build (GCB) and Cloud Run investigations. Activate when user mentions Cloud Build failures, deployment issues to Cloud Run.
*   **`devrel-frictionlog-codelab`**: 🥑 [DevRel] Automates friction logging for a given Google Codelab URL.
*   **`genmedia-setup`**: 🎨 **[MIGRATED]** Setup and use GenMedia MCP tools (Veo, Imagen, Chirp, Lyria). *This skill now includes all former `aicinema` custom command functionality.*
*   **`musicgen-lyria3`**: 🎵 Generates 30-second clips or 2-minute songs using Lyria 3.
*   **`pcc-check-for-updates`**: 🔄 Checks for updates to remote GH site for palladius/gemini-cli-custom-commands.
*   **`postmortem-aggregator`**: 💀 **[MIGRATED]** [SRE] This skill has been moved to the official [sre](https://github.com/palladius/sre) extension. Please install and use that extension instead.
*   **`postmortem-generator`**: 💀 **[MIGRATED]** [SRE] This skill has been moved to the official [sre](https://github.com/palladius/sre) extension. Please install and use that extension instead.

## Wow Factor

Here are a few examples of how you can use these commands in practice:

*   **Find all the TODOs in your code:**
    ```bash
    gemini -p "/common:find_todos"
    ```
*   **Check for updates to this extension (using the new Skill!):**
    Ask Gemini: "Is my palladius-common-commands extension up to date?"
*   **Commit and push your changes with a helpful message:**
    ```bash
    gemini -p "/git:commit_push"
    ```
