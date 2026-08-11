#!/usr/bin/env bash
set -euo pipefail
owner="${GH_PROJECT_OWNER:-}"; project="${GH_PROJECT_NUMBER:-}"
while [[ $# -gt 0 ]]; do case "$1" in --owner) owner="$2"; shift 2;; --project) project="$2"; shift 2;; *) echo "usage: $0 [--owner ORG] [--project NUMBER]" >&2; exit 2;; esac; done
if [[ -n "$owner" && -n "$project" ]]; then
  gh project view "$project" --owner "$owner" --format json >/dev/null
  echo "PASS GitHub Project #$project access"
else
  echo "INFO GitHub Project not tested; pass --owner/--project or set GH_PROJECT_OWNER/GH_PROJECT_NUMBER"
fi
echo "PASS bounded doctor checks"
