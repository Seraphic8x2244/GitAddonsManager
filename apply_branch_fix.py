from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: apply_branch_fix.py <path-to-addon.cpp>")

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")

replacements = [
    (
        """            check_git_return(git_branch_set_upstream(nlbr, git_reference_name(lbr)));""",
        """            const char *upstream_name = nullptr;
            check_git_return(git_branch_name(&upstream_name, lbr));
            check_git_return(git_branch_set_upstream(nlbr, upstream_name));""",
        "remote branch -> local branch upstream tracking"
    ),
    (
        """                (git_reference_is_remote(ref) ?
                    git_branch_remote_name :
                    git_branch_upstream_remote
                )(&buf, m_repo.get(), git_reference_name(ref));
                data.cr = buf.ptr;""",
        """                int remoteError = (git_reference_is_remote(ref) ?
                    git_branch_remote_name :
                    git_branch_upstream_remote
                )(&buf, m_repo.get(), git_reference_name(ref));
                if (remoteError == GIT_OK && buf.ptr && *buf.ptr)
                    data.cr = buf.ptr;
                else
                    data.cr.clear();""",
        "missing-upstream scan handling"
    ),
    (
        """void Addon::fetchRemote(QString remote)
{
    delegate(remote + " Fetch", [this, remote](){""",
        """void Addon::fetchRemote(QString remote)
{
    if (remote.trimmed().isEmpty()) {
        qWarning() << m_name << "Skipping fetch: current branch has no associated remote";
        return;
    }

    delegate(remote + " Fetch", [this, remote](){""",
        "empty-remote fetch guard"
    ),
]

for old, new, label in replacements:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {count}")
    text = text.replace(old, new, 1)
    print(f"Applied: {label}")

path.write_text(text, encoding="utf-8")
print(f"Patched {path}")
