This is a collection of Gemini CLI Custom Commands which is shared as an extension here:

Since it has a certain visibility, we need to ensure that:

1. CHANGELOG is up to date with any VERSION change we do.
2. VERSION is found in `gemini-extension.json`


## Symlinks

Note: Currently  `./gemini/commands/` is symlinked against `commands/` to provide dogfooding capabilities. Let's make sure new functionality is add ( and `git add`ed) to `commands/`.

When in doubt, check the official vanilla repo: https://github.com/gemini-cli-extensions/security/

## Feedback Loop

When working on new features, ensure that you keep:

* The User Manual up-to-date.
* The `CHANGELOG.md` up to date.
* Ask user if you need to bump the version. Here's the author ideas:
  * Any new script warrants a minor version bump (0.0.42 -> 0.0.43).
  * A major change/restucturing warrants a mediummiddle version bump (0.0.42 -> 0.1.0).
  * A change in docs, readme, ... whcih does NOT alter the scripts majorly should stay in current version.
