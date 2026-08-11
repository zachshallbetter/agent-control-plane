#!/usr/bin/env bash
# Add existing issues or create issue items from a JSONL manifest. Dry-run by default.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OWNER="" PROJECT="" MANIFEST="" APPLY=false INTERVAL="${ACP_GITHUB_MUTATION_INTERVAL:-1}"
while [[ $# -gt 0 ]]; do case "$1" in --owner) OWNER="$2"; shift 2;; --project) PROJECT="$2"; shift 2;; --manifest) MANIFEST="$2"; shift 2;; --apply) APPLY=true; shift;; --interval) INTERVAL="$2"; shift 2;; *) echo "usage: $0 --owner ORG --project NUMBER --manifest FILE [--apply] [--interval SECONDS]" >&2; exit 2;; esac; done
[[ -n "$OWNER" && -n "$PROJECT" && -r "$MANIFEST" ]] || { echo 'owner, project, and readable manifest are required' >&2; exit 2; }
if "$APPLY"; then
  quota="$("$ROOT/scripts/rate-limit.sh")"
  jq -e '.decision == "AVAILABLE"' <<<"$quota" >/dev/null || { printf '%s\n' "$quota" >&2; echo 'BLOCKED: GitHub GraphQL quota is unavailable.' >&2; exit 78; }
fi
while IFS= read -r line; do [[ -n "$line" ]] || continue; url="$(printf '%s' "$line" | jq -r '.url // empty')"; title="$(printf '%s' "$line" | jq -r '.title // empty')"; [[ -n "$url" || -n "$title" ]] || { echo 'invalid manifest row' >&2; exit 1; }; if "$APPLY"; then if [[ -n "$url" ]]; then gh project item-add "$PROJECT" --owner "$OWNER" --url "$url" >/dev/null; else echo "draft creation requires issue provider: $title"; fi; [[ "$INTERVAL" == "0" ]] || sleep "$INTERVAL"; else echo "would add: ${url:-$title}"; fi; done < "$MANIFEST"
"$APPLY" || echo 'dry-run only; pass --apply to mutate GitHub'
