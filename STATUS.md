# GitAddonsManager branch-fix status

## Current state
- Branch: `main`
- Upstream base: WobLight GitAddonsManager commit `4cfafffd4e48038203622f201729349b8e8b9809`
- Current fork build version: `v1.1.0-branchfix.2`
- Latest successful build: GitHub Actions run #12 (`35438873927`)
- Artifact: `GitAddonsManager-Win64-branchfix` (artifact ID `10582948848`)
- Public release currently published: `v1.1.0-branchfix.1`
- Branch-fix runtime test: fresh clone successfully discovered branches and switched branches.

## Latest commits
- `2e581ab` — Inject fork version without CI patch context
- `f46b3d2` — Remove CI.mk context from updater patch
- `49b5f9b` — Add GitHub release updater patch
- `7fb2fb6` — Add upstream source snapshot workflow
- `8d5691d` — Document UI improvement phase

## Completed
- Branch handling fix is applied to the pinned WobLight source.
- Portable Win64 package builds successfully.
- About page now links to the GitHub fork/issues while retaining upstream attribution.
- Self-update code is retargeted from WobLight GitLab CI artifacts to this fork's GitHub releases.
- Updater compares fork versions such as `v1.1.0-branchfix.1` / `.2`.
- Updater downloads the `GitAddonsManager-Win64-branchfix.zip` release asset.
- Updater extraction now supports the root-level layout used by GitHub release ZIPs.
- Build artifacts now retain `.installedFiles` for cleaner future self-updates.
- `v1.1.0-branchfix.2` embeds the correct fork version and GitHub release API URL.
- UI source audit completed.

## Untested
- `v1.1.0-branchfix.2` still needs to be launched on Windows.
- GitHub self-update needs an end-to-end test. Recommended path: manually install branchfix.2, publish branchfix.2, then publish a later test/UI release and update branchfix.2 through the app.
- Wider regression testing across addon repositories is limited.

## UI audit findings
- Branch dropdown widths vary because each ComboBox uses `implicitContentWidthPolicy: ComboBox.WidestText`; a long available branch widens that addon row even when the selected branch is short.
- Toolbar ordering and addon-directory presentation are QML-only and low risk.
- Global UI font sizing can be added as a persisted preference and inherited by controls so button/tab heights follow the font.
- The current addon list is a ListView with RowLayout delegates, not a true column/table model. Uniform widths are easy; draggable column reordering needs a deliberate layout-edit layer/refactor.
- Multiple addon directories already exist internally, but they are not presented as named WoW installations/profiles.
- The removal confirmation is currently a large always-visible file list and can be replaced by a compact confirmation with an expandable details section.

## Planned UI work
Prefer opt-in settings rather than changing upstream behaviour where practical.

Near-term:
- User-controlled UI text size with controls auto-sizing to content.
- Optional improved addon toolbar: directory control above actions and action order Upgrade All / Refresh / Download / Export.
- Normalize branch dropdown width.
- Design a layout-lock/column control without forcing a full table refactor.

Later:
- Compact addon-removal confirmation with expandable file list.
- Named management of multiple WoW directories/installations.

## Exact next step
Runtime-test the manually installed `v1.1.0-branchfix.2` build. Confirm the About page points to the fork and that startup/update checking does not report the older public `branchfix.1` as an update. If healthy, publish branchfix.2, then start the font/toolbar/branch-width UI batch for the next release so the new updater can be tested against it.
