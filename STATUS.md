# GitAddonsManager branch-fix status

## Current state
- Branch: `main`
- Target build: Win64 portable package
- Upstream base: WobLight GitAddonsManager commit `4cfafffd4e48038203622f201729349b8e8b9809`
- Upstream describe seen in CI: `v1.1.0-20-g4cfafff`
- Latest successful build: GitHub Actions run #8 (`35403533681`)
- Artifact: `GitAddonsManager-Win64-branchfix` (artifact ID `10571910686`)
- Branch-fix runtime test: fresh clone successfully discovered branches and switched branches.

## Latest commits
- `41c6348` — Record successful Win64 build
- `99cbce3` — Fix QuaZip package path in Win64 build
- `9011200` — Document build handoff after run 7
- `3f4c7a8` — Handle all four Wine install prefixes

## Completed
- Build harness clones the exact WobLight base commit.
- `apply_branch_fix.py` applies and verifies the branch-selection fix.
- Current Wine/CMake install-prefix incompatibilities are patched in CI.
- zlib, libgit2 and QuaZip build/install successfully under Wine in CI.
- Portable Win64 artifact builds and uploads successfully.
- Fresh-clone branch discovery/switching has been validated by the user.

## Untested
- Existing repositories with stale/bad Git metadata are intentionally not repaired; affected addon folders need a clean re-clone.
- Wider regression testing across many addon repositories is still limited.

## Deferred
- Non-blocking CI warnings (Vulkan headers, Git executable discovery, XDG runtime warning, Node action deprecation).
- Removal dialog redesign with collapsible file list.
- Management of multiple WoW/addon directories.

## UI phase requested
Prefer opt-in settings rather than changing upstream defaults where practical.

Requested near-term work:
- Update About tab to point at this fork/repository.
- Add an in-app update path for this fork as soon as practical.
- Add user control over UI/tab text size; auto-resize button heights to fit.
- Move addon-directory control above the bulk-action buttons.
- Reorder bulk buttons to: Upgrade All, Refresh, Download, Export.
- Add column-management control (lock/settings button), including header visibility and drag reordering if feasible.
- Normalize branch dropdown widths; current widths appear inconsistent.
- Preserve base behaviour by default where practical.

## Exact next step
Audit the upstream UI/settings implementation to identify the smallest safe first batch: About/repository link, persistent UI font-size option, toolbar layout/order, branch-combo sizing, and feasibility of persistent column controls and self-update.
