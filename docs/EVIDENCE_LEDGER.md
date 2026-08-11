# Evidence ledger

The ledger records why a lifecycle decision was made. It is append-only at the logical level; corrections create a new record that references the prior decision.

Every record includes:

```text
decision_id, issue, project_item, repository, branch, worktree,
policy_version, corpus_version, actor, timestamp,
inputs, checks, deployments, browser/API observations,
blockers, human_acknowledgement, decision
```

Evidence tiers are distinct:

```text
Documented ≠ Implemented ≠ Tested ≠ Deployed ≠ Browser-verified
```

No lower tier may satisfy a higher-tier requirement. Credentials and private payloads are referenced by identifier, never copied into the ledger.
