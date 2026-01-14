###################################################
# Note: Add this to your Makefile uf you have `make` installed but not `just` installed.
#	   If you have `just` prefer `justfile` which is more modern and powerful.
###################################################

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