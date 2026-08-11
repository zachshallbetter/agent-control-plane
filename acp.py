#!/usr/bin/env python3
"""Agent Control Plane reference CLI: deterministic policy plus SQLite evidence ledger."""
from __future__ import annotations
import argparse, hashlib, json, sqlite3, sys, time
from pathlib import Path

POLICY_VERSION = "0.1.0"
DECISIONS = {"INVALID", "BLOCKED", "APPROVED", "REJECTED", "QUALIFIED"}

def stable(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))

def decision_id(decision: str, payload: dict) -> str:
    return hashlib.sha256(stable({"decision": decision, "policy_version": POLICY_VERSION, "payload": payload}).encode()).hexdigest()[:20]

def emit(decision: str, payload: dict, reason: str, code: int = 0) -> int:
    record = {"decision": decision, "decision_id": decision_id(decision, payload), "policy_version": POLICY_VERSION, "reason": reason, **payload}
    print(stable(record)); return code

def packet(path: str) -> dict:
    data = json.loads(Path(path).read_text())
    required = ("issue", "project_item", "repository", "authorized_paths", "exclusions", "dependencies", "acceptance_criteria", "evidence_requirements", "definition_of_done")
    missing = [key for key in required if key not in data or (key not in ("exclusions", "dependencies") and not data[key])]
    if missing: raise ValueError("missing required packet fields: " + ", ".join(missing))
    return data

def cmd_admission(args: argparse.Namespace) -> int:
    try: data = packet(args.packet)
    except (OSError, json.JSONDecodeError, ValueError) as exc: return emit("INVALID", {}, str(exc), 1)
    if data.get("status") != "Ready": return emit("BLOCKED", {"issue": data["issue"]}, "Project item is not Ready", 78)
    if data.get("unresolved_dependencies"): return emit("BLOCKED", {"issue": data["issue"], "blockers": data["unresolved_dependencies"]}, "declared dependency is unresolved", 78)
    return emit("APPROVED", {"issue": data["issue"], "project_item": data["project_item"], "repository": data["repository"]}, "issue packet is actionable")

def within(path: str, roots: list[str]) -> bool:
    return any(path == root or path.startswith(root.rstrip("/") + "/") for root in roots)

def cmd_scope(args: argparse.Namespace) -> int:
    try: data = packet(args.packet); files = Path(args.files).read_text().splitlines()
    except (OSError, json.JSONDecodeError, ValueError) as exc: return emit("INVALID", {}, str(exc), 1)
    findings = []
    for path in files:
        if within(path, data["exclusions"]): findings.append({"path": path, "reason": "excluded"})
        elif not within(path, data["authorized_paths"]): findings.append({"path": path, "reason": "outside authorized paths"})
    if findings: return emit("REJECTED", {"findings": findings}, "change exceeds issue-defined scope", 1)
    return emit("APPROVED", {"files": len(files)}, "all changed files are authorized")

def cmd_qualify(args: argparse.Namespace) -> int:
    if not (args.scope_passed and args.checks_passed and args.human_acknowledged):
        return emit("BLOCKED", {}, "scope, checks, and human acknowledgement are required", 78)
    return emit("QUALIFIED", {}, "scope, checks, and human acknowledgement passed")

def connect(path: str) -> sqlite3.Connection:
    db = sqlite3.connect(path); db.execute("PRAGMA busy_timeout=5000")
    db.execute("CREATE TABLE IF NOT EXISTS evidence (id TEXT PRIMARY KEY, created_at INTEGER NOT NULL, kind TEXT NOT NULL, payload TEXT NOT NULL)"); db.commit(); return db

def cmd_evidence(args: argparse.Namespace) -> int:
    payload = json.loads(Path(args.file).read_text())
    created = int(time.time()); ident = hashlib.sha256(f"{created}:{stable(payload)}".encode()).hexdigest()
    db = connect(args.database)
    db.execute("INSERT INTO evidence(id,created_at,kind,payload) VALUES(?,?,?,?)", (ident, created, args.kind, stable(payload))); db.commit(); db.close()
    print(stable({"evidence_id": ident, "kind": args.kind, "database": args.database})); return 0

def cmd_ledger(args: argparse.Namespace) -> int:
    db = connect(args.database); rows = db.execute("SELECT id,created_at,kind,payload FROM evidence ORDER BY created_at,id").fetchall(); db.close()
    print("\n".join(stable({"evidence_id": r[0], "created_at": r[1], "kind": r[2], "payload": json.loads(r[3])}) for r in rows)); return 0

def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.directory).resolve(); (root / ".acp").mkdir(parents=True, exist_ok=True)
    config = root / ".acp" / "config.json"
    if not config.exists(): config.write_text(stable({"policy_version": POLICY_VERSION, "statuses":{"ready":"Ready","review":"In review","done":"Done","verified":"Verified"},"retry":{"max_attempts":3,"base_seconds":2,"max_seconds":60},"providers":{"github":{"enabled":True},"railway":{"enabled":False},"vercel":{"enabled":False}},"snapshot_interval_seconds":60,"require_human_acknowledgement":True}) + "\n")
    print(stable({"decision":"APPROVED","initialized":str(root),"config":str(config)})); return 0

def cmd_policy(args: argparse.Namespace) -> int:
    from policy import load
    try: print(stable({"decision":"APPROVED","policy":load(args.file)})); return 0
    except (OSError,ValueError,json.JSONDecodeError) as exc: return emit("INVALID",{},str(exc),1)

def cmd_mode(args: argparse.Namespace) -> int:
    from operating_mode import as_dict, evaluate
    mode = evaluate(project_access=args.project_access, existing_lease=args.existing_lease,
                    lease_valid=args.lease_valid, now=args.now, reset_at=args.reset_at)
    print(stable({"decision": "APPROVED" if mode.name in ("normal", "continuation", "degraded") else "BLOCKED", **as_dict(mode)}))
    return 0 if mode.name in ("normal", "continuation", "degraded") else 78

def main() -> int:
    parser = argparse.ArgumentParser(prog="acp"); sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("admission"); p.add_argument("--packet", required=True); p.set_defaults(func=cmd_admission)
    p = sub.add_parser("scope-audit"); p.add_argument("--packet", required=True); p.add_argument("--files", required=True); p.set_defaults(func=cmd_scope)
    p = sub.add_parser("qualification"); p.add_argument("--scope-passed", action="store_true"); p.add_argument("--checks-passed", action="store_true"); p.add_argument("--human-acknowledged", action="store_true"); p.set_defaults(func=cmd_qualify)
    p = sub.add_parser("evidence"); p.add_argument("--database", default=".acp/evidence.sqlite3"); p.add_argument("--kind", required=True); p.add_argument("--file", required=True); p.set_defaults(func=cmd_evidence)
    p = sub.add_parser("ledger"); p.add_argument("--database", default=".acp/evidence.sqlite3"); p.set_defaults(func=cmd_ledger)
    p = sub.add_parser("init"); p.add_argument("directory", nargs="?", default="."); p.set_defaults(func=cmd_init)
    p = sub.add_parser("policy"); p.add_argument("--file", default=".acp/config.json"); p.set_defaults(func=cmd_policy)
    p = sub.add_parser("mode"); p.add_argument("--project-access", choices=("available", "rate_limited", "unauthorized", "not_found", "unavailable"), required=True); p.add_argument("--existing-lease", action="store_true"); p.add_argument("--lease-valid", action="store_true"); p.add_argument("--now", type=int); p.add_argument("--reset-at", type=int); p.set_defaults(func=cmd_mode)
    args = parser.parse_args()
    return args.func(args)

if __name__ == "__main__": sys.exit(main())
