# GitAddonsManager branch-fix status

## Current state
- Branch: `main`
- Target build: Win64 portable package
- Upstream base: WobLight GitAddonsManager commit `4cfafffd4e48038203622f201729349b8e8b9809`
- Upstream describe seen in CI: `v1.1.0-20-g4cfafff`
- Latest build run checked: GitHub Actions run #7 (`35401927364`) — failed during final GitAddonsManager CMake generation.

## Latest commits
- `3f4c7a8` — Handle all four Wine install prefixes
- `8aba0dd` — Fix Wine paths for all Windows dependencies
- `da64c65` — Patch generated CMake install prefix robustly

## Completed
- Build harness clones the exact WobLight base commit.
- `apply_branch_fix.py` applies and verifies the branch-selection fix.
- Current Wine/CMake install-prefix incompatibilities are patched in CI.
- zlib, libgit2 and QuaZip now build/install successfully under Wine in CI.

## Untested
- No successful portable EXE/package has been produced yet.
- The branch-selection fix has not yet been runtime-tested in the Windows application.

## Deferred
- Non-blocking warnings (Vulkan headers, Git executable discovery, XDG runtime warning, Node action deprecation) can be cleaned up after a successful package build.

## Exact next step
Patch the stale final-build QuaZip CMake package path. Run #7 installed QuaZip under `QuaZip-Qt6-1.7.2`, while the final CMake invocation still points to `QuaZip-Qt6-1.5`. Then trigger the next build and inspect the result.
