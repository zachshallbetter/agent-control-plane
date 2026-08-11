#!/usr/bin/env bash
# Bounded GitHub quota probe. Cache contains quota metadata only, never secrets.
set -euo pipefail
CACHE="${ACP_RATE_LIMIT_CACHE:-${XDG_CACHE_HOME:-$HOME/.cache}/acp/github-rate-limit.json}"
MIN_AGE="${ACP_RATE_LIMIT_MIN_INTERVAL:-30}"; now="$(date +%s)"
mkdir -p "$(dirname "$CACHE")"; refresh=1
if [[ -s "$CACHE" ]]; then
  stamp="$(jq -r '.checked_at // 0' "$CACHE" 2>/dev/null || printf 0)"
  (( now - stamp < MIN_AGE )) && refresh=0
fi
if (( refresh )); then
  raw="$(gh api rate_limit)" || { echo '{"decision":"BLOCKED","reason":"GitHub rate-limit endpoint unavailable"}' >&2; exit 78; }
  tmp="$CACHE.tmp.$$"; jq --argjson checked_at "$now" '. + {checked_at:$checked_at}' <<<"$raw" > "$tmp" && mv "$tmp" "$CACHE"
fi
reset="$(jq -r '.resources.graphql.reset' "$CACHE")"
reset_local="$(date -r "$reset" '+%Y-%m-%dT%H:%M:%S %Z')"
jq -c --arg reset_local "$reset_local" '{decision:(if .resources.graphql.remaining > 0 then "AVAILABLE" else "RATE_LIMITED" end), graphql:.resources.graphql, checked_at, reset_utc:(.resources.graphql.reset | strftime("%Y-%m-%dT%H:%M:%SZ")), reset_local:$reset_local}' "$CACHE"
