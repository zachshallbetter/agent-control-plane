"""GitHub ProjectsV2 bootstrap/population plan builder."""
from dataclasses import dataclass

STANDARD_FIELDS=("Agent","Component","Priority","Size","Portfolio Milestone","Gate","Evidence State")

@dataclass(frozen=True)
class ProjectPlan:
    owner: str
    name: str
    repositories: tuple[str,...]
    fields: tuple[str,...] = STANDARD_FIELDS
    def operations(self):
        ops=[("create_project",{"owner":self.owner,"title":self.name})]
        ops += [("create_field",{"name":field}) for field in self.fields]
        ops += [("link_repository",{"repository":repo}) for repo in self.repositories]
        return ops
