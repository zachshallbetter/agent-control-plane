# Agent interoperability

ACP does not depend on a model vendor, editor, or agent runtime. Any worker that can read JSON, execute a command, and return a structured delivery record can participate.

## Worker boundary

Workers receive a packet containing issue identity, repository, worktree, authorized paths, exclusions, acceptance criteria, evidence requirements, policy version, and stop conditions. They return JSON with `decision`, `checks`, `evidence_refs`, `blockers`, and `next_action`.

The worker never owns admission, repository selection, merge, or Project status. Those remain coordinator operations.

## Supported host patterns

- Claude Code or another terminal agent: invoke `acp` from the worktree.
- OpenAI/Codex agent: call the CLI or adapter through a shell tool.
- Google/Gemini agent: use the same JSON packet and command boundary.
- IDE agents: expose `acp` as a task, run configuration, or MCP/tool wrapper.
- CI or self-hosted workers: use `--dry-run` and provider-scoped credentials.

Do not encode vendor-specific prompts in the policy engine. Vendor prompts belong in role adapters under `agents/`.
