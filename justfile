
list:
    just -l


#install:
#      "name": "palladius-common-commands",



find-installed-commands:
    find  ~/.gemini/extensions/palladius-common-commands/commands/ -name \*.toml


# [TASK] Checks for Updates of this beautiful gem
check-for-updates:
    gemini -y -c "/pcc:check-for-updates Check for status and dump all info in 'tmp-from-justfile.md'. Make sure to show local and remote version using emojis. If 'glow' is available, glow the file."

# [TASK] Checks for Google license if missing
check-google-license:
    gemini -y -p '/common:check_google_license  Verify all is in place, and if needed apply the "addlicense" script to the whole git repo.'

# [TASK] Refresh User Manual
refresh-user-manual:
    gemini -y -p '/pcc:refresh_user_manual  Regenerate the User Manual in README.md based on the commands available. Use "glow" on User Manual if available on this machine.'

# develops this gem
gemini:
    gemini -y -p 'Code some functionality making sure that CHANGELOG.md and README.md are updated accordingly. Run tests and make sure all is well.'
