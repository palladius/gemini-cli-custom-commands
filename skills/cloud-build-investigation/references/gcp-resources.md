# GCP Cloud Build & Cloud Run Resources

This document contains useful references for Cloud Build and Cloud Run investigations.

## Official Documentation

### Cloud Build
- [Cloud Build Overview](https://cloud.google.com/build/docs/overview)
- [Cloud Build Configuration](https://cloud.google.com/build/docs/build-config-file-schema)
- [Build Triggers](https://cloud.google.com/build/docs/automating-builds/create-manage-triggers)
- [Viewing Build Logs](https://cloud.google.com/build/docs/view-build-results)

### Cloud Run
- [Cloud Run Overview](https://cloud.google.com/run/docs)
- [Deploying to Cloud Run](https://cloud.google.com/run/docs/deploying)
- [Environment Variables](https://cloud.google.com/run/docs/configuring/environment-variables)
- [Cloud Run Logs](https://cloud.google.com/run/docs/logging)

## Common gcloud Commands

### Cloud Build

```bash
# List recent builds
gcloud builds list --project=PROJECT_ID --limit=10

# Get specific build details
gcloud builds describe BUILD_ID --project=PROJECT_ID

# View build logs
gcloud builds log BUILD_ID --project=PROJECT_ID

# Stream build logs (use cautiously)
gcloud builds log BUILD_ID --project=PROJECT_ID --stream

# Submit a manual build
gcloud builds submit --config=cloudbuild.yaml --project=PROJECT_ID
```

### Cloud Run

```bash
# List services
gcloud run services list --project=PROJECT_ID --region=REGION

# Describe a service
gcloud run services describe SERVICE_NAME --project=PROJECT_ID --region=REGION

# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=SERVICE_NAME" \
  --project=PROJECT_ID --limit=100

# Update environment variable
gcloud run services update SERVICE_NAME \
  --update-env-vars KEY=VALUE \
  --project=PROJECT_ID \
  --region=REGION
```

## Common Build Failure Patterns

### 1. Dependency Issues
**Symptoms**: Build fails during dependency installation
**Common Causes**:
- Updated dependency versions in lock files
- Network issues fetching dependencies
- Missing or incorrect package registry credentials

**Investigation**:
```bash
git diff LAST_GOOD_COMMIT FIRST_BAD_COMMIT -- Gemfile.lock package-lock.json requirements.txt
```

### 2. Docker Build Failures
**Symptoms**: Error during Docker image build
**Common Causes**:
- Dockerfile syntax errors
- Missing base image
- COPY/ADD path issues
- Build context problems

**Investigation**:
```bash
git diff LAST_GOOD_COMMIT FIRST_BAD_COMMIT -- Dockerfile .dockerignore
```

### 3. Test Failures
**Symptoms**: Build succeeds but tests fail
**Common Causes**:
- Code changes breaking tests
- Environment-specific test issues
- Missing test dependencies

**Investigation**:
Check test output in build logs, compare with local test runs

### 4. Deployment Failures
**Symptoms**: Build succeeds but deployment to Cloud Run fails
**Common Causes**:
- Missing environment variables
- Incorrect service configuration
- Permission issues
- Resource quota exceeded

**Investigation**:
```bash
gcloud run services describe SERVICE_NAME --project=PROJECT_ID --region=REGION
```

## Troubleshooting Checklist

- [ ] Check build logs for error messages
- [ ] Compare with last successful build
- [ ] Review git diff of suspect commits
- [ ] Verify environment variables are set correctly
- [ ] Check service account permissions
- [ ] Verify resource quotas
- [ ] Test Docker build locally
- [ ] Check for infrastructure changes (VPC, networking, etc.)
- [ ] Review Cloud Build trigger configuration
- [ ] Check for GCP service outages

## Useful Environment Variables

Common environment variables used in Cloud Build/Run:

- `PROJECT_ID`: GCP project identifier
- `REGION`: GCP region (e.g., `us-central1`)
- `SERVICE_NAME`: Cloud Run service name
- `IMAGE_NAME`: Docker image name
- `TAG`: Image tag (often `latest` or version number)
- `_CUSTOM_VAR`: Build substitution variables (prefixed with `_`)

## Best Practices

1. **Version Everything**: Use VERSION file and git tags
2. **Small Commits**: Make incremental changes for easier debugging
3. **Test Locally**: Build Docker images locally before pushing
4. **Document Triggers**: Keep trigger configuration in README
5. **Monitor Builds**: Set up notifications for build failures
6. **Use Substitutions**: Parameterize cloudbuild.yaml with substitution variables
7. **Cache Dependencies**: Use Cloud Build cache for faster builds
8. **Structured Logs**: Use JSON logging for easier parsing
