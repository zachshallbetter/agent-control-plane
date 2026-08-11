#!/usr/bin/env bash
set -euo pipefail
: "${PACKET:?PACKET is required}"
: "${BRANCH:?BRANCH is required}"; : "${WORKTREE:?WORKTREE is required}"
decision="$(PACKET="$PACKET" ./scripts/admission.sh)"
[[ "$(printf '%s' "$decision" | python3 -c 'import json,sys; print(json.load(sys.stdin)["decision"])')" == APPROVED ]] || { printf '%s\n' "$decision" >&2; exit 78; }
[[ "$BRANCH" =~ ^(feat|fix|docs|chore|coord)/[0-9]+-[a-z0-9._/-]+$ ]] || { echo '{"decision":"INVALID","reason":"branch must be type/issue-slug"}' >&2; exit 1; }
[[ ! -e "$WORKTREE" ]] || { echo '{"decision":"REJECTED","reason":"worktree already exists"}' >&2; exit 1; }
mkdir -p "$(dirname "$WORKTREE")"
git worktree add "$WORKTREE" -b "$BRANCH" HEAD
printf '%s\n' "$decision"; echo "worktree=$WORKTREE"
