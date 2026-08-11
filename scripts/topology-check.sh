#!/usr/bin/env bash
# Resolve and validate a repository or direct Git submodule without mutation.
set -euo pipefail
: "${REPOSITORY_ROOT:?REPOSITORY_ROOT is required}"
PATH_HINT="${1:-}"; TARGET="$REPOSITORY_ROOT"
if [[ -n "$PATH_HINT" ]]; then
  [[ -f "$REPOSITORY_ROOT/.gitmodules" ]] || { echo "no .gitmodules: $PATH_HINT" >&2; exit 1; }
  git -C "$REPOSITORY_ROOT" config --file .gitmodules --get-regexp '^submodule\..*\.path$' | awk '{print $2}' | grep -Fxq "$PATH_HINT" || { echo "not a direct submodule: $PATH_HINT" >&2; exit 1; }
  TARGET="$REPOSITORY_ROOT/$PATH_HINT"
  [[ -d "$TARGET/.git" || -f "$TARGET/.git" ]] || { echo "submodule is not initialized: $PATH_HINT" >&2; exit 1; }
fi
REMOTE="$(git -C "$TARGET" remote get-url origin 2>/dev/null || true)"
[[ -n "$REMOTE" ]] || { echo "repository has no origin: $TARGET" >&2; exit 1; }
[[ -z "$(git -C "$TARGET" status --porcelain)" ]] || { echo "repository is dirty: $TARGET" >&2; exit 1; }
ROLE=root-integration; [[ -n "$PATH_HINT" ]] && ROLE=child-repository
printf 'repository=%s\nremote=%s\nhead=%s\nrole=%s\n' "$TARGET" "$REMOTE" "$(git -C "$TARGET" rev-parse HEAD)" "$ROLE"
