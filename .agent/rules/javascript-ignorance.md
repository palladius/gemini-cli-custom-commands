---
trigger: glob
globs: *.js,*.ts
---

I don't know anything about JavaScript and Typescript. 
Take particular care in:
1. Readability (comments, DRYness, ..)
2. Abstraction of constants into a separate file which I can then edit myself (kudos if its YAML, in suborder JSON).
3. Tests. Every JS/TS file needs to be unit testable and somewhat included in the `just test` target
