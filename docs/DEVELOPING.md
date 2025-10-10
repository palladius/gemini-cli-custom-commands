



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
