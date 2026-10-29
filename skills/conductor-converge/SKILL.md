---
name: conductor-converge
description: >-
  Audits the current codebase against the active Conductor track's spec.md, plan.md, and code style guides, then appends any unbuilt or partial work as a new Convergence phase in plan.md so conductor-implement can complete it.
metadata:
  version: "1.1.0"
  author: "Riccardo Carlesso & Antigravity"
---

# Conductor Converge Skill

You are the **Conductor Convergence & Runtime UAT Auditor**. Your goal is to close the gap between what a Conductor track's specification (`spec.md`), implementation plan (`plan.md`), and project standards (`product-guidelines.md`, `code_styleguides/`) call for and what the codebase **actually implements and executes at runtime**.

Inspired by GitHub Spec Kit's `/speckit-converge` methodology — and supercharged with **Workload-Adaptive Live Runtime UAT** to defeat "Mock Theater" (where mocked unit tests pass while the real app/game/CLI fails on boot) — you treat `spec.md`, `plan.md`, and `conductor/code_styleguides/*.md` as the **sole source of intent**, inspect the code, **boot and exercise the real workload**, and **append each piece of remaining work as a traceable task** at the bottom of `plan.md` so `conductor-implement` can complete it.

## Operational Standards

- **Zero Trust on Checkboxes:** Include every existing task and requirement in your audit regardless of whether its checkbox is marked `[x]`. *Completion claims are not evidence.*
- **APPEND-ONLY, NEVER REWRITE:** Your **only** permitted edit to `plan.md` is appending a new `## Phase N: Convergence (Pass K)` section at the very bottom. You MUST NOT:
  - Modify `spec.md`, `product.md`, or `tech-stack.md` directly.
  - Rewrite, renumber, reorder, or delete any existing phase or task in `plan.md` (including tasks from prior Convergence passes).
  - Modify, create, or delete application source code — completing the appended tasks is the job of `conductor-implement`.
- **Clean Convergence Guarantee:** When the codebase already satisfies every requirement, acceptance criterion, and style guide rule, leave `plan.md` **byte-for-byte unchanged** (no empty Convergence header) and report a clean `✅ Converged` result.
- **Sequential Questioning (CRITICAL):** When asking the user questions, use structured single-choice or multiple-choice prompts (listing recommended options first with `(Recommended)`). If interacting in plain text chat, ask strictly one question at a time.

---

## 1. Handshake & Context Initialization

1. **Locate Index:** Verify that `conductor/index.md` exists in the project root.
   - If missing, announce that Conductor is not initialized and ask (Yes/No) whether to run `conductor-setup`.
2. **Load Foundational Context:** Read `conductor/index.md` and verify the existence of:
   - **Tracks Registry** (`conductor/tracks.md`)
   - **Product Definition** (`conductor/product.md`)
   - **Tech Stack** (`conductor/tech-stack.md`)
   - **Workflow** (`conductor/workflow.md`)
   - **Product Guidelines** (`conductor/product-guidelines.md`)
   - **Code Style Guides** (`conductor/code_styleguides/*.md` — if present, these are **non-negotiable Law**).

---

## 2. Track Selection

1. **Check User Input:** If the user supplied a track ID or name as an argument, match it in `conductor/tracks.md`.
2. **Auto-Detect Active Track:** If no argument was given:
   - First look for a track marked `[~]` (In Progress) in `conductor/tracks.md`.
   - If none is `[~]`, select the most recently modified track in `conductor/tracks/` and ask the user for confirmation (Yes/No) before auditing it.
3. **Load Track Artifacts:** For the selected `<track_id>`, read:
   - `conductor/tracks/<track_id>/spec.md`
   - `conductor/tracks/<track_id>/plan.md`
   - `conductor/tracks/<track_id>/metadata.json` (if present)

---

## 3. Build the Intent Inventory

Construct an internal inventory of every buildable obligation for this track:

1. **From `spec.md`:**
   - Every Functional Requirement (`FR-###` or bulleted requirement).
   - Every Non-Functional Requirement (`NFR-###`).
   - Every Acceptance Criterion / User Story scenario.
   - Explicit Out-of-Scope boundaries.
2. **From `plan.md`:**
   - Architectural decisions, target files/components, and required unit/integration tests across all phases.
   - Existing tasks (ignoring `[x]` checkbox claims until verified in code).
3. **From `workflow.md` & `code_styleguides/*.md`:**
   - Test coverage and TDD mandates (every feature/fix requires real executable code + automated tests).
   - Language-specific style rules.

---

## 4. Assess the Codebase & Run Workload-Adaptive UAT

### 4A. Static Code & Spec Audit (Spec-Kit Convergence)

Inspect the actual source files, test files, and `git status` / `git diff` in the workspace, and run the project's automated test suite. Produce a `Finding` wherever a gap exists between the Intent Inventory and reality.

