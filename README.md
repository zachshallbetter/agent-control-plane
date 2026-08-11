# Agent Control Plane

Provider-neutral admission, evidence, and qualification controls for autonomous software delivery.

ACP is the governance layer between a delivery request and an autonomous
implementation agent. It determines whether work is authorized, what evidence
it requires, and whether a human has reviewed the final delivery record.

The control plane enforces:

```text
issue packet → classification → claim/worktree → implementation → evidence → qualification → human approval → merge
```

Provider checks are target-aware and bounded. They never probe unrelated Projects, retry failed access, or mutate state after a provider failure. See [docs/RATE_LIMITS.md](docs/RATE_LIMITS.md).

## Why ACP exists

Autonomous agents commonly fail at coordination boundaries: wrong repository,
stale context, duplicate claims, expanded scope, incomplete deployment proof, or
Project status advanced without evidence. ACP turns those boundaries into typed,
versioned, fail-closed decisions.

## Decisions

| Decision | Meaning |
|---|---|
| `INVALID` | Repair issue or Project metadata. |
| `BLOCKED` | Resolve the named dependency, provider, credential, or evidence blocker. |
| `APPROVED` | Claim and implement within declared scope. |
| `REJECTED` | Stop for human review. |
| `QUALIFIED` | Scope, checks, evidence, and acknowledgement passed. |

`BLOCKED` is productive: the agent resolves only the named condition and
resubmits the same packet. Silence or a repeated “continue” is not approval.

GitHub is the first-class reference adapter. The reusable [GitHub adapter contract](docs/GITHUB_ADAPTER.md), [Projects skill](skills/github-projects/SKILL.md), and [coordinator agent definition](agents/coordinator.md) define how issues, Project items, dependencies, PRs, checks, and evidence become controlled delivery decisions.

InfiniteVerse is the reference integration, not a dependency.

## Architecture

```text
CLI / webhook receiver
        ↓
provider adapters → normalized facts → policy engine → evidence ledger
                                             ↓
                         admission / qualification verdict
```

The policy engine is provider-neutral. GitHub, GitLab, Linear, Jira, Railway,
Vercel, and local Git provide facts through adapters; they do not define ACP
decisions.

## Repository map

```text
schemas/    versioned normalized contracts
docs/       architecture, operations, security, adapters, evidence
scripts/    portable reference CLI commands
tests/      contract and decision fixtures
```

Runtime components also include `acp.py`, `coordinator.py`,
`webhook_receiver.py`, `adapters/`, `agents/`, and `skills/`.

## Status

The repository contains a tested operational MVP: typed decisions, SQLite
evidence persistence, signed webhook spooling, bounded coordinator leases,
provider contracts, skills, agent definitions, schemas, and reference tests.
Production adapter deployment still requires credentials, secret management,
network policy, and environment-specific configuration.

The implementation map in [docs/IMPLEMENTATION_MAP.md](docs/IMPLEMENTATION_MAP.md)
shows how the proven InfiniteVerse tooling maps into this independent project.

The signed webhook receiver and coordinator loop are reference implementations;
deploy them behind a private network boundary, with a secret manager and an
external process supervisor. The public repository never contains provider
credentials or product-specific deployment configuration.

## License

Apache-2.0. See [LICENSE](LICENSE).

## Verification

```bash
make test
make lint
```

## Drop-in installation

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
acp --help
acp init
```

ACP communicates through stable JSON decisions and does not require Claude,
OpenAI, Google, a specific IDE, or a specific agent runtime. See
[INTEROPERABILITY.md](docs/INTEROPERABILITY.md) and
[AGENT_PROTOCOL.md](docs/AGENT_PROTOCOL.md).

## Security rules

- Fail closed on unknown repositories, paths, dependencies, providers, and decisions.
- Verify webhook signatures, delivery IDs, payload limits, and idempotency.
- Never store private keys, tokens, cookies, raw prompts, or unredacted personal data in evidence.
- Use bounded timeouts, leases, refresh intervals, and retry budgets.
- Treat worker output as untrusted until validated against the issue packet.
- Require explicit human acknowledgement before merge or Project promotion.

## Roadmap

1. Complete the GitHub adapter using bounded ProjectsV2 snapshots and webhook invalidation.
2. Add Railway and Vercel adapters with deployment/browser evidence fixtures.
3. Add a supervised coordinator service with durable leases and a private bridge.
4. Add policy configuration and schema migration tooling.
5. Add a local evidence viewer and decision replay command.
6. Add additional providers without changing policy contracts.

## Setup and context

```bash
./scripts/setup.sh
python3 scripts/gen-context.py
CURRENT_CORPUS=.llms/llms-full.txt VERSIONED_CORPUS=.llms/llms-full.txt \
  MANIFEST_FILE=.llms/manifest.json scripts/context-check.sh
```

Setup asks which provider CLIs are needed, authenticates only selected
providers, writes a private local config, generates the context manifest, and
runs doctor. Context is generated from ACP sources; it is never copied from a
product repository.

The current provider modules are contract adapters with injected clients. They
intentionally do not contain credentials, implicit retries, or provider-specific
policy. Live clients and deployment wiring are the next integration boundary.
