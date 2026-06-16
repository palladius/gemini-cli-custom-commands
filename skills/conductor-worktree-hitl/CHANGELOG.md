# Changelog - Conductor Worktree HITL Skill

All notable changes to the `conductor-worktree-hitl` skill will be documented in this file.

---

## [0.3.43] - 2026-06-16
### Added
- 🤖 **Agent & Worktree Tracking**: Re-implemented `AGENT` column and `🌳` (worktree emoji) detection columns in `conductor-inspector` script, which scans `.worktrees/` directory and parses track metadata files.

## [0.3.42] - 2026-06-16
### Added
- 📊 **Location-Aware Last Changed Timestamp**: Added a `CHANGED` column in `conductor-inspector` showing when a track was last touched. It parses and compares both GitHub Issue timestamps (🐙) and local metadata/mtime updates (💻), showing the latest active timestamp.
- 🔀 **Recent-On-Top Sorting**: Refactored track sorting to display the most recently active/changed tracks first.
- 🕒 **Adaptive Relative Timestamps**: Displays changes within the last 24 hours as relative duration (e.g. `16min`, `1h5m`) and older changes in relative days (`XXdays`), improving layout readability.
- 🧹 **Compact Status Layout**: Removed brackets `[ ]` from the short-mode `STATUS` column and changed it to left-justify (`STATUS     ` instead of `[  STATUS   ]`), saving 4 bytes of terminal prefix width.
- 📝 **Execution Documentation**: Added sample execution output under `skills/conductor-worktree-hitl/references/inspector-execution.txt`.

## [0.3.41] - 2026-06-16
### Changed
- 📝 **Prompt Simplification**: Replaced long prompt with a minimal version that delegates Benjamin-specific conventions to `GEMINI.md` and worktree workflow steps to the `conductor-worktree-hitl` skill.

## [0.3.40] - 2026-06-16
### Added
- 📝 **Vehicle Field in Question Schema**: Added a `"vehicle"` block to `references/question-answered.json` to track the delivery mechanism (medium, source/person, and type, e.g. telegram audio, peer agent Nino).

## [0.3.39] - 2026-06-16
### Changed
- 📝 **Skill Reference Documenting**: Referenced `references/question-awaiting.json` and `references/question-answered.json` schemas in `SKILL.md` under the local memory registry section.

## [0.3.38] - 2026-06-16
### Changed
- 📝 **GHI Signature Alignment**: Updated the starter prompt to explicitly enforce GHI comment format `[QUESTION][<AgentName>]` and signing with `-- from <AgentName> on behalf of Riccardo` (using emojis) for consistency.

## [0.3.37] - 2026-06-16
### Changed
- 📝 **Rename Tag Signature**: Renamed the GHI comment tracking tag signature from `conductruelle` to `conductree` across the starter prompt.

## [0.3.36] - 2026-06-16
### Changed
- 📊 **Conductor Inspector**: Added the **GHI** (GitHub Issue) column to `--short` mode output to track issue numbers for each track.

## [0.3.35] - 2026-06-16
### Added
- 📝 **Reference Questions**: Added reference JSON files (`question-awaiting.json` and `question-answered.json`) under `references/` directory to demonstrate metadata-based question states.

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
- 🛡️ **Git Hygiene Step**: Added instructions in `SKILL.md` to configure git exclude inside worktrees to prevent symlink tracking.

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
