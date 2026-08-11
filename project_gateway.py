"""Cache-first Project read gateway with single-flight refreshes."""
from __future__ import annotations
import json, sqlite3, threading, time
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class GatewayResult:
    decision: str; owner: str; project: int; snapshot: dict | None; snapshot_source: str; snapshot_age_seconds: int | None; rate_limit: dict; next_probe_at: int | None; allowed: tuple[str, ...]; blocked: tuple[str, ...]

class ProjectGateway:
    def __init__(self, database: str, reader, ttl_seconds: int = 60):
        self.database=database; self.reader=reader; self.ttl_seconds=ttl_seconds; self.lock=threading.Lock(); Path(database).parent.mkdir(parents=True,exist_ok=True)
        with sqlite3.connect(database) as db: db.execute("CREATE TABLE IF NOT EXISTS project_snapshots (owner TEXT NOT NULL, project INTEGER NOT NULL, snapshot TEXT NOT NULL, checked_at INTEGER NOT NULL, quota TEXT NOT NULL, PRIMARY KEY(owner,project))")
    def _cached(self, owner, project):
        with sqlite3.connect(self.database) as db: return db.execute("SELECT snapshot,checked_at,quota FROM project_snapshots WHERE owner=? AND project=?",(owner,project)).fetchone()
    def context(self, owner: str, project: int, force: bool = False) -> GatewayResult:
        now=int(time.time()); row=self._cached(owner,project)
        if row and not force and now-row[1] < self.ttl_seconds: return self._result(owner,project,json.loads(row[0]),"cache",now-row[1],json.loads(row[2]),None)
        with self.lock:
            row=self._cached(owner,project); now=int(time.time())
            if row and not force and now-row[1] < self.ttl_seconds: return self._result(owner,project,json.loads(row[0]),"cache",now-row[1],json.loads(row[2]),None)
            try: snapshot, quota = self.reader(owner,project)
            except Exception as exc:
                if row:
                    quota={**json.loads(row[2]),"error":str(exc)[:240]}; return self._result(owner,project,json.loads(row[0]),"stale-cache",now-row[1],quota,quota.get("reset"))
                return self._result(owner,project,None,"unavailable",None,{"error":str(exc)[:240]},None)
            with sqlite3.connect(self.database) as db: db.execute("INSERT OR REPLACE INTO project_snapshots(owner,project,snapshot,checked_at,quota) VALUES(?,?,?,?,?)",(owner,project,json.dumps(snapshot,sort_keys=True),now,json.dumps(quota,sort_keys=True))); db.commit()
            return self._result(owner,project,snapshot,"provider",0,quota,None)
    @staticmethod
    def _result(owner,project,snapshot,source,age,quota,next_probe):
        degraded=quota.get("remaining",1)<=0 or source in ("stale-cache","unavailable")
        return GatewayResult("DEGRADED" if degraded else "AVAILABLE",owner,project,snapshot,source,age,quota,next_probe,("inspect","classify","prepare","queue","local-check") if degraded else ("inspect","classify","claim","worktree","mutate"),("claim","worktree","merge","project-mutation") if degraded else ())

def result_dict(result: GatewayResult) -> dict:
    return {"decision":result.decision,"project":result.project,"owner":result.owner,"snapshot":{"source":result.snapshot_source,"age_seconds":result.snapshot_age_seconds,"data":result.snapshot},"rate_limit":result.rate_limit,"next_probe_at":result.next_probe_at,"allowed":list(result.allowed),"blocked":list(result.blocked)}
