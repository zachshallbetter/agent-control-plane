#!/usr/bin/env bash
set -euo pipefail
: "${WORKTREE:?WORKTREE is required}"
[[ -d "$WORKTREE" ]] || { echo "worktree does not exist: $WORKTREE" >&2; exit 1; }
git worktree remove "$WORKTREE"
git worktree prune
echo "cleaned exact worktree: $WORKTREE"
