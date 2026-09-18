# GitAddonsManager branch-fix build

This repository builds a patched Windows version of WobLight/GitAddonsManager from exact upstream commit `4cfafffd4e48038203622f201729349b8e8b9809`.

## Fixes

1. **Remote branch -> local branch tracking**
   - Based on upstream MR !2 (`tuxpaint/fix-branches`).
   - Uses the abbreviated remote-tracking branch name such as `origin/dev` with `git_branch_set_upstream()`.
   - Checks the result of `git_branch_name()`.

2. **Missing-upstream defensive handling**
   - A failed upstream-remote lookup no longer becomes an empty remote that is later fetched.
   - `fetchRemote()` explicitly refuses an empty remote and logs a warning.

## Expected behaviour

Selecting `origin/dev` should create/check out local `dev` with tracking metadata equivalent to:

```ini
[branch "dev"]
    remote = origin
    merge = refs/heads/dev
```

Subsequent refreshes should fetch `origin` normally.

## Build

GitHub Actions:

1. clones the exact WobLight base commit;
2. runs `apply_branch_fix.py`, which requires each intended source fragment to match exactly once;
3. validates the resulting diff;
4. uses WobLight's own `CI.mk` Wine/Qt Windows build path;
5. uploads the portable build as `GitAddonsManager-Win64-branchfix`.

The build artifact also includes the exact generated source diff as `GitAddonsManager_branch_fix.generated.patch`.
