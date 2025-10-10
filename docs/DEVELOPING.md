# Dev manual

These are random thoughts that should NOT be visible in README but are still relevant to the author.

## Current Commands on your computer

To see which commands you have installed, for pure curiosity:

`find  ~/.gemini/extensions/palladius-common-commands/commands/ -name \*.toml`


## Wow factor

Once installed, run `just check-for-updates`. Or if you don't have `just` installed, you can "just" do `gemini -y -c "/pcc:check-for-updates"`.

Note this functionality has become useless since `0.4.1`'s `gemini extensions update --all`, but still: it's exciting to try genitive over version numbers!

Sample output:

```markdown
# Extension Update Check

## Versions

*   **Local Version:** 0.0.1
*   **Remote Version:** 0.0.3

## Action

The remote version is newer. To update, run the following command: `gemini extensions update palladius-common-commands`

```
