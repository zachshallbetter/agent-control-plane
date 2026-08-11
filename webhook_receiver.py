#!/usr/bin/env python3
"""Small signed, idempotent webhook spool for adapter-driven coordinators."""
import hashlib,hmac,http.server,json,os,sqlite3,time
from pathlib import Path
MAX_BYTES=1_048_576

def verify(secret: bytes, body: bytes, signature: str) -> bool:
    if not signature.startswith("sha256="): return False
    expected="sha256="+hmac.new(secret,body,hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected,signature)

class Receiver(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/webhooks/github": self.send_error(404); return
        try: size=int(self.headers.get("Content-Length","-1"))
        except ValueError: size=-1
        body=self.rfile.read(size) if 0 <= size <= MAX_BYTES else b""
        if not body or not verify(self.server.secret,body,self.headers.get("X-Hub-Signature-256","")):
            self.send_error(401); return
        delivery=self.headers.get("X-GitHub-Delivery",""); event=self.headers.get("X-GitHub-Event","")
        if not delivery or not event: self.send_error(400); return
        try: payload=json.loads(body)
        except json.JSONDecodeError: self.send_error(400); return
        try:
            self.server.db.execute("INSERT INTO deliveries(id,event,received_at,payload) VALUES(?,?,?,?)",(delivery,event,int(time.time()),json.dumps(payload,sort_keys=True,separators=(",",":")))); self.server.db.commit(); duplicate=False
        except sqlite3.IntegrityError: self.server.db.rollback(); duplicate=True
        result=json.dumps({"accepted":True,"duplicate":duplicate}).encode(); self.send_response(202); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(result))); self.end_headers(); self.wfile.write(result)
    def log_message(self,*args): pass

def serve(database: str, secret: str, host: str="127.0.0.1", port: int=8787):
    Path(database).parent.mkdir(parents=True,exist_ok=True); db=sqlite3.connect(database,check_same_thread=False); db.execute("CREATE TABLE IF NOT EXISTS deliveries(id TEXT PRIMARY KEY,event TEXT NOT NULL,received_at INTEGER NOT NULL,payload TEXT NOT NULL)"); db.commit()
    server=http.server.ThreadingHTTPServer((host,port),Receiver); server.db=db; server.secret=secret.encode(); server.serve_forever()

if __name__ == "__main__": serve(os.getenv("ACP_WEBHOOK_DB",".acp/webhooks.sqlite3"),os.environ["ACP_WEBHOOK_SECRET"])