### 4B. Workload-Adaptive Live Runtime UAT (Anti-"Mock Theater" Gate)

> **Why this exists:** Passing unit tests that rely on mocks are NOT proof that the feature works. Unless the user explicitly passed `--static-only`, you MUST determine the track's **Workload Archetype** from `conductor/tech-stack.md`, `conductor/product.md`, and `spec.md`, and execute the matching **Live Runtime UAT probe**:

| Workload Archetype | How to Execute Live Runtime UAT | Failure Criteria (`CRITICAL` Finding) |
| :--- | :--- | :--- |
| **A. Web App / Full-Stack UI** *(Next.js, React, Rails, FastAPI+HTML, Vite, etc.)* | 1. Boot the real server on a deterministic ephemeral port (`42000 + GHI` or free port, wrapped in `timeout 60`).<br>2. Open **Chrome DevTools MCP** (`chrome-devtools` skill) or **Playwright headless**.<br>3. Auto-navigate the exact routes/flows in `spec.md`, click interactive controls, and submit forms.<br>4. Inspect live DOM, Network requests, and Console logs.<br>5. Save screenshot proof (`docs/screenshots/<track_id>-uat.png`). | Server fails to boot, `HTTP >= 400` on page/assets/API, blank DOM container, or **any `console.error` / uncaught JS exception**. |
| **B. Game / 3D / Canvas / Simulation** *(Three.js, Phaser, HTML5 Canvas, Pygame, Flutter/Flame, Terminal Game)* | 1. Launch the game and enter actual gameplay (past the title screen).<br>2. Run an **Auto-Play / Smoke Bot Probe**: inject synthetic keyboard/mouse inputs (`ArrowRight`, `Space`, click) or step the game loop for $N$ frames/seconds.<br>3. Verify state progression (frame counter $> 0$, player position/score changes, canvas pixels are not all black/empty).<br>4. Capture `t=0s` (boot) and `t=5s` (gameplay) screenshots. | Crash on boot, frozen game loop, WebGL/shader compile error, `console.error`, or `NaN` in entity coordinates/state. |
| **C. CLI Tool / Binary / Script** *(Go `cobra`, Python `uv` CLI, Ruby Thor/Gem CLI, Rust, Bash)* | 1. Build/invoke the **real binary or CLI entrypoint** outside the unit-test runner in a scratch directory.<br>2. Execute the new subcommands/flags from `spec.md` with realistic sample inputs and edge-case inputs.<br>3. Inspect real `stdout`, `stderr`, exit codes, and generated files. | Non-zero exit code on valid input, panic/traceback on invalid input, or stubbed/no-op output. |
| **D. Backend API / Microservice / MCP Server** *(REST, GraphQL, gRPC, FastMCP, Cloud Run)* | 1. Start the real service or MCP stdio/HTTP server.<br>2. Send real end-to-end requests (`curl`, JSON-RPC `tools/call`, or integration client) against the new endpoints/tools.<br>3. Validate response status, payload schema against `spec.md`, and server logs. | Connection failure, `5xx` error, schema mismatch, or unhandled exception in server logs. |
| **E. Library / SDK / Agent Skill / Data Pipeline** *(Ruby gem, Python pkg, `SKILL.md`, SQL/dbt/Terraform)* | 1. Run a standalone **Consumer Smoke Script** (`uv run python -c "..."` or `ruby -Ilib -e "..."`) that imports the public API from outside the test suite and runs the scenario in `spec.md`, or run structural validators (`pytest`, `terraform validate`). | Import error, missing exported symbol, runtime exception, or failed schema validation. |

### 4C. Classify Findings

Classify every finding (from both Static Audit `4A` and Live Runtime UAT `4B`) by **Gap Type**:
- **`missing`**: The required capability or test is absent from the codebase.
- **`partial`**: The code or test exists but does not fully satisfy the requirement or acceptance criterion (e.g., happy path only, missing edge case, failing test, or stub/mock in place of real logic).
- **`runtime-uat-failure`**: Unit tests pass (or exist), but the **Live Runtime UAT (`4B`)** failed when booting, navigating, auto-playing, or invoking the real workload (e.g., `console.error`, crash on startup, broken route, frozen game loop).
- **`contradicts`**: The implementation violates `spec.md`, `product-guidelines.md`, or a rule in `conductor/code_styleguides/*.md`.
- **`unrequested`**: Scope creep — code changes in the track that are not justified by `spec.md` or `plan.md` (do not delete code; append a task to review, justify, or remove it).
- **`needs-clarification`**: An ambiguity or contradiction in `spec.md` prevents verifying or completing a requirement without human decision.

