from dataclasses import dataclass
from typing import Protocol, Any

class RailwayClient(Protocol):
    def read(self, resource: str, query: dict) -> Any: ...

@dataclass
class RailwayProvider:
    client: RailwayClient
    def deployment(self, project: str, service: str, deployment: str): return self.client.read("deployment", {"project": project, "service": service, "deployment": deployment})
    def health(self, url: str): return self.client.read("health", {"url": url})
