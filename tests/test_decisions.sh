#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"; tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
printf '%s\n' '{"issue":1,"project_item":"PVTI_test","repository":"org/repo","authorized_paths":["src"],"exclusions":["docs/private"],"dependencies":[],"acceptance_criteria":["x"],"evidence_requirements":["y"],"definition_of_done":["z"],"status":"Ready"}' > "$tmp/packet.json"
printf '%s\n' 'src/main.py' > "$tmp/files"
PACKET="$tmp/packet.json" "$root/scripts/admission.sh" >/dev/null
PACKET="$tmp/packet.json" FILES="$tmp/files" "$root/scripts/scope-audit.sh" >/dev/null
SCOPE_PASSED=true CHECKS_PASSED=true HUMAN_ACKNOWLEDGED=true "$root/scripts/qualification.sh" >/dev/null
echo 'decision tests passed'
