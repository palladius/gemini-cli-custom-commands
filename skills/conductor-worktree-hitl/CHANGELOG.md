# Changelog - Conductor Worktree HITL Skill

All notable changes to the `conductor-worktree-hitl` skill will be documented in this file.

This changelog is contextually bound to the Condutree skill itself. Version numbers represent the skill's release versions.

---

## [2.1.0] - 2026-07-08
### Added
- 📊 **Reference Justfile Recipes**: Added `conductor-status` (`--open --short`) and `conductor-status-all` (`--all --short`) recipes to `references/justfile` so new projects get them out of the box.
### Changed
- 📝 **Comment Fix**: Clarified `git-status-condutree` comment from "Aggregated status check" to "Aggregated git status check" to distinguish from `conductor-status`.

---

## [2.0.1] - 2026-07-07
### Changed
- 🧹 **Manual Cleanup**: Removed the obsolete `Proposed GHI: condutree v2.0 Roadmap & Streamlining` section from the end of `SKILL.md`.
- 📝 **Documentation Addition**: Created a comprehensive [USER_MANUAL.md](file:///usr/local/google/home/ricc/git/skillume/gemini-cli-custom-commands/skills/conductor-worktree-hitl/docs/USER_MANUAL.md) detailing setup, execution flow, scripts, and state JSON structures.

---

## [2.0.0] - 2026-07-07
### Added
- 🌳 **Condutree v2.0 Released**:
  - Implemented automated `.env` configurations symlinking alongside the central `conductor/` folder in `SKILL.md` setup instructions.
  - Implemented local git exclude rules for `.env` inside worktrees.
  - Completed all items on the implementation checklist.

---

## [1.0.0] - 2026-07-07
### Added
- 🌳 **Condutree v2.0 Implementation**:
  - Implemented `git_status_patched.py` Python aggregator script under `scripts/` to walk and summarize active worktrees.
  - Implemented `git-status-patched.sh` wrapper script.
  - Exposed `just git-status-condutree` in the root `justfile` for easy status checking.
  - Added unit test `git_status_patched_test.py` for verification.

---

## [0.0.11] - 2026-06-19
### Added
- 🌳 **Condutree v2.0 Roadmap**: Appended a structured GHI feature proposal to `conductor-worktree-hitl/SKILL.md` outlining the next major version of the worktree orchestration skill. Proposed features include automated `.env` symlinking alongside the shared `conductor/` folder, a new `conductor/bin/git_status_patched.py` status aggregator script (walks all `.worktrees/`, parses `metadata.json`, runs `git status --porcelain`), and a `just git-status-condutree` target in the root `justfile`.
- 🛠️ **Conflict Resolution default**: Added instructions in `SKILL.md` to resolve conflicts deterministically (e.g. if different agents work on different worktrees and need a web server on port 8080, use port 42000 + GitHub Issue instead).
- 📂 **Script Installation**: Updated instructions to copy scripts in `scripts/` to `GIT_REPO/conductor/bin/` so they can be called locally, recommending a startup diff check.

### Changed
- 📊 **Conductor Inspector — Total Summary Line**: Added a final summary row to `conductor-inspector` output showing aggregate track counts and overall task completion ratio (e.g. `8/20 tasks done`).
- 📝 **Explicit Agent Field Required**: Updated `SKILL.md` to mandate that subagents set `"agent": "<AgentName>"` explicitly at the root of `metadata.json` to prevent incorrect inference from generic worktree directory paths.
- 🤖 Maintenance run by `gc-skillume-bot-v0_2`.

---

## [0.0.10] - 2026-06-16
### Added
- 🤖 **Agent & Worktree Tracking**: Re-implemented `AGENT` column and `🌳` (worktree emoji) detection columns in `conductor-inspector` script, which scans `.worktrees/` directory and parses track metadata files.

---

## [0.0.9] - 2026-06-16
### Added
- 📊 **Location-Aware Last Changed Timestamp**: Added a `CHANGED` column in `conductor-inspector` showing when a track was last touched. It parses and compares both GitHub Issue timestamps (🐙) and local metadata/mtime updates (💻), showing the latest active timestamp.
- 🔀 **Recent-On-Top Sorting**: Refactored track sorting to display the most recently active/changed tracks first.
- 🕒 **Adaptive Relative Timestamps**: Displays changes within the last 24 hours as relative duration (e.g. `16min`, `1h5m`) and older changes in relative days (`XXdays`), improving layout readability.
- 🧹 **Compact Status Layout**: Removed brackets `[ ]` from the short-mode `STATUS` column and changed it to left-justify (`STATUS     ` instead of `[  STATUS   ]`), saving 4 bytes of terminal prefix width.
- 📝 **Execution Documentation**: Added sample execution output under `skills/conductor-worktree-hitl/references/inspector-execution.txt`.

---

## [0.0.8] - 2026-06-16
### Changed
- 📝 **Prompt Simplification**: Replaced long prompt with a minimal version that delegates Benjamin-specific conventions to `GEMINI.md` and worktree workflow steps to the `conductor-worktree-hitl` skill.

---

## [0.0.7] - 2026-06-16
### Added
- 📝 **Vehicle Field in Question Schema**: Added a `"vehicle"` block to `references/question-answered.json` to track the delivery mechanism (medium, source/person, and type, e.g. telegram audio, peer agent Nino).

---

## [0.0.6] - 2026-06-16
### Changed
- 📝 **Skill Reference Documenting**: Referenced `references/question-awaiting.json` and `references/question-answered.json` schemas in `SKILL.md` under the local memory registry section.

---

## [0.0.5] - 2026-06-16
### Changed
- 📝 **GHI Signature Alignment**: Updated the starter prompt to explicitly enforce GHI comment format `[QUESTION][<AgentName>]` and signing with `-- from <AgentName> on behalf of Riccardo` (using emojis) for consistency.

---

## [0.0.4] - 2026-06-16
### Changed
- 📝 **Rename Tag Signature**: Renamed the GHI comment tracking tag signature from `conductruelle` to `conductree` across the starter prompt.
- 📊 **Conductor Inspector**: Added the **GHI** (GitHub Issue) column to `--short` mode output to track issue numbers for each track.
- 📝 **Reference Questions**: Added reference JSON files (`question-awaiting.json` and `question-answered.json`) under `references/` directory to demonstrate metadata-based question states.
- 👩 **Renamed Git Concierge**: Renamed the coordinator agent from Giovanni to Agostina (Lead Git Concierge) to align with the A.G. (Antigravity) theme.
- 🤖 **Optimized Polling Loop**: Refactored `poll_ghi_questions.py` to scan local Conductor tracks metadata first and only perform GitHub API calls for issues that actively have questions awaiting human input, saving over 95% of API requests.
- 🛡️ **Disable Remote Pushing**: Updated `SKILL.md` and the orchestration prompt to explicitly forbid subagents from executing `git push`. Subagents now commit locally to their branches, leaving merging and remote pushing strictly to the parent coordinator (Agostina).
- 📝 **Orchestration Prompt**: Added the `multi-worktree-starter-prompt.md` prompt for Conductor++ worktree flow.
- 🛡️ **Git Hygiene Step**: Added instructions in `SKILL.md` to configure git exclude inside worktrees to prevent symlink tracking.
- 🔀 **Conductor Inspector Sorting**: Implemented custom sorting for tracks where `NEW` status comes first, active/pending next, and `COMPLETED`/`RESOLVED`/`CLOSED` last.
- 📊 **Conductor Inspector**: Refactored `--short` mode formatting: removed brackets `[]` around the progress bar and replaced percentage (`PCT`) with `N/M` ratio (`completed/total`).
- 🔀 **Worktree HITL Skill**: Added the new `conductor-worktree-hitl` skill supporting asynchronous multi-agent coordination inside Git Worktrees using GitHub Issues and Conductor++ metadata tracking.
- 🤖 **Issue Polling Script**: Created `scripts/poll_ghi_questions.py` to aggregate and update active questions.
