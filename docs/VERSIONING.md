# Versioning

ACP uses Semantic Versioning for the policy and normalized contracts.

- **Major**: incompatible decision, evidence, or adapter contract.
- **Minor**: backward-compatible policy or adapter capability.
- **Patch**: bug fixes and documentation corrections.

Every decision records the policy version. A stale policy or corpus is a hard stop when it changes scope, identity, routing, evidence, or status semantics.

`scripts/gen-context.py` generates the local `.llms/` projection and
`manifest.json`. The manifest binds every source path to a SHA-256 digest and
records the policy version plus generated corpus digests. `.llms/` is generated
state, never hand-edited. Run the generator after source, schema, skill, or
agent-definition changes and reject stale manifests before admission.
