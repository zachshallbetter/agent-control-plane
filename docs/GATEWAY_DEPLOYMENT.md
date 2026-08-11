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
