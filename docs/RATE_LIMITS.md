# Provider access and rate limits

Provider checks are target-aware and bounded. A doctor run performs at most one read for the selected Project. It never probes a default or unrelated Project, retries a failed provider request, or mutates state after an access failure.

Use `--owner` and `--project`, or set `GH_PROJECT_OWNER` and `GH_PROJECT_NUMBER`. A rate-limit or authorization failure is a `BLOCKED` provider condition; resume after access recovers.

## Degraded operation

A Project outage does not make the whole agent unavailable. ACP enters `degraded` mode for rate-limited or temporarily unavailable Project access. Agents may inspect issues, classify dependencies, prepare plans, run local checks, and queue work. New claims, branches, worktrees, implementation, qualification, deployment, and provider mutations remain blocked because they require fresh authority. An agent with an unexpired claim lease may enter `continuation` mode and finish reversible implementation, checks, and evidence, but may not renew the lease or perform authority mutations.

`unauthorized` and `not_found` are `paused`, not degraded: these require correction rather than waiting. A reset timestamp is a scheduling hint, never authorization; recovery always requires one bounded fresh Project read.

Use `acp queue-add` to persist a blocked candidate with its project, repository,
blocker, corpus version, and reset time. `acp queue-due` returns candidates
eligible for one recovery probe; it does not claim or mutate them. Queue records
are idempotent by issue number.

The canonical quota probe is `scripts/rate-limit.sh`. It caches quota metadata
for 30 seconds by default, reports UTC and local reset times, and must run before
any GraphQL-backed Project snapshot or mutation. Set `ACP_RATE_LIMIT_CACHE` and
`ACP_RATE_LIMIT_MIN_INTERVAL` to customize the cache path and interval. Cached
quota data prevents request storms but never authorizes work after a reset; a
fresh Project read is still required.
