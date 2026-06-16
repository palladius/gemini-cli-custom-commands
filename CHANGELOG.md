# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.34] - 2026-06-16
### Changed
- 👩 **Renamed Git Concierge**: Renamed the coordinator agent from Giovanni to Agostina (Lead Git Concierge) to align with the A.G. (Antigravity) theme.

## [0.3.33] - 2026-06-16
### Changed
- 🤖 **Optimized Polling Loop**: Refactored `poll_ghi_questions.py` to scan local Conductor tracks metadata first and only perform GitHub API calls for issues that actively have questions awaiting human input, saving over 95% of API requests.

## [0.3.32] - 2026-06-16
### Changed
- 🛡️ **Disable Remote Pushing**: Updated `SKILL.md` and the orchestration prompt to explicitly forbid subagents from executing `git push`. Subagents now commit locally to their branches, leaving merging and remote pushing strictly to the parent coordinator (Agostina).

## [0.3.31] - 2026-06-16
### Added
- 📝 **Orchestration Prompt**: Added the `multi-worktree-starter-prompt.md` prompt for Conductor++ worktree flow.
- 🛡️ **Git Hygiene step**: Added instructions in `SKILL.md` to configure git exclude inside worktrees to prevent symlink tracking.

## [0.3.30] - 2026-06-16
### Changed
- 🔀 **Conductor Inspector Sorting**: Implemented custom sorting for tracks where `NEW` status comes first, active/pending next, and `COMPLETED`/`RESOLVED`/`CLOSED` last.

## [0.3.29] - 2026-06-16
### Changed
- 📊 **Conductor Inspector**: Refactored `--short` mode formatting: removed brackets `[]` around the progress bar and replaced percentage (`PCT`) with `N/M` ratio (`completed/total`).

