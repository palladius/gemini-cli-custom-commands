# Changelog - devrel-frictionlog-codelab Skill

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
