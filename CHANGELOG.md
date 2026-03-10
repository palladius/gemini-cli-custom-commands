# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
