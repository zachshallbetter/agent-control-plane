#!/usr/bin/env bash
set -euo pipefail
: "${CURRENT_CORPUS:?CURRENT_CORPUS is required}"; : "${VERSIONED_CORPUS:?VERSIONED_CORPUS is required}"
cmp -s "$CURRENT_CORPUS" "$VERSIONED_CORPUS" || { echo '{"decision":"BLOCKED","reason":"context corpus is stale"}' >&2; exit 78; }
printf '{"decision":"APPROVED","corpus":"%s"}\n' "$VERSIONED_CORPUS"
