#!/usr/bin/env bash
set -euo pipefail
: "${PACKET:?PACKET is required}"
: "${BRANCH:?BRANCH is required}"; : "${WORKTREE:?WORKTREE is required}"
if [[ -n "${REPOSITORY_ROOT:-}" ]]; then
  REPOSITORY_PATH="${REPOSITORY_PATH:-}"
  REPOSITORY_ROOT="$REPOSITORY_ROOT" ./scripts/topology-check.sh "$REPOSITORY_PATH" >/dev/null
  TARGET_REPOSITORY="$REPOSITORY_ROOT${REPOSITORY_PATH:+/$REPOSITORY_PATH}"
  [[ "$WORKTREE" == "$TARGET_REPOSITORY/.wt/issue-"* ]] || { echo '{"decision":"INVALID","reason":"worktree must be under the owning repository .wt directory"}' >&2; exit 1; }
else
  TARGET_REPOSITORY="$(git rev-parse --show-toplevel)"
fi
decision="$(PACKET="$PACKET" ./scripts/admission.sh)"
[[ "$(printf '%s' "$decision" | python3 -c 'import json,sys; print(json.load(sys.stdin)["decision"])')" == APPROVED ]] || { printf '%s\n' "$decision" >&2; exit 78; }
[[ "$BRANCH" =~ ^(feat|fix|docs|chore|coord)/[0-9]+-[a-z0-9._/-]+$ ]] || { echo '{"decision":"INVALID","reason":"branch must be type/issue-slug"}' >&2; exit 1; }
[[ ! -e "$WORKTREE" ]] || { echo '{"decision":"REJECTED","reason":"worktree already exists"}' >&2; exit 1; }
mkdir -p "$(dirname "$WORKTREE")"
git -C "$TARGET_REPOSITORY" worktree add "$WORKTREE" -b "$BRANCH" HEAD
printf '%s\n' "$decision"; echo "repository=$TARGET_REPOSITORY"; echo "worktree=$WORKTREE"
