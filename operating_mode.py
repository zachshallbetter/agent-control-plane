"""Provider-aware operating modes for autonomous delivery."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class OperatingMode:
    name: str
    allowed: tuple[str, ...]
    blocked: tuple[str, ...]
    reason: str

def evaluate(*, project_access: str, existing_lease: bool = False, lease_valid: bool = False,
             now: int | None = None, reset_at: int | None = None) -> OperatingMode:
    if project_access == "available":
        return OperatingMode("normal", ("classify", "claim", "branch", "worktree", "implement", "check", "evidence", "qualify", "mutate"), (), "Project access is available")
    if existing_lease and lease_valid:
        return OperatingMode("continuation", ("classify", "inspect", "implement", "check", "evidence"), ("claim", "branch", "worktree", "qualify", "mutate"), "existing valid lease may continue; authority mutations remain paused")
    if project_access in {"rate_limited", "unavailable"}:
        suffix = f"; recovery probe after {reset_at}" if reset_at and now is not None and reset_at > now else ""
        return OperatingMode("degraded", ("classify", "inspect", "prepare", "queue", "local-check"), ("claim", "branch", "worktree", "implement", "qualify", "mutate", "deploy"), "Project authority unavailable; safe preparation only" + suffix)
    return OperatingMode("paused", ("inspect", "record-blocker"), ("classify", "prepare", "queue", "claim", "branch", "worktree", "implement", "qualify", "mutate", "deploy"), "Project authority is not authorized or does not exist")

def as_dict(mode: OperatingMode) -> dict:
    return {"mode": mode.name, "allowed": list(mode.allowed), "blocked": list(mode.blocked), "reason": mode.reason}
