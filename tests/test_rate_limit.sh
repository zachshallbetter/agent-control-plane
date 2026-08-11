#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"; tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
cat > "$tmp/rate.json" <<'JSON'
{"resources":{"graphql":{"limit":5000,"used":5003,"remaining":0,"reset":1786430048}},"checked_at":1786429976}
JSON
out="$(ACP_RATE_LIMIT_CACHE="$tmp/rate.json" ACP_RATE_LIMIT_MIN_INTERVAL=3600 "$root/scripts/rate-limit.sh")"
echo "$out" | jq -e '.decision=="RATE_LIMITED" and .graphql.remaining==0 and .reset_utc=="2026-08-11T06:34:08Z"' >/dev/null
echo "rate-limit tests passed"
