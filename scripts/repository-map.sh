#!/usr/bin/env bash
set -euo pipefail
: "${REPOSITORY_ROOT:?REPOSITORY_ROOT is required}"
: "${MAP_FILE:=.acp/repositories.tsv}"
mkdir -p "$(dirname "$MAP_FILE")"; : > "$MAP_FILE"
find "$REPOSITORY_ROOT" -type d -name .git -prune -print | while IFS= read -r dotgit; do
  repo="${dotgit%/.git}"; remote="$(git -C "$repo" remote get-url origin 2>/dev/null || true)"
  [[ -n "$remote" ]] && printf '%s\t%s\n' "$repo" "$remote" >> "$MAP_FILE"
done
sort -o "$MAP_FILE" "$MAP_FILE"; echo "repository map: $MAP_FILE"
