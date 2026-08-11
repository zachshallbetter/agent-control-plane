# Provider adapters

Adapters translate external systems into stable ACP facts.

## Required adapter interface

```text
authenticate() → AuthFact
read_ticket(id) → TicketFact
read_project_item(id) → ProjectFact
read_dependencies(id) → DependencyFact[]
read_repository(repo) → RepositoryFact
read_change(change) → ChangeFact
read_checks(change) → CheckFact[]
read_deployment(id) → DeploymentFact
record_comment(target, body) → EvidenceRef
```

Adapters must be bounded, observable, and idempotent. They must expose provider errors as typed facts rather than retrying internally.

## Initial adapters

- GitHub Issues/Projects/PRs and webhooks.
- Local Git repositories and worktrees.
- Railway deployments and runtime health.
- Vercel deployments and browser checks.

GitLab, Linear, Jira, and self-hosted runners are future adapters, not dependencies of the core policy engine.
