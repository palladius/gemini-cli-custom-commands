# Palladius Gemini CLI custom commands (or PCC)

Self: https://github.com/palladius/gemini-cli-custom-commands

This is a collection of all "Carlessian" commands, packaged into one place.

 ![Version](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/palladius/gemini-cli-custom-commands/main/gemini-extension.json&query=$.version&label=version&color=red&labelColor=blue) [![License](https://img.shields.io/badge/License-Apache%202.0-green?labelColor=yellow)](LICENSE)

- 📖 [User Manual](docs/USER_MANUAL.md)
- 📝 [Changelog](CHANGELOG.md)
- 💡 Inspired by [google-gemini/gemini-cli-security](https://github.com/google-gemini/gemini-cli-security) extension.
- 🚀 Referenced in the Official [Gemini CLI Extensions](https://geminicli.com/extensions/browse/) site (wOOt!)



**WARNING**: This project is intended for demonstration purposes only. It is not intended for use in a production environment.

## INSTALL

**Note** *(requires Gemini CLI v`0.4.0` or newer)*:

```bash
# 🔍 Check version
gemini -v
# 💛 Install
gemini extensions install https://github.com/palladius/gemini-cli-custom-commands
# 🔄 Update
gemini extensions update palladius-common-commands
gemini extensions update --all
# 🤢 Uninstall
gemini extensions uninstall palladius-common-commands
```

To see which commands you have installed, for pure curiosity:

`find  ~/.gemini/extensions/palladius-common-commands/commands/ -name \*.toml`

