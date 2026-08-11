import sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
from project_gateway import ProjectGateway
calls=[]
def reader(owner, project):
    calls.append((owner,project)); return ({"items":[{"number":286}]},{"limit":5000,"remaining":4999,"reset":200})
with tempfile.TemporaryDirectory() as d:
    g=ProjectGateway(str(Path(d)/"gateway.sqlite3"),reader,ttl_seconds=60)
    first=g.context("Anime-Universe",3); second=g.context("Anime-Universe",3)
    assert first.decision=="AVAILABLE" and second.snapshot_source=="cache" and len(calls)==1
    def blocked(owner, project): raise RuntimeError("graphql quota exhausted")
    g.reader=blocked; stale=g.context("Anime-Universe",3,force=True)
    assert stale.decision=="DEGRADED" and stale.snapshot_source=="stale-cache"
print("gateway tests passed")
