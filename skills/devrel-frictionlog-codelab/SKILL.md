---
name: devrel-frictionlog-codelab
version: 0.3.1
description: 🥑 [DevRel] Automates friction logging for a given Google Codelab URL (v2.0). Systematically reproduces steps, enforces outcome-based architectural assertions, proactively captures TODO screenshots, strictly prevents codelab bloat with the Less-Is-More covenant, avoids IaC/Terraform collisions, generates Synoptic Tables, and produces deterministic machine-readable telemetry (friction_log.json/yaml).
# version: in the bash script.
---

# DevRel Friction Log Codelab

This skill automates the process of going through a Google Codelab, reproducing its steps, systematically documenting the experience (a "friction log"), identifying bugs in external repositories, and producing actionable reports.

## 🚫 Golden Rules

### 1. Commit Hook Progression (Never Run 2 FLs on the Same Commit!)
* **Do NOT run multiple Friction Log iterations (`FL001`, `FL002`, ...) against the exact same unpatched Commit SHA (`X`)!**
* Every Friction Log iteration (`FLXXX`) must record the exact **Git Commit SHA and Commit Timestamp** (`git log -1 --format="%h (%ci)"`) of the repository/codelab being tested (`REPO_COMMIT_HOOK`).
* The mandatory iterative cycle is:
  1. Run **`FL001`** on initial commit `X` (recording Commit SHA `X` + its timestamp).
  2. Log all defects in `BUGS.md`, open a **GitHub Issue (GHI)** tagged with `friction-log` and `FL001`.
  3. Create a **Pull Request (PR)** attached to the GHI (`Fixes #N`), review/test it, and **merge** it into `main` to produce a new Commit SHA `Y`.
  4. Run **`FL002`** on the new commit `Y` to verify fixes and iterate until the scorecard is **100% 🟢 GREEN**.

### 2. Buganizer Hotlist Mandate (`#8950858`)
* **Whenever you create or update a Buganizer issue (`b/<BUG_ID>`) during a Friction Log campaign, you MUST tag the bug with hotlist `#8950858` (`HOTLIST+=8950858`)!**
* Note on `bugged` CLI: If `bugged` blocks AI agents (`bugged is not suitable for AI agents`), invoke it with a clean environment and place bugspec tags at the very bottom of stdin:
  ```bash
  echo -e "Friction Log update summary...\n\nHOTLIST+=8950858" | env -i PATH="$PATH" HOME="$HOME" USER="$USER" bugged edit <BUG_ID>
  ```

### 3. Multi-Iteration FL Plan & Dedicated GCP Project Pool
* In the Campaign Master `README.md` (`b<BUG_ID>-<YYYYMMDD>-frictionlog-<SLUG>/README.md`), maintain a **Master Multi-Iteration FL Plan Table (`FL001`, `FL002`, `FL003`)**.
* Assign a **different dedicated GCP Project** (e.g. from the 90-day pool `011F17-0F9CE4-E03264`) to each iteration (`FL001`, `FL002`, `FL003`) to ensure clean state isolation.
* Include **2-3 lines of explicit justification/delta** explaining what changed between Commit `X` (`FL001`) and Commit `Y` (`FL002`) to justify running the new Friction Log.

### 4. Narrative Intent vs. Executed Mechanism (Semantic Drift Check)
* **Never accept `exit 0` as proof of success:** A command returning 0 only proves valid syntax, not that the author's educational goal was achieved.
* **The Semantic Drift Invariant:** Before certifying any step, contrast the **Narrative Promise** (what the title, prose, and diagrams claim to teach) with the **Executed Mechanism** (what the commands actually perform). If the commands take a degraded shortcut or bypass the promised architecture, flag a **P1 Semantic Drift Defect**.
* **Empirical State Verification:** Always formulate an assertion that queries the live platform state directly to prove architectural compliance, rather than relying on command exit codes.

