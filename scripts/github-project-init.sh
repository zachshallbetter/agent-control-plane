#!/usr/bin/env bash
# Plan or apply a standard GitHub ProjectsV2 project. Dry-run is the default.
set -euo pipefail
OWNER=""; NAME=""; APPLY=false; REPOS=""
while [[ $# -gt 0 ]]; do case "$1" in --owner) OWNER="$2"; shift 2;; --name) NAME="$2"; shift 2;; --repositories) REPOS="$2"; shift 2;; --apply) APPLY=true; shift;; *) echo "usage: $0 --owner ORG --name NAME --repositories owner/repo[,owner/repo] [--apply]" >&2; exit 2;; esac; done
[[ -n "$OWNER" && -n "$NAME" ]] || { echo 'owner and name are required' >&2; exit 2; }
echo "create Project: $OWNER / $NAME"; for field in Agent Component Priority Size 'Portfolio Milestone' Gate 'Evidence State'; do echo "create field: $field"; done
IFS=',' read -r -a repos <<< "$REPOS"; for repo in "${repos[@]}"; do [[ -n "$repo" ]] && echo "link repository: $repo"; done
if ! "$APPLY"; then echo 'dry-run only; pass --apply to mutate GitHub'; exit 0; fi
command -v gh >/dev/null || { echo 'gh is required' >&2; exit 78; }
url="$(gh project create --owner "$OWNER" --title "$NAME" --format json | jq -r .url)"
number="$(printf '%s' "$url" | sed -n 's#.*/projects/\([0-9]*\).*#\1#p')"
for field in Agent Component Priority Size 'Portfolio Milestone' Gate 'Evidence State'; do gh project field-create "$number" --owner "$OWNER" --name "$field" --data-type TEXT >/dev/null; done
for repo in "${repos[@]}"; do [[ -n "$repo" ]] && gh project link "$number" --owner "$OWNER" --repo "$repo" >/dev/null; done
echo "created Project #$number: $url"
