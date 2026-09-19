# GitAddonsManager

A maintained Windows build of GitAddonsManager, based on WobLight's original project and focused on fixing long-standing issues and improving day-to-day addon management.

Upstream project: WobLight/GitAddonsManager  
Current upstream base: `4cfafffd4e48038203622f201729349b8e8b9809`

## Current improvements

### Multi-branch addon handling

Fixes broken local branch tracking when addons expose multiple remote branches.

The fix:

- creates local branches with the correct upstream branch name;
- checks branch-name lookup errors;
- safely handles repositories with missing upstream metadata;
- refuses to fetch an empty/invalid remote.

Existing addon folders already damaged by the previous branch handling may need to be deleted and cloned again once.

### GitHub release updater

The maintained build uses releases from this repository for self-updates rather than WobLight's historical GitLab CI artifacts.

### UI improvements

UI work is ongoing. Planned work includes configurable text sizing, cleaner bulk-action layout, consistent branch selectors, column/layout controls, a compact removal confirmation, and better multiple-WoW-directory management.

## Build

GitHub Actions:

1. clones the pinned WobLight upstream commit;
2. applies the maintained fixes/enhancements with guarded source transformations;
3. validates the resulting source diff;
4. uses the original Wine/Qt Windows build path;
5. uploads a portable Win64 build.

The original WobLight project remains credited in the application About page and here as the upstream source.