### 5. The "Less is More" Sacred Covenant: High Friction for Codelab Edits
* **Every single line added to student-facing codelab text must be weighed with a heavy heart.**
* Never bloat the codelab with 10 lines of rare edge-case workarounds, compiler warnings, or esoteric shell fixes.
* **Hierarchy of Resolution:**
  1. Fix it silently in application code, dependencies, or automated wrappers (`just recipes`, `npm test`, etc.).
  2. Add unit/integration tests in the repository test suite.
  3. Document the tribal knowledge in an **Agent Skill** (`skills/how-to-use-this-repo/references/`).
  4. Only if 50%+ of all students will hit the issue, add a concise 1-line note to the codelab.

### 6. The Proactive Visual Mandate (Eliminate Bystander Effect on TODO Screenshots)
* Whenever the agent encounters a `> 📸 TODO(riccardo): add screenshot of ...` in the codelab, it is **strictly forbidden to ignore it or leave it as a TODO**.
* The agent has live credentials, headless Chrome (`google-chrome --headless`), local ports/proxies, and running services.
* The agent MUST proactively:
  1. Trigger or render the relevant UI / terminal state.
  2. Capture, crop, and save the image into `assets/images/` and the staging directory.
  3. Replace the `TODO` with the markdown image tag and verify visual rendering.

### 7. Enforce IaC Single Source of Truth (No Terraform vs CLI Collisions)
* Infrastructure provisioned by Terraform (secrets, buckets, service accounts, databases) must **never be redundantly re-created via manual CLI commands**.
* Commands following Terraform steps must be **Pre-Flight Inspection Checklists** (e.g., `gcloud secrets describe <SECRET_NAME>`), not colliding creations (`gcloud secrets create`).

### 8. Empathize with Windows Users & Eliminate Environment Friction
* Assume 50% of students are non-expert Windows users who struggle with git, PowerShell paths, and shell environments.
* Keep copy-paste commands foolproof.
* Eliminate manual environment sourcing (`source .env`) by enforcing `set dotenv-load := true` in `justfile`.
* If an environment variable is missing (e.g., `GOOGLE_CLOUD_ACCOUNT`), scripts must output clear, actionable, copy-paste terminal remedies rather than failing with cryptic errors.

### 9. Tone Sobriety & Typography Restraint (No "Fake Wows" or AI Self-Talk)
* **Never use hyperbole or market-speak:** Eliminate fake enthusiastic claims like *"The WOW moment!"*, *"Amazing capability!"*, or celebratory commentary directed at the LLM itself.
* **Critique with empathy:** Before writing that something is a "wow moment", ask: *is this truly a wow moment for the human student, or is it an everyday occurrence / confusing technical step?*
* **Keep the tone sober, technical, and measured.**
* **Typography Rule:** Reserve **bold** strictly for technical entities (command flags, file paths, shell commands, environment variables, critical warning labels). Never bold emotive adjectives or artificial praise.

### 10. Strict TDD Mandate for Bug Fixes (Test-First Progression)
* **Every bug fix MUST be preceded by a failing automated test.** Never write a fix directly in the codebase without first demonstrating the failure in the test suite.
* **TDD Invariant:**
  1. Write an automated unit, integration, or architecture test in the project's native test framework proving the defect.
  2. Run the test suite and verify that the test **FAILS (RED)**.
  3. Implement the minimal fix in application code or configuration.
  4. Run the test suite and verify that the test **PASSES (GREEN)**.
  5. Commit both test and fix together.
* **Cumulative Test Robustness:** Every FL iteration MUST leave the repository with strictly more automated tests than before (`tests_count(FL_{N}) > tests_count(FL_{N-1})`). This guarantees that regressions are permanently locked out.

### 11. Spec & Constitution Awareness + 160-Char Tweet Checkpoint
* If the repository contains `docs/CONSTITUTION.md` or `docs/SPEC.md` (or `workshop/SKELETON.md`), the FL agent MUST verify step compliance against them.
* At the conclusion of every Codelab page in `FRICTION_LOG/XX.md`, the agent MUST write a **160-character Tweet Checkpoint** answering:
  `🐦 Constitution/Spec Tweet: [Yes/No + brief rationale <= 160 chars]`
