#!/usr/bin/env bash
set -euo pipefail
: "${PACKET:?PACKET is required}"; : "${FILES:?FILES is required}"
python3 - "$PACKET" "$FILES" <<'PY'
import json,sys
p=json.load(open(sys.argv[1])); files=open(sys.argv[2]).read().splitlines(); bad=[]
for f in files:
  if any(f==x or f.startswith(x.rstrip('/')+'/') for x in p['exclusions']): bad.append([f,'excluded'])
  elif not any(f==x or f.startswith(x.rstrip('/')+'/') for x in p['authorized_paths']): bad.append([f,'outside authorized paths'])
if bad: print(json.dumps({'decision':'REJECTED','findings':bad})); raise SystemExit(1)
print(json.dumps({'decision':'APPROVED','files':len(files)}))
PY
