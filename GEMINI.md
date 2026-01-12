This is a collection of Gemini CLI Custom Commands which is shared as an extension here:

Since it has a certain visibility, we need to ensure that:

1. CHANGELOG is up to date with any VERSION change we do.
2. VERSION is found in `gemini-extension.json`


## Symlinks

Note: Currently `./gemini/commands/` is symlinked against `commands/` to provide dogfooding capabilities. Let's make sure new functionality is add ( and `git add`ed) to `commands/`.

When in doubt, check the official vanilla repo: https://github.com/gemini-cli-extensions/security/

## About Custyom Commands

A Custom Command from [Gemini CLI](https://github.com/google-gemini/gemini-cli) works like this:

1. It's written as `.gemini/commands/path/to/file.toml`
2. It's invoked via `/path:to:file some string arguments`
3. Arguments are passes to the file as `{ { args } }` (without spaces).

Public docs on Custom commands is [here](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/custom-commands.md).

## Feedback Loop

When working on new features, ensure that you keep:

* The User Manual up-to-date.
* The `CHANGELOG.md` up to date.
* Ask user if you need to bump the version. Here's the author ideas:
  * Any new script warrants a minor version bump (0.0.42 -> 0.0.43).
  * A major change/restucturing warrants a mediummiddle version bump (0.0.42 -> 0.1.0).
  * A change in docs, readme, ... whcih does NOT alter the scripts majorly should stay in current version.
* use `gitmoji` for commits and changelog entries. If you propose a commit change yourself, please add some sort of AI signature, eg ("-- made with AntiGravity" or "-- made with Gemini CLI", .. whichever feels best).

## Documentation

* All commands under commands/ should be available in `docs/USER_MANUAL.md`.
* Whenever a file is added or moved, trigger a comparative search between that file.
* If you changed `docs/USER_MANUAL.md`, also bring those changes, summarized, under the `README.md`.


## DONT's

 * this project does NOT need a cloudbuild.