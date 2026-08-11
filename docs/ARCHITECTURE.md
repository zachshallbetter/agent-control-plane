# Architecture

Agent Control Plane (ACP) is a provider-neutral control plane for autonomous software delivery.

```text
CLI / webhook receiver
        ↓
provider adapters → normalized facts → policy engine → decision ledger
                                             ↓
                         admission / qualification verdict
```

## Boundaries

| Layer | Owns | Does not own |
|---|---|---|
| CLI | local commands, config, output | provider policy authority |
| Coordinator | scheduling, lifecycle, bounded retries | product implementation |
| Policy engine | scope, dependency, evidence, approval decisions | credentials or deployments |
| Provider adapters | GitHub, GitLab, Railway, Vercel, Git facts | cross-provider business rules |
| Evidence ledger | immutable decision/evidence records | source code or issue content |
| Workers | changes inside an approved worktree | ownership, scope, merge authority |

Providers are replaceable adapters. The policy engine consumes normalized facts and produces typed decisions; it never parses a provider's UI or infers authorization from prose.

## Lifecycle

```text
Ticket → Admission → Claim → Worktree → Implementation → Evidence
      → Scope audit → Qualification → Human acknowledgement → Merge/status
```

Each transition is idempotent, recorded, and fail-closed.
