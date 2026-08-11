"""Durable, idempotent queue for work awaiting provider recovery."""
from __future__ import annotations
import sqlite3, time
from pathlib import Path

def open_queue(path: str) -> sqlite3.Connection:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path); db.execute("PRAGMA busy_timeout=5000")
    db.execute("CREATE TABLE IF NOT EXISTS queue (issue TEXT PRIMARY KEY, project TEXT NOT NULL, repository TEXT NOT NULL, reason TEXT NOT NULL, corpus_version TEXT NOT NULL, reset_at INTEGER, status TEXT NOT NULL DEFAULT 'queued', updated_at INTEGER NOT NULL)"); db.commit(); return db

def enqueue(path: str, *, issue: str, project: str, repository: str, reason: str, corpus_version: str, reset_at: int | None = None) -> None:
    db=open_queue(path); now=int(time.time())
    db.execute("INSERT INTO queue(issue,project,repository,reason,corpus_version,reset_at,status,updated_at) VALUES(?,?,?,?,?,?,?,?) ON CONFLICT(issue) DO UPDATE SET project=excluded.project,repository=excluded.repository,reason=excluded.reason,corpus_version=excluded.corpus_version,reset_at=excluded.reset_at,status='queued',updated_at=excluded.updated_at", (str(issue),project,repository,reason,corpus_version,reset_at,"queued",now)); db.commit(); db.close()

def due(path: str, now: int | None = None) -> list[dict]:
    db=open_queue(path); now=int(time.time()) if now is None else now
    rows=db.execute("SELECT issue,project,repository,reason,corpus_version,reset_at,status,updated_at FROM queue WHERE status='queued' AND (reset_at IS NULL OR reset_at<=?) ORDER BY COALESCE(reset_at,0),issue", (now,)).fetchall(); db.close()
    keys=("issue","project","repository","reason","corpus_version","reset_at","status","updated_at")
    return [dict(zip(keys,row)) for row in rows]
