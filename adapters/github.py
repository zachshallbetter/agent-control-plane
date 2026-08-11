"""GitHub adapter boundary. Provider calls are deliberately injected, bounded, and testable."""
from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class GitHubFacts:
    issue: dict
    project_item: dict
    pull_request: dict | None = None

class GitHubAdapter:
    def __init__(self, read: Callable[[str, dict], Any], write: Callable[[str, dict], Any] | None = None):
        self.read = read; self.write = write
    def issue_packet(self, repository: str, issue: int) -> dict:
        return self.read("issue", {"repository": repository, "issue": issue})
    def project_item(self, owner: str, project: int, item: str) -> dict:
        return self.read("project_item", {"owner": owner, "project": project, "item": item})
    def pull_request(self, repository: str, number: int) -> dict:
        return self.read("pull_request", {"repository": repository, "number": number})
    def record(self, target: str, body: str) -> Any:
        if self.write is None: raise RuntimeError("GitHub adapter is read-only")
        return self.write(target, {"body": body})
