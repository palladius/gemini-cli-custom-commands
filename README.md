# gemini-cli-custom-commands

Inspired by https://github.com/google-gemini/gemini-cli-security/tree/main

This is a collection of all Carlessian commands, packaged into one.

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
