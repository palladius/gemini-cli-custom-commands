---
name: cloud-build-investigation
description: |
  Expert-level SRE skill for Google Cloud Build (GCB) and Cloud Run investigations.
  Activate when user mentions Cloud Build failures, deployment issues to Cloud Run,
  or needs help debugging GCB pipelines. Specializes in correlating git commits with
  build failures, analyzing build logs, and providing systematic debugging workflows.
---

# Cloud Build Investigation Skill

This skill provides expert-level SRE capabilities for investigating and debugging Google Cloud Build (GCB) issues, particularly for deployments to Cloud Run.

## When to Activate

Use this skill when:
- User mentions Cloud Build failures or errors
- Debugging deployment issues to Cloud Run
- Investigating why a build/deployment stopped working
- Correlating git commits with build failures
- Setting up or troubleshooting Cloud Build pipelines
- Adding environment variables to Cloud Build/Cloud Run

## Core Principles

⚠️ **CRITICAL**: Assume positive intention!
- If a `cloudbuild.yaml` exists with a trigger, **DO NOT MOVE OR MAJORLY CHANGE IT**
- The user (likely Riccardo) may have spent hours making it work
- Take **baby steps** and **minimize mutations**
- Changing folder targets or major refactoring will likely break things further

## Investigation Workflow

### Step 1: Gather Build History

1. Run `just git-logs-timestamped` to get compact commit history with timestamps (YYYYMMDD HH:MM)
2. Run `just cloud-build-list` to get recent Cloud Builds
3. Identify N successful builds and M failed builds
4. Focus on the **FIRST failing build** (this is key!)

### Step 2: Analyze the Failure

1. Use `just cloud-build-show-log FIRST_FAILING_BUILD_ID` to examine logs
2. Cross-correlate with git commits via timestamps
3. Cross-reference with the VERSION file (Carlessian standard)
4. Identify the exact commit that introduced the failure

### Step 3: Root Cause Analysis

Cross-correlate failed build logs with the git diff of the culprit commit:
- Was it a Dockerfile change?
- A dependency update (Gemfile/requirements.txt/package.json)?
- A configuration change?
- An environment variable issue?

### Step 4: Corrective Action

If investigation shows **NO errors** → Done! ✅

If errors found:

1. **File GitHub Issue**:
   - Title: `[failed Cloud Build] <BUILD_ID> <SHORT_DESCRIPTION>`
   - BUILD_ID in title enables deduplication
   - Post the git log list (enables GH to link commits visually)
   
2. **Investigate & Propose Fix**:
   - Document findings in the issue
   - Propose a fix with user collaboration
   
3. **Test with Baby Steps**:
   - Cloud Build tests require small commit/pushes
   - Version bumps: `1.2.3` → `1.2.3a` → `1.2.3b` (for quick testing)
   - Each build takes 5-6 minutes
   - Consider combining with minor UI/UX improvements for time efficiency

4. **Monitor**:
   - Keep checking build status every 2 minutes
   - Use `just cloud-build-list` and `just cloud-build-show-log {{build_id}}`

## Required Justfile Targets

Ensure the project's `justfile` has these targets (adapt PROJECT_ID and CLOUD_RUN_ENDPOINT):

```makefile
# List latest 10 CB builds, possibly the first might still be running
cloud-build-list:
    gcloud builds list --project=PROJECT_ID --limit=10

# Show the log of a specific Cloud Build, eg 7c82188e-485a-4735-a70d-fb303fbfe5a0
cloud-build-show-log build_id:
    @echo "Showing log for build ID: {{build_id}}. Use --stream to follow the log indefinitely (you can do it, but I want Gemini NOT to do it)."
    gcloud builds log {{build_id}} --project=PROJECT_ID

# Show Cloud Run logs
cloud-run-logs:
    @echo "☁️  Fetching logs for Cloud Run environment..."
    gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=CLOUD_RUN_ENDPOINT" --project=PROJECT_ID --limit=100 --format="value(timestamp, severity, textPayload)"

# Shows git logs in timestamped way
git-logs-timestamped:
    git log --pretty=format:'%h %ad | %s%d [%an]' --date=iso -n 10
```

**Note**: If `just` is not available, use a `Makefile` instead (convert N spaces to tabs).

## Adding Environment Variables

This is a complex process. Follow carefully:

1. Add variable to the script (usually in `bin/` with "cloud build" in name)
   - Example: `bin/ricc-cb-push-to-cloudrun-magic.sh`
2. Ensure the variable is passed from Cloud Build in the step that calls it
3. Update the Cloud Run trigger for this service
   - Should be documented in `README.md` (if not, document it!)
4. Check `gcp/` or `iac/` folders for additional hints

## File Structure

If Cloud Build is set up, expect:
- `cloudbuild.yaml` (root file, likely has trigger attached)
- Possibly `bin/` scripts for deployment
- Possibly `gcp/` or `iac/` folders with infrastructure code

## Resources

- **Scripts**: Check `.gemini/skills/cloud-build-investigation/scripts/` for helper utilities
- **References**: See `.gemini/skills/cloud-build-investigation/references/` for GCP docs

## Important Reminders

🚫 **DO NOT**:
- Change `cloudbuild.yaml` location or major structure
- Modify `build` target in `justfile` without understanding full context
- Make sweeping changes to folder structures
- Auto-stream logs indefinitely (use `--stream` cautiously)

✅ **DO**:
- Take baby steps
- Test incrementally
- Document findings in GitHub issues
- Collaborate with the user (Riccardo)
- Cross-correlate timestamps between git and Cloud Build
- Use VERSION file for additional context
