#!/usr/bin/env bash
# Plan or apply a standard GitHub ProjectsV2 project. Dry-run is the default.
set -euo pipefail
OWNER=""; NAME=""; APPLY=false; REPOS=""
INTERVAL="${ACP_GITHUB_MUTATION_INTERVAL:-1}"
while [[ $# -gt 0 ]]; do case "$1" in --owner) OWNER="$2"; shift 2;; --name) NAME="$2"; shift 2;; --repositories) REPOS="$2"; shift 2;; --apply) APPLY=true; shift;; --interval) INTERVAL="$2"; shift 2;; *) echo "usage: $0 --owner ORG --name NAME --repositories owner/repo[,owner/repo] [--apply] [--interval SECONDS]" >&2; exit 2;; esac; done
[[ -n "$OWNER" && -n "$NAME" ]] || { echo 'owner and name are required' >&2; exit 2; }
declare -a FIELD_SPECS=(
  'Agent|TEXT|'
  'Component|SINGLE_SELECT|Verse Home,Library,Reader,Discovery,SSP,Operating Model'
  'Priority|SINGLE_SELECT|P0,P1,P2,P3'
  'Size|SINGLE_SELECT|XS,S,M,L,XL'
  'Portfolio Milestone|SINGLE_SELECT|M1 Repository Foundations,M2 Object Pipeline,M3 Scene Pipeline,M4 Manga Verse Playable,M5 Integration Tier 2,M6 Observed Validation Tier 3,M7 Creator Platform,M8 InfiniteVerse Expansion'
  'Gate|TEXT|'
  'Evidence State|TEXT|'
)
echo "create Project: $OWNER / $NAME"; for spec in "${FIELD_SPECS[@]}"; do IFS='|' read -r field dtype options <<<"$spec"; echo "create field: $field ($dtype)"; done
IFS=',' read -r -a repos <<< "$REPOS"; for repo in "${repos[@]}"; do [[ -n "$repo" ]] && echo "link repository: $repo"; done
if ! "$APPLY"; then echo 'dry-run only; pass --apply to mutate GitHub'; exit 0; fi
command -v gh >/dev/null || { echo 'gh is required' >&2; exit 78; }
quota="$("$(dirname "${BASH_SOURCE[0]}")/rate-limit.sh")"
jq -e '.decision == "AVAILABLE"' <<<"$quota" >/dev/null || { printf '%s\n' "$quota" >&2; echo 'BLOCKED: GitHub GraphQL quota is unavailable.' >&2; exit 78; }
url="$(gh project create --owner "$OWNER" --title "$NAME" --format json | jq -r .url)"
number="$(printf '%s' "$url" | sed -n 's#.*/projects/\([0-9]*\).*#\1#p')"
for spec in "${FIELD_SPECS[@]}"; do IFS='|' read -r field dtype options <<<"$spec"; if [[ "$dtype" == SINGLE_SELECT ]]; then gh project field-create "$number" --owner "$OWNER" --name "$field" --data-type "$dtype" --single-select-options "$options" >/dev/null; else gh project field-create "$number" --owner "$OWNER" --name "$field" --data-type "$dtype" >/dev/null; fi; [[ "$INTERVAL" == "0" ]] || sleep "$INTERVAL"; done
for repo in "${repos[@]}"; do [[ -n "$repo" ]] && gh project link "$number" --owner "$OWNER" --repo "$repo" >/dev/null; [[ "$INTERVAL" == "0" ]] || sleep "$INTERVAL"; done
echo "created Project #$number: $url"
