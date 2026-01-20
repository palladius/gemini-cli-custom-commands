---
description: Add standard Carlessian test cases
---

* Generate unit tests for each file and each method.
* Make sure the unit tests are named similar to files but with `_test` suffix
* Tests should be colorful (as appropriate) and contain fun emojis. Useful AND fun can coexist!
* If main folder has a Makefile or, better, a `justfile`, ensure there's a target for it (show example in JUST):
     1. If iot doesnt exist, `just test` should trigger a ~quick round of unit tests.
     2. If it exists, it should ALSO trigger unit tests (the faster cycle should run first).
* It's important that ALL tests can run in a single simple command independently on the language used.
* This test should also be integrated in the CI (eg, GitHUb Actions, or Cloud Build) under the promise that a failing test CAN be pushed to main but CANNOT be pushed to prod, or staging!