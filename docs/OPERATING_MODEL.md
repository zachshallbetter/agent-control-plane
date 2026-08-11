# Operating model

An issue packet is the authorization boundary. It must declare:

- issue and Project identity;
- owning repository and component;
- authorized paths and exclusions;
- dependencies and their completion state;
- acceptance criteria;
- evidence requirements; and
- definition of done.

ACP admission is the reusable policy decision over that packet and supplied
provider, topology, and corpus facts. Project integrations remain responsible
for final local enforcement before claims, worktrees, merges, or mutations.

## Decisions

| Decision | Meaning | Agent action |
|---|---|---|
| `INVALID` | Packet or identity is incomplete | Repair metadata and resubmit |
| `BLOCKED` | A declared dependency, credential, or provider condition is unresolved | Resolve only the named blocker and resubmit |
| `APPROVED` | Work is authorized | Claim, create worktree, and implement |
| `REJECTED` | Scope, policy, or safety violation | Stop for human review |
| `QUALIFIED` | Evidence and review gates passed | Human may merge or promote status |

Silence, a repeated “continue,” a green local test, or a browser session is not approval. A human must read and acknowledge the final delivery record.

## Invariants

1. One issue, one claim, one worktree, one PR.
2. Workers never select their own repository or scope.
3. Findings outside scope become linked work.
4. Provider failures stop authority-dependent work; retry budgets are explicit.
5. Rate limits use degraded mode so agents can prepare and queue work without creating untracked implementation.
5. Direct pushes to protected branches are unqualified.