* Example:
  `🐦 Tweet: ✅ Step 6 fully adheres to Constitution Art. 10 (compose.prod.yaml sidecars active) and Spec: web, worker, and proxy containers all running.`

## Core Workflow

When the user provides a Codelab URL, follow these exact steps. Ensure each step is fully completed before moving on to the next. Do not skip steps. This skill is designed to be resumable, so if the execution is interrupted, restart the skill and pick up where you left off.

### Step 1: Preparation & Dynamic Scaffold

1. Determine the base campaign directory (`b<BUG_ID>-<YYYYMMDD>-frictionlog-<CODELAB_SLUG>`) and iteration subdirectory (`<YYYYMMDD>-fl<NNN>`, e.g. `20260911-fl001`).
2. Ensure the Buganizer campaign issue is tagged with hotlist `#8950858`.
3. Run the included `scripts/setup_scaffold.sh` script passing the Codelab URL (or local `index.lab.md` path) as the second argument:

    ```bash
    ./scripts/setup_scaffold.sh <YYYYMMDD-frictionlog-CODELAB_TITLE> <CODELAB_URL_OR_MD_PATH> [BUG_ID]
    ```

    This script automatically creates the directory structure AND invokes `scripts/extract_codelab.py`, which extracts every step (`01.md` .. `NN.md`) and **dynamically populates the Step-by-Step Scorecard Table in `README.md` with the exact `N` steps, real step titles, and durations**!

### Step 2: Download and Mirror Codelab Content (Dynamic Scorecard Sync)

1. If `setup_scaffold.sh` was called without `<CODELAB_URL>`, run `extract_codelab.py` directly:

    ```bash
    python3 scripts/extract_codelab.py <URL_OR_MD_PATH> <YYYYMMDD-frictionlog-CODELAB_TITLE>/codelab/original
    ```

2. *Fallback for JS-rendered Codelabs*: If `extract_codelab.py` yields empty files (due to dynamic JS rendering), use `web_fetch` or `curl` to save each step into `codelab/original/01.md`, `02.md`, ..., `NN.md` (with `# Step Title` on line 1), and then run:

    ```bash
    python3 scripts/extract_codelab.py --sync-readme <YYYYMMDD-frictionlog-CODELAB_TITLE>
    ```

    This scans `codelab/original/*.md` and **dynamically replaces the placeholder Pagella Semaforica in `README.md` with the exact `N` steps and titles**!
3. Copy all the original markdown files into the `codelab/proposed/` directory. You will apply fixes and patches to the copies in this directory later.

### Step 3: GCP Project Setup

1. Ask the user: "Please provide a fresh/virgin GCP Project ID (with billing enabled) to avoid resource conflicts, OR a Billing Account ID."
    * **Virgin Project Preference**: Emphasize to the user that using a brand new, empty ("virgin") project from the 90-day pool (`011F17-0F9CE4-E03264`) is strongly recommended to prevent overlapping terraform states, GKE clusters, or IAM conflicts.
2. If the user provides an existing `PROJECT_ID`:
    * Verify that the project exists and has active billing associated (e.g., using `gcloud beta billing projects describe <PROJECT_ID>`).
    * **DO NOT PROCEED** to Step 4 until you have verified that billing is correctly linked. If billing is missing or disabled, stop and ask the user to fix it.
    * Save it to the `.env.fl` file and proceed to Step 4.
3. If the user provides a Billing Account ID without a project, use `gcloud` commands to autonomously:
    * Create a new GCP project (generate a sensible, unique project ID).
    * Link the newly created project to the provided Billing Account ID (`gcloud beta billing projects link <PROJECT_ID> --billing-account <ACCOUNT_ID>`).
    * Verify that the billing is correctly linked. **DO NOT PROCEED** until billing is active.
    * Save the newly created `PROJECT_ID` to the `.env.fl` file.
4. **Automation Mandate**: From this point forward, automate as much as you reasonably can without asking for permission between steps.

