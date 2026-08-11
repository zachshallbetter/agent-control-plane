#!/usr/bin/env bash
set -euo pipefail
: "${PACKET:?PACKET is required}"
python3 - "$PACKET" <<'PY'
import json,sys
p=json.load(open(sys.argv[1])); required='issue project_item repository authorized_paths exclusions dependencies acceptance_criteria evidence_requirements definition_of_done'.split()
missing=[k for k in required if not p.get(k)]
if missing: print(json.dumps({'decision':'INVALID','missing':missing})); raise SystemExit(1)
if p.get('status')!='Ready': print(json.dumps({'decision':'BLOCKED','reason':'Project item is not Ready'})); raise SystemExit(78)
if p.get('unresolved_dependencies'): print(json.dumps({'decision':'BLOCKED','dependencies':p['unresolved_dependencies']})); raise SystemExit(78)
print(json.dumps({'decision':'APPROVED','issue':p['issue'],'project_item':p['project_item'],'repository':p['repository']}))
PY
