---
name: conductor-worktree-hitl
description: "Manage asynchronous task implementation in Git Worktrees using Conductor++ and GitHub Issues for low-friction HITL choice prompting and screenshot verification."
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

### 2. Conductor Quality Gates & Plan Roast
1.  Verify the track's `metadata.json` configuration. Populate the `"worktree"` and `"github_issue"` blocks.
2.  Before coding, execute the Conductor `/roastme` command to analyze the `plan.md` against product guidelines and code style rules.
3.  If `/roastme` identifies unresolved design constraints, proceed to the communication protocol.

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
5.  **Enter Polling Sleep**: Periodically read `metadata.json` (every 15 seconds). Once the local polling script updates the question status to `"answered"`, extract the `"answer"` value, clear the question from the local queue, and resume.

### 4. Verification & Push
1.  Implement the feature to pass all tests.
2.  Run the linting suite and verify test coverage meets style requirements (>80%).
3.  Commit changes, push to origin, and attach a detailed summary using Git Notes:
    ```bash
    git notes add -m "Task completed: <summary>" <commit-hash>
    ```
4.  Open a Pull Request and mark the task as `completed` in `metadata.json`.
