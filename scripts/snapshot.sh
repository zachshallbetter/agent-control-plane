#!/usr/bin/env bash
set -euo pipefail
: "${SNAPSHOT_FILE:=.acp/project-snapshot.json}"; : "${SNAPSHOT_SOURCE:?SNAPSHOT_SOURCE is required}"
lock="${SNAPSHOT_FILE}.lock"; stamp="${SNAPSHOT_FILE}.timestamp"; now="$(date +%s)"; min="${SNAPSHOT_MIN_INTERVAL:-60}"
if [[ -s "$SNAPSHOT_FILE" && -r "$stamp" ]]; then age=$((now-$(<"$stamp"))); [[ "$age" -ge 0 && "$age" -lt "$min" ]] && { echo "cached snapshot ($age seconds old)"; exit 0; }; fi
mkdir "$lock" 2>/dev/null || { echo "snapshot refresh already in progress" >&2; exit 78; }
trap 'rmdir "$lock" 2>/dev/null || true' EXIT
mkdir -p "$(dirname "$SNAPSHOT_FILE")"; cp "$SNAPSHOT_SOURCE" "$SNAPSHOT_FILE"; printf '%s\n' "$(date +%s)" > "$stamp"; echo "snapshot refreshed: $SNAPSHOT_FILE"
