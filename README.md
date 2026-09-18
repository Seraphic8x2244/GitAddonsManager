# GitAddonsManager branch-fix build

This patch targets WobLight/GitAddonsManager commit `4cfafffd4e48038203622f201729349b8e8b9809`.

It contains two related fixes:

1. **Remote branch -> local branch tracking fix**
   - Based on upstream MR !2 (`tuxpaint/fix-branches`).
   - Uses the abbreviated branch name (`origin/dev`) with `git_branch_set_upstream()` instead of the full ref (`refs/remotes/origin/dev`).
   - Also checks the return value from `git_branch_name()`.

2. **Missing-upstream defensive handling**
   - `scanBranches()` no longer treats a failed upstream-remote lookup as a valid empty remote.
   - `fetchRemote()` refuses to fetch an empty remote and logs a clear warning instead of producing `'' is not a valid remote name`.

## Expected result

After selecting `origin/dev`, GitAddonsManager should create/check out local `dev` and `.git/config` should contain equivalent tracking metadata:

```ini
[branch "dev"]
    remote = origin
    merge = refs/heads/dev
```

Subsequent refreshes should fetch `origin` normally.

## Build

The included GitHub Actions workflow clones the exact upstream base commit, applies `GitAddonsManager_branch_fix.patch`, then uses WobLight's own OpenSUSE/Wine/Qt Win64 build path from `CI.mk`.

The workflow artifact is named `GitAddonsManager-Win64-branchfix`.
