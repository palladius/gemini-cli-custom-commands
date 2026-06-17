---
name: conductor-worktree-hitl
description: "Manage asynchronous task implementation in Git Worktrees using Conductor++ and GitHub Issues for low-friction HITL choice prompting and screenshot verification."
version: 0.0.10
---

# Conductor++ Asynchronous Git Worktree & GHI HITL Skill

This skill guides the agent to execute parallel software development tasks using Git Worktrees, Conductor quality gates, and GitHub Issues (GHI) for Human-in-the-Loop (HITL) communication.

## Core Flow & Execution Steps

### 1. Worktree Isolation Setup
Before performing any task modifications, create an isolated Git Worktree:
1.  Verify that the main repository is clean (`git status`).
2.  Add a new worktree check-out under `.worktrees/issue-<number>-<role>`:
    ```bash
    git worktree add .worktrees/issue-<number>-<role> -b feature/issue-<number>
    ```
3.  Navigate your context into the worktree directory. All subsequent tool runs (editing, compiling, testing) must happen within this worktree.
4.  **Symlink the Conductor Folder**: Inside the worktree directory, create a symbolic link pointing back to the main repository's `conductor/` directory:
    ```bash
    ln -s ../../conductor conductor
    ```
    This ensures a single point of sync/truth for all Conductor++ metadata and states, preventing branch conflicts on project tracking files.
5.  **Configure Git Hygiene**: To prevent the subagent from accidentally tracking or staging the `conductor` symlink or track metadata changes to its feature branch, add it to the worktree's local exclude file:
    ```bash
    echo "conductor" >> $(git rev-parse --git-dir)/info/exclude
    ```

### 2. Conductor Quality Gates & Plan Roast
1.  Verify the track's `metadata.json` configuration. Populate the `"worktree"`, `"github_issue"`, and `"agent"` blocks. You MUST explicitly set `"agent": "<AgentName>"` at the root level of `metadata.json` so that the conductor inspector knows exactly which agent is assigned to the track, avoiding incorrect inference from reused or generic worktree directory paths.
2.  **Injecting GitHub Issues as Tasks**: If specific tasks inside the track are tracked in separate GitHub Issues, use the `inject-ghi` utility to import them into the track's `"tasks"` database:
    ```bash
    ./scripts/inject-ghi --issue <number>
    ```
3.  **Handling Task-Specific Issues**:
    - If a task has a `github_issue_url` specified, fetch the issue's contents and comments for context or human input before starting.
    - When the task is complete, post a confirmation comment on the issue page.
4.  Before coding, execute the Conductor `/roastme` command to analyze the `plan.md` against product guidelines and code style rules.
5.  If `/roastme` identifies unresolved design constraints, proceed to the communication protocol.

### 3. Asynchronous Multiple-Choice Choice (`ask_me`)
If you require clarification on a design choice, UI asset, or logic condition:
1.  **Format the Question**: Create a numbered multiple-choice list with clear context and a write-in option (option 4/other).
2.  **Attach Screenshots (UI Tasks)**:
    -   If the query is visual, capture a screenshot of the local preview or simulator.
    -   Save the screenshot to the track's assets folder (e.g. `subtasks/TODAY/assets/`).
    -   Reference the raw GitHub URL or path of the screenshot in the comment.
3.  **Publish to GitHub**: Post the comment to the assigned GitHub Issue with the prefix `[QUESTION][<your-agent-role>]`.
4.  **Local Memory Registry**: Append the question structure to the `"active_questions"` array in `metadata.json`:
    ```json
    "active_questions": [
      {
        "question_id": "<unique_id>",
        "question": "<question_text>",
        "status": "awaiting_human",
        "answer": null
      }
    ]
    ```
    *(For complete schema structure, see [references/question-awaiting.json](./references/question-awaiting.json) for the open question format, and [references/question-answered.json](./references/question-answered.json) for the answered question format).*
5.  **Enter Polling Sleep**: Periodically read `metadata.json` (every 15 seconds). Once the local polling script updates the question status to `"answered"`, extract the `"answer"` value, clear the question from the local queue, and resume.

### 4. Verification & Local Commit (No Remote Pushing)
1.  Implement the feature to pass all tests.
2.  Run the linting suite and verify test coverage meets style requirements (>80%).
3.  **Commit Locally (Do NOT Push)**: Stage and commit all code changes locally to your feature branch. Under no circumstances should you run `git push`.
4.  Attach a detailed summary using Git Notes:
    ```bash
    git notes add -m "Task completed: <summary>" <commit-hash>
    ```
5.  Mark the task status as `completed` in `metadata.json`. The coordinator (Agostina) will handle checking out the branch, validation, merging, and final pushing.

---

## 🚀 Proposed GHI: condutree v2.0 Roadmap & Streamlining

**Title**: `feat(condutree): automate workspace symlinking and streamline worktree status helper (v2.0)`

### Context & Gaps in v1.0
Currently, `condutree v1.0` (this skill) relies on manual or ad-hoc shell scripts for workspace setup (symlinking the `conductor` directory, adding local git excludes) and doesn't cleanly handle `.env` configurations. Furthermore, checking the unified status of all parallel worktrees requires parsing multiple raw git commands and JSON files, creating cognitive load for human operators.

### Proposed Solution
For `condutree v2.0`, we plan to streamline these tasks by packaging the setup/status checks into a single, cohesive workflow:
1.  **Automated Shared Config Symlinking**: Automatically symlink `.env` files alongside the central `conductor/` folder to ensure subagents inherit environment secrets without manual copies.
2.  **Worktree Git Status Helper**: Implement a pure Python script under `conductor/bin/git_status_patched.py` that walks active `.worktrees/`, parses each track's `metadata.json` (extracting active questions, blocked states, and current tasks), runs `git status --porcelain` in each tree, and prints a clean, aggregated color-coded summary.
3.  **`justfile` Integration**: Package this invocation as `conductor/bin/git-status-patched.sh` and expose it via a standard `just git-status-condutree` target in the project's root `justfile`.

### Implementation Checklist
- [ ] Implement automated `.env` symlinking during isolated worktree setup.
- [ ] Create `conductor/bin/git_status_patched.py` walk and parse script.
- [ ] Expose `just git-status-condutree` target in root `justfile` wrapping `conductor/bin/git-status-patched.sh`.
- [ ] Document the updated v2.0 automation flow in the user manual.

