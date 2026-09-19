# GitAddonsManager development status

## Current state
- Repository: `Seraphic8x2244/GitAddonsManager`
- Branch: `main`
- Upstream base: WobLight GitAddonsManager commit `4cfafffd4e48038203622f201729349b8e8b9809`
- Current installed/test version: `v1.1.0-branchfix.2`
- Next version: `v1.2.0`
- Latest successful build: GitHub Actions run #15 (`35440254493`)
- Clean artifact: `GitAddonsManager-Win64` (artifact ID `10583616398`)
- Legacy updater bridge artifact: `GitAddonsManager-Win64-branchfix` (artifact ID `10584145660`)
- Project direction: maintained GitAddonsManager fork; branch-fix naming is retired except for one-time compatibility.

## Latest commits
- `c02b587` — Rebrand README for maintained GitAddonsManager
- `cc5c722` — Fix CMake token matching in enhancement script
- `008911b` — Use robust GAM enhancement applicator
- `f241b71` — Apply maintained GAM enhancements robustly
- `907c71d` — Rebrand next build as GitAddonsManager v1.2.0
- `14e9127` — Record GitAddonsManager repository rename

## Completed
- Multi-branch/upstream handling fix is applied and runtime-tested on a fresh addon clone.
- Repository renamed from `GitAddonsManager-branchfix` to `GitAddonsManager`.
- README and build identity now describe a maintained GitAddonsManager fork rather than a one-off branch fix.
- About page points to `Seraphic8x2244/GitAddonsManager` and keeps WobLight/upstream attribution.
- Self-update code now targets this repository's GitHub releases.
- New updater prefers `GitAddonsManager-Win64.zip` and accepts the old `GitAddonsManager-Win64-branchfix.zip` as a fallback.
- Version comparison supports migration from `v1.1.0-branchfix.x` to normal versions such as `v1.2.0`.
- Enhancements are applied by guarded Python source transformations rather than fragile hand-edited diff hunks.
- `v1.2.0` Win64 build completed successfully.
- Build produces both clean and legacy-named artifacts for the one-time updater transition.

## Untested
- `v1.2.0` still needs a Windows runtime check.
- The updater needs an end-to-end test from the installed `v1.1.0-branchfix.2` to a published `v1.2.0` release.
- Wider regression testing across addon repositories remains limited.

## Transition requirement
For the `v1.2.0` GitHub release, upload both:
- `GitAddonsManager-Win64.zip`
- `GitAddonsManager-Win64-branchfix.zip`

The two files contain the same build. The legacy filename is needed only because `v1.1.0-branchfix.2` specifically searches for it. After users can update to `v1.2.0`, future releases can use only the clean filename.

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
Publish `v1.2.0` with both transition assets, leave the installed `v1.1.0-branchfix.2` in place, and use its in-app updater to move to `v1.2.0`. Once that succeeds, begin the font-size / toolbar / branch-width UI batch for the next release.
