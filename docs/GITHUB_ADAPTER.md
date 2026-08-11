# GitHub adapter

GitHub is the first production adapter because it provides the issue, ProjectV2, pull request, review, webhook, and repository primitives required by the ACP lifecycle.

## Mapping

| ACP concept | GitHub source |
|---|---|
| Ticket | Issue |
| Work queue | ProjectsV2 item and Status field |
| Ownership | Project Agent field, assignee, repository metadata |
| Dependency | Native blocked-by/blocking relationships |
| Change | Branch, worktree, pull request, commit |
| Checks | Local/provider-native checks and PR status contexts |
| Approval | Review plus explicit delivery-record acknowledgement |
| Evidence | Issue/PR comments, check output, deployment URLs, ledger record |

## Rules

- The issue number is the durable join key across branch, commit, PR, comments, evidence, and Project item.
- Use native Project items; drafts are not implementation authorization.
- Read Project state from a cached snapshot and refresh only at bounded coordinator-cycle boundaries.
- Use webhooks to invalidate or queue a refresh, not to trigger an unbounded API loop.
- Never infer repository ownership from a title or prompt; resolve and verify the remote.
- Provider rate limits and missing scopes produce `BLOCKED`, never retries or partial mutation.
