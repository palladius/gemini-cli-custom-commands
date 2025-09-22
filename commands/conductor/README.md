
My colleague https://github.com/keithballinger/ has created a beautiful assortment of
prompts that define architecture, plan, style guides, workflows, and intent.

# Actions

This Custom Commands folder contains two sub-commands:

## do.toml

Simply says

```markdown
Check for file `conductor.md`.

1. If the file doesn't exist, suggest user to launch "/conductor:install" and fail nicely, ignoring the following.
2. If the file exists, use the process outlined in conductor.md to execute the  following action:

## User input

{{args}}
```


## install.toml

This is to check installation and does the following:

1. If `CWD/.conductor/` exists and `conductor.md` exists , all good.
   1. => Exit 0
2. If not, git clone https://github.com/keithballinger/.conductor in tmp/ and copy:
   1.  the `.conductor/` folder to local `./.conductor/` (local folder)
   2.  the `conductor.md` file to local `./conductor.md`
   3.  Check its all good
       1.  exit 0
3. If the process fails in anyway, create a `CONDUCTOR_INSTALL_FAILURE.md` with details on how and why it failed, and ask the user to take it from there.
