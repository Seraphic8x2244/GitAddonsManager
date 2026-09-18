from pathlib import Path
p = Path('GitAddonsManager_branch_fix.patch').read_text(encoding='utf-8')
checks = {
    'abbreviated upstream branch': 'git_branch_name(&upstream_name, lbr)',
    'tracking branch setup': 'git_branch_set_upstream(nlbr, upstream_name)',
    'upstream lookup checked': 'remoteError == GIT_OK',
    'empty remote fetch guard': 'remote.trimmed().isEmpty()',
}
missing = [name for name, needle in checks.items() if needle not in p]
if missing:
    raise SystemExit('Missing: ' + ', '.join(missing))
print('Patch contains all expected branch/upstream fixes.')
