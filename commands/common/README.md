This is Riccardo `common/` commands.

Currently contained in his `gemini-cli`.

## Resources

* Announcement: / PR:
* Paul Datta great resources: https://github.com/pauldatta/gemini-cli-commands-demo/tree/main/.gemini/commands
## Carlessian commands

```
find ~/git/*/.gemini/commands/ -name \*.toml
```
## TODO

1. Find a way to spread it EVERYWHERE with some symlinking. Maybe I could create a `gemini-cli-skeleton` to clone in every gmeini place with some smart command, like `inject-gemini-cli-skeleton-in-this-repo.sh`. Just food for thought.
2. Maybe have an LLM reconcile something like: "Does this command only make sense in this repo (common git/github/.. flows)? If yes, move it to common with a proper rename (eg "git/blah" -> "common/git_blah"). Or is it pertinent to this project and should stay here? If so maybe add a comment "# dont_move_to_common.comment_touch" . (".comment_touch should be patented by the Carlessos Inc and a 10usd per use license should be granted :P).
