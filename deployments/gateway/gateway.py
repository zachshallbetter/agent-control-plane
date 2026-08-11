#!/usr/bin/env python3
"""Portable ACP gateway: isolated health and GitHub App probe."""
from __future__ import annotations
import base64, hmac, http.server, json, os, subprocess, tempfile, time
from urllib.request import Request, urlopen

def configured(): return all(os.getenv(k) for k in ("ACP_GITHUB_APP_ID","ACP_GITHUB_INSTALLATION_ID","ACP_GITHUB_PRIVATE_KEY"))
def authorized(handler):
    token=os.getenv("ACP_GATEWAY_TOKEN",""); return bool(token) and hmac.compare_digest(handler.headers.get("Authorization",""),"Bearer "+token)
def installation_token():
    now=int(time.time()); enc=lambda b: base64.urlsafe_b64encode(b).rstrip(b"=").decode(); header=enc(b'{"alg":"RS256","typ":"JWT"}'); payload=enc(json.dumps({"iat":now-60,"exp":now+540,"iss":os.environ["ACP_GITHUB_APP_ID"]},separators=(",",":")).encode()); signing=f"{header}.{payload}".encode()
    with tempfile.NamedTemporaryFile(mode="w",prefix="acp-key-",delete=False) as key:
        os.chmod(key.name,0o600); key.write(os.environ["ACP_GITHUB_PRIVATE_KEY"]); key.flush(); path=key.name
    try: sig=subprocess.run(["openssl","dgst","-sha256","-sign",path],input=signing,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout
    finally: os.unlink(path)
    req=Request(f"https://api.github.com/app/installations/{os.environ['ACP_GITHUB_INSTALLATION_ID']}/access_tokens",method="POST",headers={"Authorization":"Bearer "+signing.decode()+"."+enc(sig),"Accept":"application/vnd.github+json","User-Agent":"acp-gateway"})
    with urlopen(req,timeout=10) as response: return json.load(response)
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=="/health": self.reply(200,{"status":"ok","service":"acp-gateway","app_configured":configured()}); return
        if self.path=="/internal/app-status" and authorized(self): self.reply(200,{"configured":configured(),"installation_id":os.getenv("ACP_GITHUB_INSTALLATION_ID") if configured() else None,"token_minting":"internal-only"}); return
        if self.path=="/internal/app-probe" and authorized(self):
            if not configured(): self.reply(503,{"configured":False}); return
            try:
                token=installation_token(); self.reply(200,{"configured":True,"installation_token":"minted","token_expires_at":token.get("expires_at"),"permissions":token.get("permissions",{})})
            except Exception as exc: self.reply(502,{"configured":True,"installation_token":"failed","error":str(exc)[:240]})
            return
        self.send_error(401 if self.path.startswith("/internal/") else 404)
    def reply(self,code,body):
        data=json.dumps(body,separators=(",",":"),sort_keys=True).encode(); self.send_response(code); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(data))); self.end_headers(); self.wfile.write(data)
    def log_message(self,*_): pass
def main():
    if not os.getenv("ACP_GATEWAY_TOKEN"): raise SystemExit("ACP_GATEWAY_TOKEN is required")
    http.server.ThreadingHTTPServer(("0.0.0.0",int(os.getenv("PORT","8080"))),Handler).serve_forever()
if __name__=="__main__": main()