## [0.3.28] - 2026-06-16
### Added
- 🔀 **Worktree HITL Skill**: Added the new `conductor-worktree-hitl` skill supporting asynchronous multi-agent coordination inside Git Worktrees using GitHub Issues and Conductor++ metadata tracking.
- 🤖 **Issue Polling Script**: Created [scripts/poll_ghi_questions.py](file:///Users/ricc/git/gemini-cli-custom-commands/skills/conductor-worktree-hitl/scripts/poll_ghi_questions.py) to aggregate and update active questions.

## [0.3.27] - 2026-06-08
### Added
- 🥑 **Friction Log Skill**: Added the `outputGdocUrl` field to the [references/friction_log.yaml](file:///usr/local/google/home/ricc/git/gemini-cli-custom-commands/skills/devrel-frictionlog-codelab/references/friction_log.yaml) template.
- 🛠️ **Scaffolding Setup**: Updated [setup_scaffold.sh](file:///usr/local/google/home/ricc/git/gemini-cli-custom-commands/skills/devrel-frictionlog-codelab/scripts/setup_scaffold.sh) to accept the 5th optional argument `[OUTPUT_GDOC_URL]` and replace it in the generated `friction_log.yaml`. Updated documentation and unit tests.

## [0.3.26] - 2026-06-08
### Added
- 🥑 **Friction Log Skill**: Created a template file `references/friction_log.yaml` containing the Kubernetes-like schema with version (`codelabVersion`) and start date (`startedAt`) fields.
- 🛠️ **Scaffolding Setup**: Updated `setup_scaffold.sh` to read `references/friction_log.yaml`, replace placeholders, and generate the concrete `friction_log.yaml` file. Added the 4th command-line argument `[CODELAB_VERSION]` and automatic ISO-8601 timestamp generation.

## [0.3.25] - 2026-06-08
### Added
- 🥑 **Friction Log Skill**: Added `friction_log.yaml` as a Kubernetes-like key-value metadata store to keep track of execution parameters (project ID, identity, codelab URL, TF bug).
- 🛠️ **Scaffolding Setup**: Updated `setup_scaffold.sh` to accept optional `[CODELAB_URL]` and `[BUG_ID]` arguments, auto-detect GCP project ID and identity, and write `friction_log.yaml` automatically. Added full unit tests.

## [0.3.24] - 2026-06-08
### Changed
- 🥑 **Friction Log Skill**: Updated the `devrel-frictionlog-codelab` skill to strongly recommend using a fresh/virgin GCP project ID to avoid resource conflicts.

## [0.3.23] - 2026-06-06
### Changed
- 📝 Refreshed User Manual in `README.md` and `docs/USER_MANUAL.md` to ensure all current commands and skills are documented.
- 🚀 Bumped version to 0.3.23.
- 🤖 Maintenance run by gc-skillume-bot-v0_2.

## [0.3.22] - 2026-06-05
### Changed
- 📝 Refreshed User Manual in `README.md` and `docs/USER_MANUAL.md` with more detailed descriptions and "Wow Factor" examples.
- 🚀 Bumped version to 0.3.22.
- 🤖 Maintenance run by `gc-skillume-bot-v0_2`.

## [0.3.21] - 2026-06-04
### Changed
- 📝 Refreshed User Manual in `README.md` and `docs/USER_MANUAL.md`.
- 🤖 Maintenance run by `gc-skillume-bot-v0_2`.

## [0.3.20] - 2026-05-30
### Added
- 🎵 Added new `seby-6-anni` MP3 and text script to `musicgen-lyria3` skill.
### Changed
- 🤖 Maintenance run and commit by `gc-skillume-bot-v0_2`.

## [0.3.19] - 2026-05-27
### Changed
- 🤖 Maintenance run by `gc-skillume-bot-v0_2`.
- 🧹 Routine checks and minor updates.

## [0.3.18] - 2026-05-26
### Changed
- 🤖 Maintenance run by `gc-skillume-bot-v0_2`.
- 🧹 Routine checks and minor updates.

## [0.3.17] - 2026-05-25
### Changed
- 🤖 Maintenance run by `gc-skillume-bot-v0_2`.
- 🛠️ Routine checks and synchronization.

## [0.3.16] - 2026-05-24
### Fixed
- 📝 Added missing SRE Commands section to `USER_MANUAL.md` and `README.md`.
- 🤖 Secondary maintenance run by `gc-skillume-bot-v0_2`.

## [0.3.15] - 2026-05-24
### Changed
- 🤖 Maintenance run by `gc-skillume-bot-v0_2`.
- 🛠️ Routine checks and synchronization.

## [0.3.14] - 2026-05-22
### Changed
- 📝 Cleaned up `README.md` and `docs/USER_MANUAL.md` to remove references to deprecated/removed postmortem skills and commands.
- 🤖 Maintenance run by `gc-skillume-bot-v0_2`.
- 🛠️ Routine checks and synchronization.

## [0.3.13] - 2026-05-20
### Removed
- 🔥 Completely removed `postmortem-generator` and `postmortem-aggregator` skills as they have been fully migrated to the official SRE extension (`palladius/sre`) -- made with AntiGravity.

## [0.3.12] - 2026-05-19
### Added
- ✨ [musicgen-lyria3] Committing untracked generated music and text files (sebi-lido-estensi, sebi-hot-wheels). (-- made with Gemini CLI by gc-skillume-bot-v0_2)

## [0.3.11] - 2026-05-07
- 🤖 Maintenance run by `gc-skillume-bot-v0_2`: Fixed typo in `GEMINI.md` and standardized CHANGELOG format.

## [0.3.10] - 2026-05-06
### Fixed
- 🐛 [musicgen-lyria3] Fixed silent failure bug: scripts now exit with 1 if destination directory is missing or on any generation error.
- 🤖 Maintenance run by `gc-skillume-bot-v0_2`.

## [0.3.10] - 2026-05-05
- 📝 Anonymize project ID in genmedia-setup sample settings. -- made with gc-skillume-bot-v0_2

## [0.3.9] - 2026-05-03
### Changed
- 🤖 Maintenance run: Updated skill metadata schemas to use `metadata.version` and `compatibility`.
- 🤖 Signed: gc-skillume-bot-v0_2.

## [0.3.8] - 2026-04-29

## [0.3.7] - 2026-04-22
### Added
- 📝 Standardized `SKILL.md` headers with `version` and added missing `CHANGELOG.md` for 5 skills: `cloud-build-investigation`, `devrel-frictionlog-codelab`, `pcc-check-for-updates`, `postmortem-aggregator`, and `postmortem-generator` -- gc-skillume-bot-v0_2.

## [0.3.6] - 2026-04-21
### Fixed
- 🎵 Improved `musicgen-lyria3` scripts with better API key handling and updated GenAI SDK response parsing -- gc-skillume-bot-v0_2.

## [0.3.5] - 2026-04-19
### Changed
- 📝 Refreshed User Manual in README.md and docs/USER_MANUAL.md -- gc-skillume-bot-v0_2.

## [0.3.4] - 2026-04-17
### Changed
- 🚨 Marked `postmortem-create` and related skills as `[DEPRECATED]` and `[MIGRATED]`, pointing to the official `sre` extension repository -- made with AntiGravity.

## [0.3.3] - 2026-04-17
### Changed
- 🎵 Tracked the latest generated `musicgen-lyria3` assets from 2026-04-16 -- gc-skillume-bot-v0_2.

## [0.3.2] - 2026-04-16
### Fixed
- 🎵 Actually tracked the generated `musicgen-lyria3` assets promised in previous version -- gc-skillume-bot-v0_2.

## [0.3.1] - 2026-04-15
### Changed
- 🎤 Improved `musicgen-lyria3` scripts with better safety filter handling and updated GenAI SDK response parsing -- gc-skillume-bot-v0_2.
- 🔧 Added untracked generated assets for `musicgen-lyria3`.

## [0.3.0] - 2026-03-30
### Removed
- 🎬 Removed `commands/aicinema/` custom commands. All functionality (storyboarding, act structure, quality production) has been migrated to the `genmedia-setup` skill.
### Changed
- 📝 Updated `README.md` and `docs/USER_MANUAL.md` to reflect the `aicinema` migration.
- 🚀 Bumped extension version to 0.3.0.

## [0.2.2] - 2026-03-30
### Added
- 🎥 Final migration of "AI Cinema" quality logic to `genmedia-setup` skill (0.1.2):
  - Added persona integration from `doc/personas/`.
  - Added structured project organization (`PLAN.md`, `README.md`).
  - Added multi-lingual naming conventions and trailer production logic.
- 🚀 Bumped extension version to 0.2.2.

## [0.2.1] - 2026-03-30
### Added
- 🍌 Updated `genmedia-setup` skill (0.1.1) with new Nano Banana models: `gemini-2.5-flash-image`, `gemini-3-pro-image-preview`, and `gemini-3.1-flash-image-preview`.
- 🚀 Bumped extension version to 0.2.1.

## [0.2.0] - 2026-03-30
### Added
- 🎬 Major restructuring of `genmedia-setup` skill:
  - Extracted installation details to `references/install.md`.
  - Added "Four-Act Structure" storyboarding logic.
  - Added guidelines for style continuity and audio sanitization.
  - Bumped skill to 0.1.0 and extension to 0.2.0.

## [0.1.13] - 2026-03-30
### Changed
- 📝 Added versioning to the `genmedia-setup` skill (bumped to 0.0.3).
- 📜 Added skill-specific `CHANGELOG.md` for `genmedia-setup`.
- 📝 Expanded model descriptions in `which_models.md` with official documentation links.
- 🚀 Bumped extension version to 0.1.13.

## [0.1.12] - 2026-03-30
### Changed
- 🔄 `genmedia-setup` skill now defaults to `mcp-nanobanana-go` for the `imagen` command.
- 📝 Consolidated model recommendations for Imagen, Veo, Lyria (with lyric support), and Chirp in `which_models.md`.
- 🎤 Documented specific GA regions for Chirp 2 (`us-central1`, `europe-west4`, `asia-southeast1`) and Chirp 3 (`us`, `eu`).
- 🚀 Bumped extension version to 0.1.12.

## [0.1.11] - 2026-03-30
### Fixed
- 🎤 Updated `chirp-2` GA regions: `us-central1`, `europe-west4`, and `asia-southeast1`.
- 🚀 Bumped extension version to 0.1.11.

## [0.1.10] - 2026-03-30
### Fixed
- 🎤 Corrected Chirp 3 availability information: GA in `us` and `eu` multi-regions.
- 🚀 Bumped extension version to 0.1.10.

## [0.1.9] - 2026-03-30
### Added
- 🎤 Added Chirp 2 and Chirp 3 models to `which_models.md` with regional availability notes (Chirp 3 only in US/EU).
- 🚀 Bumped extension version to 0.1.9.

## [0.1.8] - 2026-03-30
### Added
- 🎵 Added Lyria 3 models (`lyria-3-clip-preview`, `lyria-3-pro-preview`) with lyric support to `which_models.md`.
- 🚀 Bumped extension version to 0.1.8.

## [0.1.7] - 2026-03-30
### Changed
- 🔄 Updated `genmedia-setup` to use `mcp-nanobanana-go` instead of `mcp-imagen-go`.
- 📝 Added `which_models.md` reference to `genmedia-setup` skill for easy access to recommended models.
- 🚀 Bumped extension version to 0.1.7.

## [0.1.6] - 2026-03-30
### Changed
- 🔄 `genmedia-setup` script now automatically enables Vertex AI, Text-to-Speech, and Storage APIs.
- 📝 Added mandatory prerequisites (`ffmpeg`, `ADC login`, IAM bindings) to `genmedia-setup` SKILL.md.

## [0.1.5] - 2026-03-30
### Added
- ✨ Added `genmedia-setup` skill to install GenMedia MCP binaries, skills, and inject JSON configurations for Vertex AI Creative Studio tools.

## [0.1.4] - 2026-03-30
### Added
- Added `musicgen-lyria3` skill (moved from public-goodies).

## [0.1.3] - 2026-03-13
### Changed
- 🥑 Enforced stricter rules before proceeding to the next page in the `devrel-frictionlog-codelab` skill (v0.0.3).

## [0.1.2] - 2026-03-13
### Changed
- 🥑 Enforced strict billing setup and automated YOLO mode suggestions in the `devrel-frictionlog-codelab` skill (v0.0.3).
- 🥑 Added also a MEtadata table to Friction Log final doc.

## [0.1.1] - 2026-03-13
### Changed
- 🥑 Improved `devrel-frictionlog-codelab` skill (v0.0.2):
    - Added consolidated `FRICTION_LOG.md` output with visual diffs and concatenated logs.
    - Added mandatory `HH:MM:SS` timestamps to all log entries.
    - Added automated Time Analysis (AI vs Codelab estimate vs Human suggestion) at the end of each page.
    - Bumped extension version to 0.1.1.

## [0.1.0] - 2026-03-13
### Added
- ✨ Added `devrel-frictionlog-codelab` skill v0.1.0: automates the process of executing a Codelab, extracting its content to Markdown, creating a deterministic scaffold, and recording friction logs for DevRel evaluation.

## [0.0.33] - 2026-03-11
### Changed
- 🔄 Bumped version and checked repository updates -- gc-skillume-bot-v0_1.

## [0.0.32] - 2026-03-10
### Added
- ✨ Added `postmortem-aggregator` skill.
- ✨ Updated `postmortem-generator` skill with versioning and formatting fixes.

## [0.0.31] - 2026-03-06
### Added
- ✨ Added emojis to skill descriptions (🔄, 🏗️, 💀).

## [0.0.30] - 2026-03-06
### Fixed
- 🔄 Aligned `post-mortem` directory with internal name `postmortem-generator`.

## [0.0.29] - 2026-03-06
### Fixed
- 🔄 Renamed `check-for-updates` skill to `pcc-check-for-updates` internally and directory-wise.

## [0.0.28] - 2026-03-06
### Fixed
- 🔄 Renamed `pr-creator` skill to `pr-creator-copy` internally to match directory naming.

## [0.0.26] - 2026-01-26
### Changed
- **SRE PostMortem**: Reverted Action Items to table format for better structured view, while keeping Timeline as bullet points for better density.

## [0.0.25] - 2026-01-20
### Changed
- **SRE Commands & Skills**:
  - Updated `postmortem-create.toml` and `skills/post-mortem/SKILL.md`:
    - Timeline and Action Items use bullet points instead of tables for better density.
    - Added permalink support for commits, bugs, and other resources.
    - Updated timeline milestone colors for better readability.

## [0.0.24] - 2026-01-14
### Added
- **PDA Workflow**: Added `commands/code/pda.toml` for the Plan, Define, Act workflow.

## [0.0.23] - 2026-01-13
### Added
- **Skills Support**: Initial support for skills in extensions.
- **PostMortem Skill**: Added `skills/post-mortem/SKILL.md` (copied from custom command).
- **PR Creator Skill**: Added `skills/pr-creator-copy/SKILL.md` (copied from Gemini CLI).
