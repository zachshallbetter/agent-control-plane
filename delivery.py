"""Durable webhook delivery spool with idempotency and bounded retry states."""
import json,sqlite3,time
from pathlib import Path

class DeliverySpool:
    def __init__(self,path='.acp/deliveries.sqlite3'):
        Path(path).parent.mkdir(parents=True,exist_ok=True); self.db=sqlite3.connect(path); self.db.execute('PRAGMA busy_timeout=5000'); self.db.execute('''CREATE TABLE IF NOT EXISTS deliveries(id TEXT PRIMARY KEY,event TEXT NOT NULL,payload TEXT NOT NULL,received_at INTEGER NOT NULL,status TEXT NOT NULL DEFAULT 'queued',attempts INTEGER NOT NULL DEFAULT 0,last_error TEXT)'''); self.db.commit()
    def enqueue(self,ident,event,payload):
        try: self.db.execute('INSERT INTO deliveries(id,event,payload,received_at) VALUES(?,?,?,?)',(ident,event,json.dumps(payload,sort_keys=True,separators=(',',':')),int(time.time()))); self.db.commit(); return True
        except sqlite3.IntegrityError: self.db.rollback(); return False
    def claim(self,limit=1):
        rows=self.db.execute("SELECT id,event,payload,attempts FROM deliveries WHERE status='queued' ORDER BY received_at,id LIMIT ?",(limit,)).fetchall(); out=[]
        for ident,event,payload,attempts in rows:
            if self.db.execute("UPDATE deliveries SET status='processing',attempts=attempts+1 WHERE id=? AND status='queued'",(ident,)).rowcount: out.append({'id':ident,'event':event,'payload':json.loads(payload),'attempt':attempts+1})
        self.db.commit(); return out
    def finish(self,ident,success,error='',max_attempts=3):
        row=self.db.execute('SELECT attempts FROM deliveries WHERE id=?',(ident,)).fetchone(); attempts=row[0] if row else max_attempts
        status='succeeded' if success else ('queued' if attempts < max_attempts else 'failed')
        self.db.execute('UPDATE deliveries SET status=?,last_error=? WHERE id=?',(status,error[:500],ident)); self.db.commit(); return status
