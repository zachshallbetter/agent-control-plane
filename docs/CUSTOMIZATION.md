# Customization

ACP ships safe defaults but is designed to be customized per project through `.acp/config.json`.

```json
{
  "policy_version": "0.1.0",
  "statuses": {"ready": "Ready", "review": "In review", "done": "Done", "verified": "Verified"},
  "retry": {"max_attempts": 5, "base_seconds": 5, "max_seconds": 120},
  "snapshot_interval_seconds": 90,
  "require_human_acknowledgement": true,
  "providers": {
    "github": {"enabled": true, "owner": "example", "project": 1},
    "railway": {"enabled": true, "project": "project-id", "environment": "staging"},
    "vercel": {"enabled": true, "project": "frontend"}
  }
}
```

Customize provider targets, status labels, retry budgets, refresh intervals, and enabled adapters. Do not put credentials in this file. Environment variables or an external secret manager supply credentials.

Validate with:

```bash
acp policy --file .acp/config.json
```

Policy changes are versioned and should be reviewed like code. A project may add stricter rules but must not silently weaken human approval, scope, evidence, or provider-failure stop conditions.

The default review policy supports a declared single-maintainer mode. In that
mode, a second-pass human review is recorded as `self-approved`; it is distinct
from `independent-approved` and must include the same scope, check, and evidence
record. Enabling single-maintainer mode does not waive merge, deployment, or
runtime evidence gates.
