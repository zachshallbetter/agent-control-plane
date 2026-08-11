# Implementation map

| InfiniteVerse implementation | ACP home |
|---|---|
| `doctor.sh` | `scripts/doctor.sh` |
| `coordinator-admission.sh` | `scripts/admission.sh` / `acp.py admission` |
| `coordinator-finalize.sh` | `acp.py qualification` |
| `agent-start.sh` | `scripts/agent-start.sh` |
| board snapshot | `scripts/snapshot.sh` |
| PR scope audit | `acp.py scope-audit` |
| evidence audit | `scripts/audit-evidence.sh` / `acp.py ledger` |
| worktree cleanup | `scripts/cleanup.sh` |
| coordinator bridge | `scripts/coordinator-bridge.sh` |
| signed webhook receiver | `webhook_receiver.py` |
| coordinator loop and leases | `coordinator.py` |
| repository safety | `scripts/repository-check.sh` |
| context freshness | `scripts/context-check.sh` |
| agent roles | `agents/` |
| reusable skills | `skills/` |
| version/corpus rules | `docs/VERSIONING.md` and adapter configuration |

The map is intentionally a boundary document, not a copy of product-repository implementation.
