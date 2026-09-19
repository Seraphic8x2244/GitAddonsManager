# GitAddonsManager development status

## Current state
- Repository: `Seraphic8x2244/GitAddonsManager`
- Branch: `main`
- Upstream base: WobLight GitAddonsManager commit `4cfafffd4e48038203622f201729349b8e8b9809`
- Installed/test build: `v1.1.0-branchfix.2`
- Latest successful build before repository rename: GitHub Actions run #12 (`35438873927`)
- Public release: `v1.1.0-branchfix.1`
- Next version: `v1.2.0`
- Project direction: maintained GitAddonsManager fork, no longer branded as a one-off branch fix.

## Completed
- Multi-branch/upstream handling fix is applied and runtime-tested on a fresh addon clone.
- Portable Win64 build pipeline works.
- About page/updater prototype builds successfully.
- GitHub repository renamed from `GitAddonsManager-branchfix` to `GitAddonsManager`.
- UI source audit completed.

## Untested
- GitHub self-update still needs an end-to-end release-to-release test.
- Wider regression testing across addon repositories remains limited.

## Transition requirement
The installed `v1.1.0-branchfix.2` updater still requests the old repository URL and the legacy release asset name `GitAddonsManager-Win64-branchfix.zip`. GitHub should redirect the renamed repository URL, but the first cleanly named release must preserve a legacy-named asset as an upgrade bridge. The new updater should accept both clean and legacy asset names.

## Planned UI work
Near-term:
- User-controlled UI text size with controls auto-sizing to content.
- Optional improved addon toolbar: directory control above actions and action order Upgrade All / Refresh / Download / Export.
- Normalize branch dropdown width.
- Design a layout-lock/column control without forcing a full table refactor.

Later:
- Compact addon-removal confirmation with expandable file list.
- Named management of multiple WoW directories/installations.

## Exact next step
Retarget source/About/updater URLs to `Seraphic8x2244/GitAddonsManager`, rename build/artifact identity, version the next build as `v1.2.0`, and preserve one legacy-named release asset so `v1.1.0-branchfix.2` can self-update into the clean version line.
