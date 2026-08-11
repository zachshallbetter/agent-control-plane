# CLI reference

The Python CLI is the provider-neutral reference implementation:

```bash
./acp.py admission --packet packet.json
./acp.py scope-audit --packet packet.json --files changed-files.txt
./acp.py qualification --scope-passed --checks-passed --human-acknowledged
./acp.py evidence --kind browser --file evidence.json --database .acp/evidence.sqlite3
./acp.py ledger --database .acp/evidence.sqlite3
```

Exit codes are stable: `0` is accepted, `1` is invalid/rejected, and `78` is blocked pending external action. Commands emit one JSON decision record per invocation.
