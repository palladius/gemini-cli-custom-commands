---
name: conductor-worktree-hitl
description: "Manage asynchronous task implementation in Git Worktrees using Conductor++ and GitHub Issues for low-friction HITL choice prompting and screenshot verification."
meta:
  version: 2.0.1
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
4.  **Symlink the Conductor Folder & Shared Secrets**: Inside the worktree directory, create symbolic links pointing back to the main repository's `conductor/` directory and `.env` file (if present) to ensure shared configuration/secrets sync:
    ```bash
    ln -s ../../conductor conductor
    if [ -f ../../.env ]; then ln -s ../../.env .env; fi
    ```
    This ensures a single point of sync/truth for all Conductor++ metadata and environment configurations.
5.  **Configure Git Hygiene**: To prevent the subagent from accidentally tracking or staging the `conductor` symlink, track metadata, or `.env` files to its feature branch, add them to the worktree's local exclude file:
    ```bash
    echo "conductor" >> $(git rev-parse --git-dir)/info/exclude
    echo ".env" >> $(git rev-parse --git-dir)/info/exclude
    ```
6.  If conflicts arise, find a way to solve these conflicts deterministically. Eg, say different agents work on different worktrees and need to spin up a web server on port 8080, use this DEFAULT OVER CONFIGURATION instead: use port 42000 + GitHub Issue.
7. Copy the scripts in scripts/ to GIT_REPO/conductor/bin/ so they can be called from there. At startup run a diff to make sure you use the latest version. 

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

## 📊 Conductor Track JSON (metadata.json) Evolution

Every Conductor track maintains its state in a specific metadata file at a standard path:
*   **Sample Path**: `conductor/tracks/telegram_incident_creation/metadata.json`

The file structure evolves dynamically as the track is assigned to agents, linked to GitHub Issues (GHI), and processes human feedback:

### 1. Initial State (Unassigned)
When a track is first created, it starts with only basic details *(see reference file [references/track-initial.json](./references/track-initial.json))*:
```json
{
  "track_id": "telegram_incident_creation",
  "status": "NEW",
  "description": "Implement incident creation in telegram",
  "tasks": []
}
```

### 2. Assignment State (Agent & Worktree Setup)
When a subagent checks out the track, it updates `metadata.json` to assign itself (`"agent"`) and document its isolated worktree branch and path *(see reference file [references/track-assigned.json](./references/track-assigned.json))*:
```json
{
  "track_id": "telegram_incident_creation",
  "status": "ACTIVE",
  "description": "Implement incident creation in telegram",
  "agent": "Mario",
  "worktree": {
    "branch": "feature/issue-123",
    "directory": ".worktrees/issue-123-mario"
  },
  "tasks": []
}
```

### 3. Linked to GitHub Issue (GHI Integration)
When associated with a GitHub Issue (GHI), a `"github_issue"` block is populated containing the issue number:
```json
{
  "track_id": "telegram_incident_creation",
  "status": "ACTIVE",
  "description": "Implement incident creation in telegram",
  "agent": "Mario",
  "worktree": {
    "branch": "feature/issue-123",
    "directory": ".worktrees/issue-123-mario"
  },
  "github_issue": {
    "number": 123
  },
  "tasks": []
}
```

### 4. Awaiting Human Input (HITL Active)
When the subagent posts a question to the GHI, it appends the question to `"active_questions"` with `"status": "awaiting_human"`:
```json
{
  "track_id": "telegram_incident_creation",
  "status": "ACTIVE",
  "description": "Implement incident creation in telegram",
  "agent": "Mario",
  "worktree": {
    "branch": "feature/issue-123",
    "directory": ".worktrees/issue-123-mario"
  },
  "github_issue": {
    "number": 123
  },
  "active_questions": [
    {
      "agent": "Mario",
      "question": "Should we default to HTML formatting or MarkdownV2 for Telegram message payloads?",
      "status": "awaiting_human",
      "created_at": "2026-06-16T11:00:00Z"
    }
  ],
  "tasks": []
}
```

### 5. Answered State (HITL Complete)
Once the polling script parses the answer from the GHI comments, it updates the question block to `"status": "answered"`, adds the `"answer"`, and attaches the `"vehicle"` delivery details:
```json
{
  "track_id": "telegram_incident_creation",
  "status": "ACTIVE",
  "description": "Implement incident creation in telegram",
  "agent": "Mario",
  "worktree": {
    "branch": "feature/issue-123",
    "directory": ".worktrees/issue-123-mario"
  },
  "github_issue": {
    "number": 123
  },
  "active_questions": [
    {
      "agent": "Mario",
      "question": "Should we default to HTML formatting or MarkdownV2 for Telegram message payloads?",
      "status": "answered",
      "answer": "HTML is preferred for simplicity and better parsing consistency in our Telegram library.",
      "vehicle": {
        "type": "telegram",
        "medium": "audio_message",
        "delivered_by": "human",
        "original_transcript": "Hey Mario, let's go with HTML formatting, it is much easier to maintain."
      },
      "created_at": "2026-06-16T11:00:00Z"
    }
  ],
  "tasks": [],
  "updated_at": "2026-06-16T11:05:00Z"
}
```


