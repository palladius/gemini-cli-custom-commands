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
| **1** | **Prerequisites & Auth Setup** | ⏳ | `0m` | Pending execution |
| **2** | **Environment / Infrastructure Provisioning** | ⏳ | `0m` | Pending execution |
| **3** | **Core Codelab Scenario Execution** | ⏳ | `0m` | Pending execution |
| **4** | **Teardown (`terraform destroy`)** | ⏳ | `0m` | Always clean up cloud resources when done |
