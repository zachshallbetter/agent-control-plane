# Portable gateway deployment

The ACP gateway is independently deployable from `deployments/gateway`. It is
provider infrastructure, not InfiniteVerse product code. Configure these
Railway secrets on the ACP-owned service:

```text
ACP_GATEWAY_TOKEN
ACP_GITHUB_APP_ID
ACP_GITHUB_INSTALLATION_ID
ACP_GITHUB_PRIVATE_KEY
```

The authenticated App probe returns only token expiry and permissions metadata;
it never returns the installation token or private key.

## Local agent handoff

`ACP_GATEWAY_TOKEN` belongs in the deployment secret store. Setup may inject it
into a child agent process, but must never commit it, write it into the
repository, include it in generated context, or print it. Record gateway
health, local credential presence, App-token probing, and fresh Project-context
verification as separate states. `LOCAL_GATEWAY_CREDENTIAL_MISSING` is a setup
blocker, not a GitHub `NOT_FOUND` result. Only the authenticated bounded
Project-context result clears the Project authority gate.
