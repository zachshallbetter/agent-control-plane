from dataclasses import dataclass
from typing import Protocol, Any

class VercelClient(Protocol):
    def read(self, resource: str, query: dict) -> Any: ...

@dataclass
class VercelProvider:
    client: VercelClient
    def deployment(self, project: str, deployment: str): return self.client.read("deployment", {"project": project, "deployment": deployment})
    def browser_evidence(self, url: str, checks: list[str]): return self.client.read("browser_evidence", {"url": url, "checks": checks})
