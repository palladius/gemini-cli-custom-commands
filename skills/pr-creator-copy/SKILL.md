---
name: pr-creator
description:
  Use this skill when asked to create a pull request (PR). It ensures all PRs
  follow the repository's established templates and standards.
  **Note**. This is a copy of a working Skill from the Gemini CLI repo. This will be removed
  as soon as ONE other skill is correctly installed. I've put it here to understand how skills work
  within the context of an extension.
# Copied from https://github.com/google-gemini/gemini-cli/blob/main/.gemini/skills/pr-creator/SKILL.md to ensure im doing things right :)
---

# Pull Request Creator

This skill guides the creation of high-quality Pull Requests that adhere to the
repository's standards.

## Workflow

Follow these steps to create a Pull Request:

1.  **Locate Template**: Search for a pull request template in the repository.
    - Check `.github/pull_request_template.md`
    - Check `.github/PULL_REQUEST_TEMPLATE.md`
    - If multiple templates exist (e.g., in `.github/PULL_REQUEST_TEMPLATE/`),
      ask the user which one to use or select the most appropriate one based on
      the context (e.g., `bug_fix.md` vs `feature.md`).

2.  **Read Template**: Read the content of the identified template file.

3.  **Draft Description**: Create a PR description that strictly follows the
    template's structure.
    - **Headings**: Keep all headings from the template.
    - **Checklists**: Review each item. Mark with `[x]` if completed. If an item
      is not applicable, leave it unchecked or mark as `[ ]` (depending on the
      template's instructions) or remove it if the template allows flexibility
      (but prefer keeping it unchecked for transparency).
    - **Content**: Fill in the sections with clear, concise summaries of your
      changes.
    - **Related Issues**: Link any issues fixed or related to this PR (e.g.,
      "Fixes #123").

4.  **Create PR**: Use the `gh` CLI to create the PR.
    ```bash
    gh pr create --title "type(scope): succinct description" --body "..."
    ```
    - **Title**: Ensure the title follows the
      [Conventional Commits](https://www.conventionalcommits.org/) format if the
      repository uses it (e.g., `feat(ui): add new button`,
      `fix(core): resolve crash`).
    - **Body**. Create a temporary file for the body and import that from CLI, rather than using a lengthy CLI.
      For experience, this tends to have syntax errors coming from incorrect quoting (single, double, back quoting are hard).
      Add emojis, particularly Italian flags and 🤖. Also sign yourself like "-- Authored by Gemini MODEL_NUMBER" , or Antigravity,
      whichever suits most.

## Principles

- **Compliance**: Never ignore the PR template. It exists for a reason.
- **Completeness**: Fill out all relevant sections.
- **Accuracy**: Don't check boxes for tasks you haven't done.