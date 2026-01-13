
# Install just from https://github.com/casey/just

# Lists targets
list:
    just -l


find-installed-commands:
    find  ~/.gemini/extensions/palladius-common-commands/commands/ -name \*.toml


# [TASK] Checks for Updates of this beautiful gem
check-for-updates:
    #gemini -y -c "/pcc:check-for-updates Check for status and dump all info in 'tmp-from-justfile.md'. Make sure to show local and remote version using emojis. If 'glow' is available, glow the file."
    ./.gemini/skills/check-for-updates/scripts/check_updates.rb

# [TASK] Checks for Google license if missing
check-google-license:
    gemini -y -p '/common:check_google_license  Verify all is in place, and if needed apply the "addlicense" script to the whole git repo.'

# [TASK] Refresh User Manual
refresh-user-manual:
    gemini -y -p '/pcc:refresh_user_manual  Regenerate the User Manual in README.md based on the commands available. Use "glow" on User Manual if available on this machine.'

# [TASK] Dedupe ricc's custom commands from old place to current place.
check-ricc-other-custom-commands:
    gemini -y -p 'check Custom Commands in here: https://github.com/palladius/gemini-cli-demos/tree/main/.gemini/commands and give me a diff of those vs the ones under ./commands/. What am I missing?'

# develops this gem
gemini:
    gemini -e '' --allowed-mcp-server-names '' -y
    # -p 'Code some functionality making sure that CHANGELOG.md and README.md are updated accordingly. Run tests and make sure all is well.'

