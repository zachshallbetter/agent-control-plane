# Security Policy

## Reporting a vulnerability

Please report security issues privately rather than opening a public issue. Use GitHub private
vulnerability reporting:

**https://github.com/zachshallbetter/agent-control-plane/security/advisories/new**

Include a description of the issue and its impact, steps to reproduce (a minimal example is ideal),
and the affected path and version. Do not put credentials or exploit details in a public issue.

This is a solo-maintained project. Handling is best-effort with no SLA: there is no guaranteed
response or fix time.

## Scope

ACP is a policy engine, an evidence ledger, a signed-webhook receiver, a coordinator loop, provider
adapters and a gateway (`deployments/gateway/`). It fails closed by design, so reports about a path
that admits or qualifies work it should not, webhook signature, timestamp or idempotency checks,
payload limits, credential or personal data reaching the evidence ledger, and unsafe handling of
worker output are in scope. The engineering rules the project holds itself to are in
[`docs/SECURITY.md`](docs/SECURITY.md). Credentials and deployment configuration are never part of
this repository; a report should not include any.

## Supported versions

Only the latest release receives fixes. Fixes land on `main` and ship in the next release.
