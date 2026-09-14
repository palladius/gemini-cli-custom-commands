---
name: devrel-frictionlog-codelab
version: 0.2.1
description: 🥑 [DevRel] Automates friction logging for a given Google Codelab URL. Use when a user provides a codelab URL and wants the agent to systematically reproduce the steps, log friction for each page, optionally create a GCP project, clone external repos to fix bugs, and produce a detailed report of the experience in a README.md and BUGS.md with Synoptic Executive Tables, Step-by-Step Scorecards, and Commit Hook progression.
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

### Step 4: Autonomous Execution, Logging, and Repo Analysis

Begin reproducing the codelab autonomously, going through each page (`01`, `02`, ..., `NN`) sequentially.

For each page `XX`:

1. Check if `FRICTION_LOG/XX.md` already exists and is complete. If it is, **skip** to the next page. This allows the workflow to be resumable.
2. Follow the instructions on the codelab page as closely as possible, running commands and performing tasks verbatim.
3. **External Repositories**: If the codelab references an external Git repository:
    * Clone the repository into the `external-repos/` directory.
    * Record the exact Commit SHA and Commit Timestamp (`git log -1 --format="%h (%ci)"`).
    * Analyze the repository code for any missing permissions (`chmod +x`), broken relative paths, or bugs.
    * Open a GitHub Issue (`GHI`) tagged with `friction-log` and `FL00X`, and attach a Pull Request (`PR`) fixing those issues.
4. **Log your experience** by writing to `FRICTION_LOG/XX.md`:
    * Use bullet points for every distinct action or instruction.
    * **Include a timestamp** at the beginning of each bullet point in the format `` * `HH:MM:SS` `` to track execution time and make the logs easily grep-able.
    * Use 🔴 (Red) if the experience was bad, broken, or a blocker (`Exit code != 0`).
    * Use 🟡 (Yellow) if the experience was suboptimal, required a workaround, or had minor friction.
    * Use 🟢 (Green) if the experience was smooth and worked out-of-the-box.
5. At the end of the page, write a **Proof of Execution** block showing exact CLI output (`kubectl get pods`, `curl -I`, etc.).

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

6. **Always clean up expensive cloud resources (`terraform destroy`)** once the friction log and postmortem artifacts are captured, unless explicitly asked to leave them running.
