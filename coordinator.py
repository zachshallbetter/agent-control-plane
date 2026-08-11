"""Bounded coordinator loop. Scheduling is injected so policy remains provider-neutral."""
from dataclasses import dataclass
from time import monotonic
from retry import RetryPolicy

@dataclass
class Lease:
    issue: str
    actor: str
    expires_at: float

class Coordinator:
    def __init__(self, classify, execute, lease_seconds=1800, retry_policy=None):
        self.classify=classify; self.execute=execute; self.lease_seconds=lease_seconds; self.leases={}; self.retry_policy=retry_policy or RetryPolicy(); self.attempts={}
    def cycle(self, packets):
        results=[]
        for packet in packets:
            issue=str(packet.get("issue")); decision=self.classify(packet)
            if decision.get("decision") != "APPROVED": results.append(decision); continue
            if issue in self.leases and self.leases[issue].expires_at > monotonic(): continue
            self.leases[issue]=Lease(issue,packet.get("actor","coordinator"),monotonic()+self.lease_seconds)
            attempt=self.attempts.get(issue,0)+1; self.attempts[issue]=attempt
            try: result=self.execute(packet, attempt)
            except Exception as exc: result={"decision":"BLOCKED","issue":issue,"reason":str(exc)[:240],"attempt":attempt,"retryable":False}
            if result.get("decision") == "QUALIFIED": self.release(issue)
            results.append(result)
        return results
    def release(self, issue): self.leases.pop(str(issue),None)
