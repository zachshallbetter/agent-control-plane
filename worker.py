"""Worker lifecycle boundary. Runtime-specific agents implement the callback."""
from dataclasses import dataclass
from ledger import Ledger
from retry import RetryPolicy

@dataclass
class WorkerResult:
    decision: str
    reason: str
    attempt: int

class WorkerRunner:
    def __init__(self,ledger=None,policy=None): self.ledger=ledger or Ledger(); self.policy=policy or RetryPolicy()
    def run(self,packet,actor,worker):
        issue=str(packet['issue']); self.ledger.claim(issue,actor); attempt=self.ledger.attempt(issue)
        try: result=worker(packet,attempt)
        except Exception as exc: result={'decision':'BLOCKED','reason':str(exc)[:240], 'retryable':False}
        self.ledger.db.execute('UPDATE attempts SET outcome=? WHERE issue=? AND attempt=?',(result.get('decision'),issue,attempt)); self.ledger.db.commit()
        if result.get('decision') in ('QUALIFIED','REJECTED'): self.ledger.release(issue)
        return WorkerResult(result.get('decision','BLOCKED'),result.get('reason',''),attempt)
