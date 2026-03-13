---
name: devrel-frictionlog-codelab
version: 0.0.3
description: 🥑 [DevRel] Automates friction logging for a given Google Codelab URL. Use when a user provides a codelab URL and wants the agent to systematically reproduce the steps, log friction for each page, optionally create a GCP project, clone external repos to fix bugs, and produce a detailed report of the experience in a README.md and BUGS.md.
# version: in the bash script.
---

# DevRel Friction Log Codelab

This skill automates the process of going through a Google Codelab, reproducing its steps, systematically documenting the experience (a "friction log"), identifying bugs in external repositories, and producing actionable reports.

## Core Workflow

When the user provides a Codelab URL, follow these exact steps. Ensure each step is fully completed before moving on to the next. Do not skip steps. This skill is designed to be resumable, so if the execution is interrupted, restart the skill and pick up where you left off.

### Step 1: Preparation

1. Determine the base directory for the execution named `YYYYMMDD-frictionlog-<CODELAB_TITLE>`. (e.g., `20260313-frictionlog-app-mod-workshop`).
2. Run the included `scripts/setup_scaffold.sh` script to deterministically create the scaffolding:

    ```bash
    ./scripts/setup_scaffold.sh <YYYYMMDD-frictionlog-CODELAB_TITLE>
    ```

    This script automatically creates the `codelab/original/`, `codelab/proposed/`, `FRICTION_LOG/`, and `external-repos/` directories. It also initializes the `.env` file, the `BUGS.md` file, the `external-repos/.gitignore`, and writes a `.version` file for tracking the skill version and repository.

### Step 2: Download and Mirror Codelab Content

1. Attempt to extract the codelab content using the included Python script:

    ```bash
    python3 scripts/extract_codelab.py <URL> <YYYYMMDD-frictionlog-CODELAB_TITLE>/codelab/original
    ```

2. *Fallback*: If the `extract_codelab.py` script fails or yields empty files (due to dynamic rendering), use your internal `web_fetch` tool or `curl` to read the Codelab pages and save the textual content into `01.md`, `02.md`, etc., within `codelab/original/`.
3. Copy all the original markdown files into the `codelab/proposed/` directory. You will apply fixes and patches to the copies in this directory later.

### Step 3: GCP Project Setup

1. Ask the user: "Please provide an existing GCP Project ID (with billing enabled) OR a Billing Account ID."
2. If the user provides an existing `PROJECT_ID`:
    * Verify that the project exists and has active billing associated (e.g., using `gcloud beta billing projects describe <PROJECT_ID>`).
    * **DO NOT PROCEED** to Step 4 until you have verified that billing is correctly linked. If billing is missing or disabled, stop and ask the user to fix it.
    * Save it to the `.env` file and proceed to Step 4.
3. If the user provides a Billing Account ID without a project, use `gcloud` commands to autonomously:
    * Create a new GCP project (generate a sensible, unique project ID).
    * Link the newly created project to the provided Billing Account ID (`gcloud beta billing projects link <PROJECT_ID> --billing-account <ACCOUNT_ID>`).
    * Verify that the billing is correctly linked. **DO NOT PROCEED** until billing is active.
    * Save the newly created `PROJECT_ID` to the `.env` file.
4. **YOLO Mode Suggestion**: Once billing is successfully verified and enabled, explicitly suggest to the user: "Project and billing are successfully configured. To proceed smoothly through the rest of the Codelab, I recommend enabling **YOLO mode (CTRL + Y)**."
5. **Automation Mandate**: From this point forward, try to automate as much as you reasonably can. Only stop and ask for human intervention when you encounter a strict blocker that requires a human (e.g., creating a new GitHub user, generating an OAuth consent screen via the UI, forking a repository manually, or browsing an authenticated web resource that the CLI cannot access).

### Step 4: Autonomous Execution, Logging, and Repo Analysis

Begin reproducing the codelab autonomously, going through each page (`01`, `02`, ..., `NN`) sequentially.

For each page `XX`:

1. Check if `FRICTION_LOG/XX.md` already exists and is complete. If it is, **skip** to the next page. This allows the workflow to be resumable.
2. Follow the instructions on the codelab page as closely as possible, running commands and performing tasks.
3. **External Repositories**: If the codelab references an external Git repository:
    * Clone the repository into the `external-repos/` directory.
    * Analyze the repository code for any missing or broken parts mentioned in the codelab instructions.
    * If bugs or broken parts are identified, ask the user for permission to start filing Pull Requests to fix those issues.
4. **Log your experience** by writing to `FRICTION_LOG/XX.md`:
    * Use bullet points for every distinct action or instruction.
    * **Include a timestamp** at the beginning of each bullet point in the format `` * `HH:MM:SS` `` to track execution time and make the logs easily grep-able.
    * Use `*` for normal, expected steps.
    * Use 🔴 (Red) if the experience was bad, broken, or highly confusing.
    * Use 🟡 (Yellow) if the experience was "meh", suboptimal, or slightly confusing.
    * Use 🟢 (Green) if the experience was particularly good or delightful.
    * Document any inconsistencies between the text instructions, provided screenshots (if you are capable of reviewing them or they are described textually), and the actual behavior you experience.
    * **Time Analysis:** At the end of each page's log, note the total time it took you (the AI) to complete the page. Compare this with the codelab's estimated time for that page (if provided), and suggest a realistic completion time for a human user based on the complexity of the tasks.
5. If you encounter errors, typos, or wrong instructions in the codelab text, or broken code in external repos:
    * Patch the markdown file in `codelab/proposed/XX.md` with the proposed solution or fix.
    * Explain *why* the change was needed in the `FRICTION_LOG/XX.md` file.
    * Add a detailed bullet point to `BUGS.md` explaining the issue and linking to the proposed fix or PR.
6. Continuously update the `.env` file with any new resource coordinates created during the step (e.g., URLs, instances, DB strings).

### Step 5: Final Output Synthesis

Once all pages have been completed, create a short `README.md` file in the base directory containing a high-level summary of the entire run, and a consolidated `FRICTION_LOG.md` file.

The `README.md` must be concise and include:

1. **What you did**: A brief sentence explaining the codelab run.
2. **What you found**: High-level observations and Completion Status (were you able to run the whole codelab?).
3. **Big Mistakes**: A summarized list of major inconsistencies or show-stopping bugs.
4. **Links**: Explicit links to the `BUGS.md` file and the consolidated `FRICTION_LOG.md` file.

The `FRICTION_LOG.md` must include:

1. **Changes Needed (Top Section)**: A precise list of the changes that need to be made. Provide visual markdown diffs or patches showing the OLD incorrect text/code and the NEW corrected text/code.
2. **Consolidated Friction Logs**: A concatenation of all the individual per-page friction logs from the `FRICTION_LOG/` directory. Use an H2 (`##`) for each page so they are easy to isolate.

## Resumption Logic

Always check the base directory and `FRICTION_LOG/` contents before starting work. If a folder for the codelab already exists, identify the last completed step by finding the highest numbered `FRICTION_LOG/XX.md` file, and resume execution from the next step (`XX+1`). Do not repeat completed work unless explicitly requested.
