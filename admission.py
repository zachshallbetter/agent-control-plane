"""Provider-neutral admission decisions; adapters supply project-specific facts."""
from __future__ import annotations

def decide(data: dict, *, topology_ok: bool = True, corpus_fresh: bool = True, provider_available: bool = True) -> tuple[str, str, dict]:
    required=("issue","project_item","repository","authorized_paths","exclusions","dependencies","acceptance_criteria","evidence_requirements","definition_of_done")
    missing=[key for key in required if key not in data or (key not in ("exclusions","dependencies") and not data[key])]
    if missing: return "INVALID", "missing required packet fields: " + ", ".join(missing), {}
    if not provider_available: return "BLOCKED", "project provider unavailable; queue or prepare only", {"issue":data["issue"]}
    if not topology_ok: return "BLOCKED", "repository or submodule topology is not verified", {"issue":data["issue"],"repository":data["repository"]}
    if not corpus_fresh: return "BLOCKED", "versioned context corpus is stale", {"issue":data["issue"]}
    if data.get("status") != "Ready": return "BLOCKED", "Project item is not Ready", {"issue":data["issue"]}
    if data.get("unresolved_dependencies"): return "BLOCKED", "declared dependency is unresolved", {"issue":data["issue"],"blockers":data["unresolved_dependencies"]}
    return "APPROVED", "issue packet and supplied authority facts are actionable", {"issue":data["issue"],"project_item":data["project_item"],"repository":data["repository"]}