### Step 4: Autonomous Execution, Logging, and Repo Analysis (The 6-Question Step Audit)

Begin reproducing the codelab autonomously, going through each page (`01`, `02`, ..., `NN`) sequentially.

For each page `XX`:

1. Check if `FRICTION_LOG/XX.md` already exists and is complete. If it is, **skip** to the next page. This allows the workflow to be resumable.
2. **Execute the 6-Question Structural Audit**:
   - **Q1: Prerequisite Integrity**: What was expected to be finished in Page `XX-1`? Is our environment and cloud state 100% prepared, or did we carry over half-baked state?
   - **Q2: Teleological Purpose & Scope (Semantic Drift Check)**:
     - What is the exact learning outcome of this page? Explicitly separate **Mandatory Steps** from **Optional Sidebars**.
     - **Cognitive Drift Check (High Thinking)**: Compare the **Narrative Promise** of the page (title, intro, diagram) with the **Executed CLI Commands**. Does the command actually achieve what the prose promised, or is it a degraded shortcut that leaves the student with an architecture different from what was taught? If there is a mismatch between declared learning intent and actual implementation, flag a **P1 Semantic Drift Defect** immediately.
   - **Q3: Mandatory Gatekeeping**: Run all mandatory instructions verbatim. If ANY mandatory command fails or cannot be completed:
     - 🛑 **ABORT IMMEDIATELY**.
     - Mark the step 🔴 **RED** in `FRICTION_LOG/XX.md` with the exact blocker and root cause.
     - Ask the user for help if the step inherently requires human interaction, or halt execution. **Never silently skip a mandatory failure.**
   - **Q4: Optional Part Accounting**: Test optional exercises. If not performed or failed, document why without penalizing the primary core grade.
   - **Q5: Structural Placement Critique**:
     - Could this step have been anticipated 2 steps earlier?
     - Should it be postponed or merged into another step (e.g. did a standalone step have no reason to exist)?
     - Did it perform duplicate work already handled by Terraform or automated scripts?
   - **Q6: Audience Alignment & Density Check**:
     - Are difficult concepts explained simply and intuitively?
     - Did we dwell too long on trivia that only 1 student in 20 will ever encounter? (If so, flag for trimming under the "Less is More" covenant).
3. **External Repositories**: If the codelab references an external Git repository:
    * Clone the repository into the `external-repos/` directory.
    * Record the exact Commit SHA and Commit Timestamp (`git log -1 --format="%h (%ci)"`).
    * Analyze the repository code for any missing permissions (`chmod +x`), broken relative paths, or bugs.
    * Open a GitHub Issue (`GHI`) tagged with `friction-log` and `FL00X`, and attach a Pull Request (`PR`) fixing those issues.
4. **Log your experience** by writing to `FRICTION_LOG/XX.md`:
    * Use bullet points for every distinct action or instruction.
    * **Include a timestamp** at the beginning of each bullet point in the format `` * `HH:MM:SS` `` to track execution time and make the logs easily grep-able.
    * Use 🔴 (Red) if the experience was bad, broken, or a blocker (`Exit code != 0` or mandatory gate failure).
    * Use 🟡 (Yellow) if the experience was suboptimal, required a workaround, or had minor friction.
    * Use 🟢 (Green) if the experience was smooth and worked out-of-the-box.
5. At the end of the page, write a **Proof of Execution** block showing exact CLI output (`kubectl get pods`, `curl -I`, etc.).
6. Write the **160-Char Tweet Checkpoint**:
   ```markdown
   > 🐦 **Constitution/Spec Tweet:** [Max 160 chars: did this step adhere to docs/CONSTITUTION.md / SPEC.md?]
   ```

### Step 5: Final Output Synthesis & Mandatory Synoptic Tables

Once all pages have been completed, create `README.md` and `FRICTION_LOG.md` in the iteration folder. Both files MUST begin with **two mandatory synoptic tables**:

#### 1. Executive Synoptic Table (Top Metadata Table)
Must contain the following exact rows:

