#!/usr/bin/env bash
set -euo pipefail
[[ "${SCOPE_PASSED:-false}" == true && "${CHECKS_PASSED:-false}" == true && "${HUMAN_ACKNOWLEDGED:-false}" == true ]] || { echo '{"decision":"BLOCKED","reason":"scope, checks, and human acknowledgement are required"}'; exit 78; }
echo '{"decision":"QUALIFIED","reason":"scope, checks, and human acknowledgement passed"}'
