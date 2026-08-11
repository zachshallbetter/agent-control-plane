#!/usr/bin/env bash
set -euo pipefail
: "${DATABASE:=.acp/evidence.sqlite3}"
python3 - "$DATABASE" <<'PY'
import sqlite3,sys
db=sqlite3.connect(sys.argv[1]); rows=db.execute('SELECT COUNT(*), MAX(created_at) FROM evidence').fetchone(); db.close()
print(f'evidence records={rows[0]} latest={rows[1] or "none"}')
PY
