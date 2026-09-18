# GitAddonsManager branch-fix status

## Current state
- Branch: `main`
- Target build: Win64 portable package
- Upstream base: WobLight GitAddonsManager commit `4cfafffd4e48038203622f201729349b8e8b9809`
- Upstream describe seen in CI: `v1.1.0-20-g4cfafff`
- Latest successful build: GitHub Actions run #8 (`35403533681`)
- Artifact: `GitAddonsManager-Win64-branchfix` (artifact ID `10571910686`)

## Latest commits
- `99cbce3` — Fix QuaZip package path in Win64 build
- `9011200` — Document build handoff after run 7
- `3f4c7a8` — Handle all four Wine install prefixes
- `8aba0dd` — Fix Wine paths for all Windows dependencies
- `da64c65` — Patch generated CMake install prefix robustly

## Completed
- Build harness clones the exact WobLight base commit.
- `apply_branch_fix.py` applies and verifies the branch-selection fix.
- Current Wine/CMake install-prefix incompatibilities are patched in CI.
- zlib, libgit2 and QuaZip build/install successfully under Wine in CI.
- Stale final-build QuaZip 1.5 lookup is patched to the installed 1.7.2 package path.
- Run #8 completed successfully.
- Portable Win64 artifact was uploaded successfully.

## Untested
- The generated Windows build has not yet been launched on the user's Windows system.
- The branch-selection fix still needs a real addon install/update test against a repository whose default/content branch exposes the original bug.

## Deferred
- Non-blocking warnings (Vulkan headers, Git executable discovery, XDG runtime warning, Node action deprecation) can be cleaned up later.

## Exact next step
Download the run #8 artifact, extract it, launch GitAddonsManager, then test the branch-fix behavior with the addon/repository that previously failed.
