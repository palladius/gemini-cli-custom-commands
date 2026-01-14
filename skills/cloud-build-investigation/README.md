# Cloud Build Investigation Skill

Expert-level SRE skill for investigating and debugging Google Cloud Build (GCB) and Cloud Run deployment issues.

## Overview

This skill provides systematic workflows for:
- Correlating git commits with Cloud Build failures
- Analyzing build logs
- Debugging deployment issues
- Managing environment variables
- Following SRE best practices for incident investigation

## Structure

```
cloud-build-investigation/
├── SKILL.md                      # Main skill definition (read by Gemini)
├── README.md                     # This file
├── scripts/
│   ├── correlate_builds.rb       # Correlates git commits with Cloud Builds
│   └── correlate_builds_test.rb  # Test suite for correlation script
├── references/
│   └── gcp-resources.md          # GCP documentation and troubleshooting guide
└── assets/
    └── (empty - for future diagrams/screenshots)
```

## Usage

### For Gemini CLI

The skill is automatically activated when you mention Cloud Build issues:

```bash
gemini "Why is my Cloud Build failing?"
gemini "Help me debug this Cloud Run deployment"
gemini "Investigate the latest Cloud Build failure"
```

### Manual Script Usage

You can also run the correlation script directly:

```bash
# Correlate commits with builds
ruby .gemini/skills/cloud-build-investigation/scripts/correlate_builds.rb YOUR_PROJECT_ID

# Or set environment variable
export GCP_PROJECT=your-project-id
ruby .gemini/skills/cloud-build-investigation/scripts/correlate_builds.rb

# Run tests
ruby .gemini/skills/cloud-build-investigation/scripts/correlate_builds_test.rb
```

## Prerequisites

- **gcloud CLI**: Installed and authenticated
- **Git repository**: Must be in a git repo
- **Ruby**: For running correlation scripts
- **Justfile targets**: Recommended (see SKILL.md for templates)

## Key Principles

⚠️ **CRITICAL**: This skill follows the principle of "assume positive intention"
- Never make major changes to existing `cloudbuild.yaml`
- Take baby steps when debugging
- Minimize mutations to working configurations
- Cross-correlate timestamps between git and Cloud Build
- Document findings in GitHub issues

## Workflow Summary

1. **Gather**: Collect git logs and Cloud Build history
2. **Analyze**: Find the first failing build
3. **Correlate**: Match build failures to git commits
4. **Investigate**: Examine logs and diffs
5. **Fix**: Propose and test fixes incrementally
6. **Document**: File GitHub issues with findings

## Resources

- See `references/gcp-resources.md` for GCP documentation links
- See `SKILL.md` for detailed workflow instructions
- See scripts for automation tools

## Testing

Run the test suite to verify the correlation script:

```bash
ruby .gemini/skills/cloud-build-investigation/scripts/correlate_builds_test.rb
```

Expected output:
```
🧪 Testing correlate_builds.rb
==================================================
Test: Script file exists... ✅ PASS
Test: Script is executable... ✅ PASS
Test: Handles missing PROJECT_ID... ✅ PASS
Test: Shows usage message... ✅ PASS

==================================================
Results: 4 passed, 0 failed
```

## Contributing

When updating this skill:
1. Update `SKILL.md` with new workflows or instructions
2. Add helper scripts to `scripts/` with corresponding `_test.rb` files
3. Update `references/` with new documentation
4. Test thoroughly before committing
5. Update this README if structure changes

## Version History

- **v1.0** (2026-01-14): Initial skill creation from custom command refactoring
  - SKILL.md with comprehensive workflow
  - correlate_builds.rb script for automated correlation
  - GCP resources reference documentation
  - Test suite
