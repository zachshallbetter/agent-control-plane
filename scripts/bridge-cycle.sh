#!/usr/bin/env bash
set -euo pipefail
: "${DELIVERY_DATABASE:=.acp/deliveries.sqlite3}"; : "${DELIVERY_COMMAND:?DELIVERY_COMMAND is required}"
python3 - "$DELIVERY_DATABASE" "$DELIVERY_COMMAND" <<'PY'
import shlex,subprocess,sys
from delivery import DeliverySpool
spool=DeliverySpool(sys.argv[1]); command=shlex.split(sys.argv[2])
for delivery in spool.claim(10):
    try: subprocess.run(command+[delivery['id'],delivery['event']],check=True,timeout=120); spool.finish(delivery['id'],True)
    except Exception as exc: spool.finish(delivery['id'],False,str(exc))
PY
