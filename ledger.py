"""Durable SQLite claims, attempts, and evidence primitives."""
import sqlite3,time
from pathlib import Path

class Ledger:
    def __init__(self,path='.acp/evidence.sqlite3'):
        Path(path).parent.mkdir(parents=True,exist_ok=True); self.db=sqlite3.connect(path); self.db.execute('PRAGMA busy_timeout=5000'); self.db.executescript('''CREATE TABLE IF NOT EXISTS claims(issue TEXT PRIMARY KEY, actor TEXT NOT NULL, lease_until INTEGER NOT NULL); CREATE TABLE IF NOT EXISTS attempts(issue TEXT NOT NULL, attempt INTEGER NOT NULL, started_at INTEGER NOT NULL, outcome TEXT, PRIMARY KEY(issue,attempt));'''); self.db.commit()
    def claim(self,issue,actor,seconds=1800):
        now=int(time.time()); row=self.db.execute('SELECT actor,lease_until FROM claims WHERE issue=?',(str(issue),)).fetchone()
        if row and row[1]>now and row[0]!=actor: return False
        self.db.execute('INSERT OR REPLACE INTO claims VALUES(?,?,?)',(str(issue),actor,now+seconds)); self.db.commit(); return True
    def release(self,issue): self.db.execute('DELETE FROM claims WHERE issue=?',(str(issue),)); self.db.commit()
    def attempt(self,issue,outcome=None):
        row=self.db.execute('SELECT COALESCE(MAX(attempt),0)+1 FROM attempts WHERE issue=?',(str(issue),)).fetchone(); n=row[0]; self.db.execute('INSERT INTO attempts VALUES(?,?,?,?)',(str(issue),n,int(time.time()),outcome)); self.db.commit(); return n
