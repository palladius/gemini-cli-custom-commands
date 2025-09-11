# Palladius Gemini CLI custom commands (or PCC)

Self: https://github.com/palladius/gemini-cli-custom-commands
Inspired by https://github.com/google-gemini/gemini-cli-security/tree/main

This is a collection of all Carlessian commands, packaged into one place.

## install

**Note** *(requires Gemini CLI v0.4.0 or newer):

```bash
# Install
gemini extensions install https://github.com/palladius/gemini-cli-custom-commands
# Update
gemini extensions update palladius-common-commands
gemini extensions update --all
# Uninstall
gemini extensions uninstall palladius-common-commands
```

To see which commands you have installed, for pure curiosity:

`find  ~/.gemini/extensions/palladius-common-commands/commands/ -name \*.toml`

## Wow factor

Once installed, run `just check-for-updates`. Or if you don't have `just` installed, you can "just" do `gemini -y -c "/pcc:check-for-updates"`

Sample output:

```markdown
# Extension Update Check

## Versions

*   **Local Version:** 0.0.1
*   **Remote Version:** 0.0.3

## Action

The remote version is newer. To update, run the following command: `gemini extensions update palladius-common-commands`

```
