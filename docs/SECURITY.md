# Security

- Never store private keys, provider tokens, cookies, or raw prompts in the ledger.
- Verify webhook signatures, timestamps, payload size, and idempotency keys.
- Redact credentials and personal data by default.
- Default to deny for unknown repositories, paths, providers, and decisions.
- Use bounded timeouts and typed retryable/fatal errors.
- Treat worker output as untrusted input; validate structured verdicts before mutation.
- Human acknowledgement is required for merge and status promotion.

Report vulnerabilities privately through GitHub Security Advisories; do not publish credentials or exploit details in issues.
