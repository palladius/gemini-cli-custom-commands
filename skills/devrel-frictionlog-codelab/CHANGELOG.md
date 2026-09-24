# Changelog - devrel-frictionlog-codelab Skill

## [0.3.5] - 2026-09-24

- 🛡️ **Multi-Instance Isolation & Collision Guard (Golden Rule 15)**:
  - **Chat/Session Locking (`CHAT_ID` / `INCARNATION_ID`)**: Each session records its unique identifier in `.env.fl`. If `.env.fl` already belongs to another active chat/incarnation, execution halts to avoid clobbering.
  - **Reentrant `gcloud` Configuration**: Mandated `CLOUDSDK_ACTIVE_CONFIG_NAME="fl<NNN>-<SLUG>"` so parallel agent terminals never mutate each other's active project or account.
  - **Atomic Step 0**: Immediate `.env.fl` generation with verbatim user prompt commented at the top (`# User Prompt: ...`), preserving 100% bash parseability.
  - **Template Polish**: Updated `references/env.template` with `FRICTIONLOG_SKILL_VERSION`, empty `AI_MODEL` with UI lookup guidance, and `INCARNATION_ID` (Antigravity UUID).
  - **"When in doubt, ask USER!"**: Explicit interactive pause when folder ownership or credentials are ambiguous.

## [0.3.4] - 2026-09-24

- 🛑 **Mandatory Pre-Teardown UAT Gate & Artifact Proof of Work (Golden Rule 14)**:
  - Strict prohibition against `terraform destroy` or unlinking billing without explicit user UAT validation.
  - Mandated generation of a Proof of Work Artifact (live URLs, database coords, screenshots) prior to asking for teardown authorization.
  - Added automatic model autodetection in `validate_telemetry.py` by inspecting Antigravity session transcripts.

## [0.3.3] - 2026-09-24

- 🤖 **Explicit AI Runner & Harness Telemetry in Synoptic Tables**:
  - Added **`AI_RUNNER`** (`Antigravity 2.0` / `Gemini CLI 0.37+`) and **`AI_MODEL`** (`gemini-2.5-pro`) rows explicitly to the mandatory Executive Synoptic Table in `SKILL.md` and Markdown reports.
  - Added **`SKILL_VERSION`** row to Markdown table template matching machine-readable telemetry (`friction_log.yaml`).
  - Added GCP Resources Artifact standard (`gcp_resources_flXXX.md`) detailing live endpoints, database instances, buckets, and teardown confirmation.

## [0.3.2] - 2026-09-24

- 🤝 **Mandatory Kickoff Triad Agreement & Virgin Baselines**:
  - **Interactive Kickoff Agreement**: The agent MUST interactively present available GCP identities (`gcloud auth list`), confirm the Billing Account ID, and agree on whether to create a fresh virgin project before executing any codelab steps.
  - **Virgin Baseline Mandate**: Every FL reproduction MUST start from a clean local directory/worktree and a brand-new, empty virgin GCP project with zero pre-enabled APIs or leftover resources.
  - **Skill Version Tracking in Telemetry**: Mandated `environment.skill.name` and `environment.skill.version` in `friction_log.yaml` / `.json` manifests (enforced by `scripts/validate_telemetry.py`).

## [0.3.1] - 2026-09-24

- 📊 **Deterministic Machine-Readable Telemetry & Validator Suite**:
  - Mandated generation of `friction_log.json` / `friction_log.yaml` (`apiVersion: devrel.google.com/v2alpha1`).
  - Added `scripts/validate_telemetry.py` to enforce presence of mandatory fields (`metadata`, `git`, `ai_runner`, `human_intervention`, `steps`, `bugs_logged`).
  - Implemented `--autofill` flag to safely backfill any unobserved mandatory fields with sensible defaults (e.g. `UNKNOWN`) preventing parser breakage.
  - Added automated test suite `scripts/validate_telemetry_test.py` covering strict validation, YAML/JSON parsing, and autofill recovery.

## [0.3.0] - 2026-09-23

- 🦖 **Friction Logging v2.0 (Lessons Learned from FL100)**:
  - **No Tautology Trap (Outcome & Architecture Assertion)**: Enforced rule that exit code 0 is insufficient. Agents must verify underlying cloud architecture and container sidecars rather than shallow command syntax.
  - **The "Less is More" Sacred Covenant**: High friction for editing student codelabs. Edits require heavy justification; edge-case workarounds belong in agent skills, automated tests, or tooling wrappers, never polluting the codelab.
  - **Proactive Visual Mandate**: Strictly abolished the bystander effect on `TODO(riccardo): add screenshot`. Agents must capture, crop, and embed screenshots autonomously.
  - **IaC Single Source of Truth**: Explicitly prohibited manual CLI commands that collide with or duplicate Terraform-provisioned resources.
  - **User Empathy & Windows Users**: Aggressively minimize cognitive friction for novice and Windows attendees; require `justfile` dotenv auto-loading and actionable, self-healing bash fixes when variables are missing.

## [0.2.1] - 2026-09-14

- 🧠 **Dynamic N-Step Pagella Semaforica (`extract_codelab.py` + `setup_scaffold.sh`)**: Resolved static placeholder limitation! `extract_codelab.py` now parses HTML (`<google-codelab-step label="..." duration="...">`), local DevSite Markdown (`index.lab.md`), or `--sync-readme <base_dir>` (`codelab/original/*.md`) and **dynamically rewrites `README.md` with the exact `N` steps, real step titles, and estimated durations**.

## [0.2.0] - 2026-09-14

- 🚫 **Commit Hook Progression Mandate**: Enforced strict rule never to run multiple Friction Logs on the same Git Commit SHA (`REPO_COMMIT_HOOK` with SHA + Timestamp).
- 🏷️ **Buganizer Hotlist Mandate (`#8950858`)**: Enforced automatic tagging with `HOTLIST+=8950858` on all Buganizer campaign issues (`env -i` clean invocation for `bugged`).
- 🗺️ **Multi-Iteration FL Plan & 90-Day GCP Project Pool**: Added Master 3-Iteration FL Plan table (`FL001` -> `FL002` -> `FL003`) allocating dedicated projects (`011F17-0F9CE4-E03264`) and 2-3 lines of explicit delta/justification between commits.
- 📊 **Mandatory Synoptic Tables**: Added `references/README.template.md` and updated `scripts/setup_scaffold.sh` to automatically scaffold the **Executive Synoptic Metadata Table** and **Step-by-Step Traffic-Light Scorecard Table**.

## [0.1.1] - 2026-04-22

- ✨ Initial documented changelog.
- 🥑 Automated friction logging and scaffold generation.
- 🤖 Auto-populated by `gc-skillume-bot-v0_2`.
