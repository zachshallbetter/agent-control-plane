from dataclasses import dataclass
from typing import Protocol, Any

class GitHubClient(Protocol):
    def read(self, resource: str, query: dict) -> Any: ...
    def write(self, resource: str, payload: dict) -> Any: ...

@dataclass
class GitHubProvider:
    client: GitHubClient
    def issue(self, repository: str, number: int): return self.client.read("issue", {"repository": repository, "number": number})
    def project_item(self, owner: str, project: int, item: str): return self.client.read("project_item", {"owner": owner, "project": project, "item": item})
    def pull_request(self, repository: str, number: int): return self.client.read("pull_request", {"repository": repository, "number": number})
    def webhook_event(self, delivery: str): return self.client.read("webhook_delivery", {"delivery": delivery})