| Field | Value | Notes / Details |
| :--- | :--- | :--- |
| **ITERATION_ID** | `YYYYMMDD-flNNN` (`FL-NNN`) | e.g., `20260911-fl001` (`FL-001`) |
| **START_DATETIME** | `YYYY-MM-DD HH:MM:SS TZ` | End time: `YYYY-MM-DD HH:MM:SS TZ` |
| **PROJECT_ID** | `<GCP_PROJECT_ID>` | GCP Project used for reproduction |
| **BILLING_ACCOUNT** | `<BILLING_ACCOUNT_ID>` | Billing Account ID & name |
| **TESTER_IDENTITY** | `<EMAIL>` | Identity / gcloud configuration used |
| **CODELAB_URL** | `[Link](https://...)` | Staging / Production URL & Google3 CL |
| **REPO_COMMIT_HOOK** | `[repo@SHA](https://...)` | **Commit Timestamp:** `YYYY-MM-DD HH:MM:SS TZ` (`git log -1 --format="%h (%ci)"`) |
| **TRACKING_ISSUES** | `[b/ID](http://b/...)` \| `[GHI #N](https://...)` | Attached PR: `[PR #M](https://...)` \| Hotlist `#8950858` |
| **OVERALL_STATUS** | `🔴 RED` / `🟡 YELLOW` / `🟢 GREEN` | Summary score & blocker count |

#### 2. Step-by-Step Scorecard Table (Traffic Light Vote Per Step)
Must grade every single Codelab step (`🟢 GREEN`, `🟡 YELLOW`, `🔴 RED`) with duration and concise empirical notes:

| Step # | Codelab Step Title | Vote | Duration | Empirical Verification & Notes |
| :---: | :--- | :---: | :---: | :--- |
| **01** | **Step 1 (e.g. Setup / Auth)** | 🟢 **GREEN** | `~2m` | Identity & billing verified |
| **02** | **Step 2 (e.g. Environment Deploy)** | 🟡 **YELLOW** | `~11m` | e.g. 1 retry needed due to API race condition |
| **03** | **Step 3** | 🔴 **RED** | `~5m` | e.g. `Permission denied` on script (`BUG-03`) |
| **04** | **Step 4** | 🟢 **GREEN** | `~4m` | Verification passed |
| **05** | **Step 5** | 🟢 **GREEN** | `~5m` | Teardown completed |
| **...** | **...** *(Expand/contract to match exact N steps)* | ... | `...` | `...` |

#### 3. Deterministic Machine-Readable Telemetry (`friction_log.json` / `friction_log.yaml`)
In addition to the markdown reports, the agent **MUST** output a deterministic machine-readable manifest (`friction_log.json` or `friction_log.yaml`) adhering to `apiVersion: devrel.google.com/v2alpha1` (see `references/friction_log.yaml`).
This manifest MUST record:
- **`git` Hook**: Target commit SHA, commit timestamp, and dual versions (app version and codelab version).
- **`ai_runner`**: AI Harness used (`Antigravity`, `Gemini CLI`, `Claude Code`), harness version, model string (`gemini-2.5-pro`), and model pool.
- **`human_intervention`**: Total prompts exchanged, number of manual unblocks by the human, and a 1-line summary of human assistance.
- **`steps`**: Granular array of steps with duration in seconds, errors/warnings count, semantic drift flag, captured screenshots, and the 160-char tweet checkpoint.
- **`bugs_logged`**: Tracked bug IDs, severities, and GHI / Buganizer links.

**Mandatory Validation & Autofill Tool**:
The agent MUST run the included validator to ensure schema compliance before finalizing the log:
```bash
python3 scripts/validate_telemetry.py path/to/friction_log.json --autofill
```
If any mandatory field could not be deduced during execution, `--autofill` ensures it is safely stamped with explicit `UNKNOWN` values instead of omitting keys or crashing downstream parsers.

6. **Always clean up expensive cloud resources (`terraform destroy`)** once the friction log and postmortem artifacts are captured, unless explicitly asked to leave them running.
