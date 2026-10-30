# Agent Instructions for `gemini-cli-custom-commands` (💻)

Community-facing Gemini CLI extension and Agent Plugin (`palladius-common-commands`) containing reusable Custom Commands (`commands/`) and Skills (`skills/`).

## Structure & Local Dogfooding
- **Canonical Directories**: Add and track all new commands under `commands/` and skills under `skills/` (`.gemini/commands` and `.gemini/skills` are git-ignored symlinks to `../commands/` and `../skills/` for local dogfooding).
- **Custom Commands (`commands/**/*.toml`)**: Invoked via `/path:to:file <args>` with arguments passed via `{{args}}` ([Gemini CLI Custom Commands docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/custom-commands.md)).
- **Skills (`skills/<name>/SKILL.md`)**:
  - Follow the standard `SKILL.md` frontmatter schema (`name`, `description: >-`, `compatibility`, `metadata.version`).
  - Include a brief usage header at the top of each script under `skills/<name>/scripts/` and a matching runnable test (`<script>_test.rb` or `<script>_test.py`).
  - Reference repo for security/extension conventions: `https://github.com/gemini-cli-extensions/security/`.

## Release, Docs & Conventions
- **Version & Changelog**: Keep `VERSION` in `gemini-extension.json` (`+0.0.1` for new scripts/patches, `+0.1.0` for major restructurings; no bump needed for pure doc fixes) and update `CHANGELOG.md`.
- **Documentation**: Document all commands in `docs/USER_MANUAL.md` and summarize updates in `README.md`.
- **Git Style**: Use `gitmoji` in commits/changelogs and sign agent-authored commits (e.g., `[Antigravity]` or `-- made with Gemini CLI`).
- **Constraints**: This repository does **not** use Cloud Build (`cloudbuild.yaml`).
