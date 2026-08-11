import sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
from queue import enqueue, due
with tempfile.TemporaryDirectory() as d:
    db=str(Path(d)/"queue.sqlite3")
    enqueue(db, issue="286", project="3", repository="org/services", reason="graphql rate limit", corpus_version="v1", reset_at=200)
    enqueue(db, issue="286", project="3", repository="org/services", reason="graphql rate limit", corpus_version="v1", reset_at=200)
    assert due(db, 100) == []
    assert due(db, 200)[0]["issue"] == "286"
print("queue tests passed")
