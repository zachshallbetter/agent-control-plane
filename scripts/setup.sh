#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="${ACP_CONFIG_FILE:-$HOME/.config/agent-control-plane/config.env}"
mkdir -p "$(dirname "$CONFIG")"
command -v python3 >/dev/null || { echo 'BLOCKED: python3 is required' >&2; exit 78; }
command -v git >/dev/null || { echo 'BLOCKED: git is required' >&2; exit 78; }
ask() { local answer; read -r -p "$1 [y/N] " answer; [[ "$answer" =~ ^[Yy]$ ]]; }
github_project_scope() {
  command -v gh >/dev/null 2>&1 || return 1
  gh auth status --hostname github.com --json hosts 2>/dev/null \
    | jq -e '.hosts["github.com"][0].scopes | index("project") != null' >/dev/null 2>&1
}
ensure_github_project_scope() {
  if github_project_scope; then
    echo 'GitHub authentication already has the project scope; no device flow required.'
    return 0
  fi
  echo 'GitHub project scope is missing; one explicit refresh is required.'
  gh auth refresh --hostname github.com --scopes project
  github_project_scope || { echo 'BLOCKED: GitHub project scope was not granted.' >&2; return 78; }
}
if ! command -v gh >/dev/null; then echo 'INFO: gh not installed; GitHub adapter unavailable'; elif ask 'Configure GitHub authentication?'; then gh auth login; ensure_github_project_scope; fi
if ! command -v railway >/dev/null; then echo 'INFO: railway CLI not installed; Railway adapter unavailable'; elif ask 'Configure Railway authentication?'; then railway login; fi
if ! command -v vercel >/dev/null; then echo 'INFO: vercel CLI not installed; Vercel adapter unavailable'; elif ask 'Configure Vercel authentication?'; then vercel login; fi
if [[ ! -f "$CONFIG" ]]; then
  umask 077
  { echo "ACP_ROOT=$ROOT"; echo "ACP_POLICY_VERSION=0.1.0"; echo "ACP_CORPUS_DIR=$ROOT/.llms"; } > "$CONFIG"
  echo "created $CONFIG"
else echo "using $CONFIG"; fi
python3 "$ROOT/scripts/gen-context.py"
for tool in gh railway vercel; do command -v "$tool" >/dev/null 2>&1 && echo "capability: $tool available" || echo "capability: $tool unavailable"; done
"$ROOT/scripts/doctor.sh"
echo 'Setup complete. Run: ./acp.py admission --packet <packet.json>'