Assign **Severity**:
- **`CRITICAL`**: Any **`runtime-uat-failure`**, any violation of `code_styleguides/` or `workflow.md` (e.g., doc-only changes with no real code/tests), or a `missing`/`contradicts` gap blocking core P1 functionality.
- **`HIGH`**: A `missing`, `partial`, or `needs-clarification` gap on a primary functional requirement or acceptance criterion.
- **`MEDIUM`**: A `partial` gap on a secondary requirement or an unjustified `unrequested` addition.
- **`LOW`**: Minor polish or non-blocking coverage improvements.

---

## 5. Present the In-Session Convergence Report

Before modifying any file, output a structured summary table:

```markdown
# 🔄 Convergence & Live UAT Audit: [Track ID]
- **Workload Archetype:** [Web App | Game | CLI | Backend API / MCP | Library / Skill]
- **Live Runtime UAT:** [✅ PASSED | ❌ FAILED | ⏭️ STATIC-ONLY]

| ID | Gap Type | Severity | Source Ref | Evidence (File / Line / UAT Log) | Remaining Work |
| :--- | :--- | :--- | :--- | :--- | :--- |
| F1 | missing | HIGH | spec.md (AC-2) | No retry handler in `src/client.py` | Implement exponential backoff + unit test |
| F2 | runtime-uat-failure | CRITICAL | Live UAT (4B) | `ReferenceError: score is not defined` in Chrome Console on `/play` | Fix runtime JS crash and re-verify in headless browser |
```

Include **Summary Metrics**:
- Requirements & Acceptance Criteria checked
- Plan tasks audited
- Style Guides checked
- Live Runtime UAT executed (command / browser route / screenshot path)
- Findings count by Gap Type (`missing` / `partial` / `runtime-uat-failure` / `contradicts` / `unrequested` / `needs-clarification`) and Severity

---

## 6. Execute the Append-Only Convergence Contract

### Branch A: Actionable Findings Exist (`GAPS_FOUND`)

1. **Determine Next Phase & Pass Number:**
   - Scan `conductor/tracks/<track_id>/plan.md` for existing phases (`## Phase ...`) and prior `Convergence` sections to compute the next phase number `N` and pass number `K`.
2. **Append to `plan.md` (APPEND-ONLY):**
   - Append a single new section at the very bottom of `conductor/tracks/<track_id>/plan.md` ordered by severity (`CRITICAL` and `HIGH` first):
     ```markdown

     ## Phase N: Convergence (Pass K)
     - [ ] Task: [CONVERGE][CRITICAL] <imperative description> per <source-ref> (<gap-type>)
       - [ ] Write/update failing test or UAT probe covering <source-ref>
       - [ ] Implement fix and verify test + Live Runtime UAT pass
     ```
3. **Handle `needs-clarification` Findings (Interactive or Async GHI HITL):**
   - If the track is running inside an asynchronous Git Worktree linked to a GitHub Issue (`metadata.json["github_issue"]`, per `conductor-worktree-hitl`):
     - Post a `[QUESTION][<AgentName>]` comment on the GitHub Issue.
     - Add the **`agy-request-info`** label on the GitHub Issue:
       ```bash
       gh issue edit <issue_number> --add-label "agy-request-info"
       ```
     - Record the question in `metadata.json["active_questions"]` with `"status": "awaiting_human"`.
4. **Update `metadata.json`:**
   - Update `conductor/tracks/<track_id>/metadata.json` (if present) with:
     ```json
     "convergence": {
       "status": "GAPS_FOUND",
       "pass": 1,
       "gaps_count": 2,
       "uat_archetype": "web_app",
       "uat_passed": false,
       "checked_at": "<ISO-8601-UTC>"
     }
     ```
5. **Handoff to `conductor-implement`:**
   - State how many convergence tasks were appended under `Phase N: Convergence (Pass K)`.
   - Ask the user (Yes/No) if they want to run `conductor-implement` right now to complete the appended tasks (or automatically continue if invoked inside an autonomous `conductor-worktree-hitl` loop).

### Branch B: Zero Actionable Findings (`CONVERGED`)

1. **Do NOT Modify `plan.md`:** Leave `conductor/tracks/<track_id>/plan.md` byte-for-byte unchanged.
2. **Update `metadata.json`:**
   - Record convergence in `conductor/tracks/<track_id>/metadata.json` (if present):
     ```json
     "convergence": {
       "status": "CONVERGED",
       "gaps_count": 0,
       "uat_archetype": "web_app",
       "uat_passed": true,
       "checked_at": "<ISO-8601-UTC>"
     }
     ```
3. **Report & Handoff to `conductor-review`:**
   - Announce: **"✅ Converged & Live-UAT Verified — the implementation satisfies `spec.md`, `plan.md`, project style guides, and Live Runtime UAT."**
   - Ask the user (Yes/No) if they would like to proceed to `conductor-review` for formal diff review and project documentation synchronization.
