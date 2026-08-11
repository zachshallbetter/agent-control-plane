#!/usr/bin/env python3
import json, subprocess, tempfile
from pathlib import Path

root = Path(__file__).parents[1]
with tempfile.TemporaryDirectory() as directory:
    base = Path(directory); packet = base / "packet.json"; files = base / "files"; db = base / "evidence.sqlite3"; evidence = base / "evidence.json"
    packet.write_text(json.dumps({"issue": 1, "project_item": "PVTI_test", "repository": "org/repo", "authorized_paths": ["src"], "exclusions": ["private"], "dependencies": [], "acceptance_criteria": ["x"], "evidence_requirements": ["y"], "definition_of_done": ["z"], "status": "Ready"}))
    files.write_text("src/main.py\n"); evidence.write_text(json.dumps({"kind": "test", "subject": "fixture", "observed_at": "2026-01-01T00:00:00Z", "result": "pass"}))
    def run(*args): return subprocess.run(["python3", str(root / "acp.py"), *args], text=True, capture_output=True)
    assert json.loads(run("admission", "--packet", str(packet)).stdout)["decision"] == "APPROVED"
    assert json.loads(run("scope-audit", "--packet", str(packet), "--files", str(files)).stdout)["decision"] == "APPROVED"
    assert json.loads(run("evidence", "--database", str(db), "--kind", "test", "--file", str(evidence)).stdout)["evidence_id"]
    assert "test" in run("ledger", "--database", str(db)).stdout
print("python CLI tests passed")
