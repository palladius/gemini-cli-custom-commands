# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.12] - 2025-10-22

### Changed

- Updated `commands/git/migrate_bitbucket_to_gitxxb.toml` to improve the migration process.
- Bumped version to 0.0.12 in `gemini-extension.json`.

## [0.0.11] - 2025-10-21

### Changed

- Moved git commands to `commands/git` directory.
- Moved github commands to `commands/github` directory.

### Removed

- Removed `commands/github/implement.toml`.

## [0.0.10] - 2025-10-21

### Added

- **Git Commands**:
  - `migrate_bitbucket_to_gitxxb.toml`: A new command to migrate a BitBucket repository to GitHub or GitLab.

### Changed

- Updated `commands/common/git_commit_push.toml` to add a note about `.gitignore`.
- Updated `.gitignore` to ignore `carlessian_context.yaml`.

## [0.0.9] - 2025-10-10

### Added

- **Plan Commands**:
  - `commands/plan/do.toml`: A new command to plan a new feature or fix a bug.

### Fixed

- Improved language and tone in the following command files for better clarity and professionalism:
  - `commands/gcp/cloud_build_investigation.toml`
  - `commands/common/find_todos.toml`
  - `commands/common/git_recover_history.toml`

## [0.0.8] - 2025-10-10

### Added

- **GCP Commands**:
  - `cloud_build_investigation.toml`: A new command to investigate Cloud Build issues.

## [0.0.7] - 2025-10-10

### Added

- **Dev Commands**:
  - `check-writing-style.toml`: A new command to check writing style for documentation.
- **PCC Commands**:
  - `refresh-user-manual.toml`: A new command to refresh the user manual.

## [0.0.6] - 2025-09-22

### Added

-   **Conductor Commands**:
    -   `do.toml`: A new command to execute conductor actions.
    -   `install.toml`: A new command to install conductor.