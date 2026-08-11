#!/usr/bin/env bash
set -euo pipefail
: "${REPOSITORY:?REPOSITORY is required}"; : "${EXPECTED_REMOTE:?EXPECTED_REMOTE is required}"
actual="$(git -C "$REPOSITORY" remote get-url origin)"
[[ "$actual" == "$EXPECTED_REMOTE" ]] || { echo "repository mismatch: $actual" >&2; exit 1; }
[[ -z "$(git -C "$REPOSITORY" status --porcelain)" ]] || { echo "repository has uncommitted changes" >&2; exit 1; }
echo "repository baseline passed"
