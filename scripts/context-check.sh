#!/usr/bin/env bash
set -euo pipefail
: "${CURRENT_CORPUS:?CURRENT_CORPUS is required}"; : "${VERSIONED_CORPUS:?VERSIONED_CORPUS is required}"
cmp -s "$CURRENT_CORPUS" "$VERSIONED_CORPUS" || { echo '{"decision":"BLOCKED","reason":"context corpus is stale"}' >&2; exit 78; }
if [[ -n "${MANIFEST_FILE:-}" ]]; then
  python3 - "$MANIFEST_FILE" "$CURRENT_CORPUS" <<'PY'
import hashlib,json,sys
m=json.load(open(sys.argv[1])); actual=hashlib.sha256(open(sys.argv[2],'rb').read()).hexdigest()
if actual != m.get('llms_full_sha256'): print('{"decision":"BLOCKED","reason":"context manifest hash mismatch"}'); raise SystemExit(78)
PY
fi
printf '{"decision":"APPROVED","corpus":"%s"}\n' "$VERSIONED_CORPUS"
