
list:
    just -l


#install:
#      "name": "palladius-common-commands",



find-installed-commands:
    find  ~/.gemini/extensions/palladius-common-commands/commands/ -name \*.toml


# works from v0.0.3 hopefully
check-for-updates:
    gemini -y -c "/pcc:check-for-updates Check for status and dump all info in tmp-from-justfile.md . Make sure to show local and remote version"

check-google-license:
    gemini -y -p '/common:check_google_license  Verify all is in place, and if needed apply the addlicense script to the whole git repo.'
