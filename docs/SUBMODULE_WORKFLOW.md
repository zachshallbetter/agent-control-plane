# Submodule-aware repository workflow

ACP treats repository topology as an admission fact, not an agent guess.

Set `REPOSITORY_ROOT` to the ecosystem integration repository and optionally set `REPOSITORY_PATH` to a direct path listed in `.gitmodules`. `scripts/topology-check.sh` verifies initialization, origin, cleanliness, and the current child commit before work begins.

- `root-integration`: work in the root and update a child pin only after the child commit is verified and available remotely.
- `child-repository`: work in `<child>/.wt/issue-<number>`; do not edit the parent checkout as child implementation.
- `multi-repository`: merge and evidence the child change first, then perform a separate root pin update.

`scripts/agent-start.sh` enforces the child worktree boundary whenever `REPOSITORY_ROOT` is set. Missing, dirty, uninitialized, or remote-mismatched repositories stop admission. Parent pin changes never authorize unreviewed child changes.
