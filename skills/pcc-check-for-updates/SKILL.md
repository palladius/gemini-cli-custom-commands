---
name: pcc-check-for-updates
description: 
    Checks for updates to remote GH site for palladius/gemini-cli-custom-commands. 
    Use Ruby code to check for newer/older version.
---
# Check for Updates Skill

This skill allows the agent to check if the `palladius-common-commands` extension is up to date by comparing the local version with the remote version on GitHub.

## Description

Checks if the installed version of `palladius-common-commands` is the latest version available.

## Usage
Activate this skill when the user asks to check for updates or verify the extension version.

## Instructions
1.  Run the provided ruby script to perform the check.
    ```bash
    ruby .gemini/skills/check-for-updates/scripts/check_updates.rb
    ```
2.  Report the result to the user.
    - If an update is available, provide the command to update.
    - If up to date, confirm it.
    - If the local version cannot be determined (e.g., error in `gemini extensions list`), inform the user and suggest checking their installation.

## Resources
- Script: `scripts/check_updates.rb`
