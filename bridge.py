"""Authenticated local bridge for coordinator delivery acknowledgements."""
import hmac,json,os,secrets
from http.server import BaseHTTPRequestHandler,HTTPServer

class BridgeHandler(BaseHTTPRequestHandler):
    def authorized(self): return hmac.compare_digest(self.headers.get('Authorization',''), 'Bearer '+self.server.token)
    def do_GET(self):
        if self.path=='/health': self.send_response(200); self.end_headers(); self.wfile.write(b'{"status":"ok"}'); return
        if self.path=='/internal/status' and self.authorized(): self.send_response(200); self.end_headers(); self.wfile.write(b'{"status":"ready"}'); return
        self.send_error(401 if self.path.startswith('/internal/') else 404)
    def do_POST(self):
        if self.path!='/internal/ack' or not self.authorized(): self.send_error(401); return
        length=int(self.headers.get('Content-Length','0')); body=self.rfile.read(min(length,65536)); json.loads(body)
        self.send_response(204); self.end_headers()
    def log_message(self,*args): pass

def serve(host='127.0.0.1',port=8788,token=None):
    token=token or secrets.token_urlsafe(32); server=HTTPServer((host,port),BridgeHandler); server.token=token; print(f'bridge listening on {host}:{port}; token is configured externally'); server.serve_forever()

if __name__=='__main__': serve(token=os.environ['ACP_BRIDGE_TOKEN'])
