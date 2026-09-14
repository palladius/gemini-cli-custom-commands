# 🦖 Friction Log Report: {{NAME}}

## 📋 Executive Synoptic Table

| Field | Value | Notes / Details |
| :--- | :--- | :--- |
| **ITERATION_ID** | `{{NAME}}` | e.g. `YYYYMMDD-fl001` (`FL-001`) |
| **START_DATETIME** | `{{STARTED_AT}}` | End Datetime: `<TBD>` |
| **PROJECT_ID** | `{{PROJECT_ID}}` | GCP Project used for reproduction (prefer 90-day pool `011F17-0F9CE4-E03264`) |
| **BILLING_ACCOUNT** | `<BILLING_ACCOUNT_ID>` | Active Billing Account ID |
| **TESTER_IDENTITY** | `{{IDENTITY}}` | Identity / `gcloud` configuration used |
| **CODELAB_URL** | [Codelab Link]({{CODELAB_URL}}) | Google3 CitC / Staging URL |
| **REPO_COMMIT_HOOK** | `<repo@SHA>` (`YYYY-MM-DD HH:MM:SS TZ`) | **Mandatory:** Record exact `git log -1 --format="%h (%ci)"`! Never run 2 FLs on same SHA! |
| **TRACKING_ISSUES** | [b/{{BUG_ID}}](http://b/{{BUG_ID}}) (Hotlist `#8950858`) \| `GHI #<N>` | Attached PR: `PR #<M>` |
| **OVERALL_STATUS** | **⏳ IN PROGRESS** | Final Vote: `🟢 GREEN` / `🟡 YELLOW` / `🔴 RED` |

---

## 🚦 Step-by-Step Scorecard Table

| Step # | Codelab Step Title | Vote (`🟢`/`🟡`/`🔴`) | Duration | Empirical Verification & Notes |
| :---: | :--- | :---: | :---: | :--- |
| **01** | **Step 1 (e.g. Setup / Auth)** | ⏳ | `0m` | [Original](codelab/original/01.md) \| [Log](FRICTION_LOG/01.md) |
| **02** | **Step 2 (e.g. Environment Deploy)** | ⏳ | `0m` | [Original](codelab/original/02.md) \| [Log](FRICTION_LOG/02.md) |
| **03** | **Step 3** | ⏳ | `0m` | [Original](codelab/original/03.md) \| [Log](FRICTION_LOG/03.md) |
| **04** | **Step 4** | ⏳ | `0m` | [Original](codelab/original/04.md) \| [Log](FRICTION_LOG/04.md) |
| **05** | **Step 5** | ⏳ | `0m` | [Original](codelab/original/05.md) \| [Log](FRICTION_LOG/05.md) |
| **...** | *(AI Note: Add or remove rows `06..NN` to match the exact steps of this Codelab)* | ⏳ | `...` | `...` |
