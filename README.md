# Agent Control Plane

Bounded admission, evidence, and qualification controls for autonomous software delivery.

The control plane enforces:

```text
issue packet → classification → claim/worktree → implementation → evidence → qualification → human approval → merge
```

Provider checks are target-aware and bounded. They never probe unrelated Projects, retry failed access, or mutate state after a provider failure. See [docs/RATE_LIMITS.md](docs/RATE_LIMITS.md).

GitHub is the first-class reference adapter. The reusable [GitHub adapter contract](docs/GITHUB_ADAPTER.md), [Projects skill](skills/github-projects/SKILL.md), and [coordinator agent definition](agents/coordinator.md) define how issues, Project items, dependencies, PRs, checks, and evidence become controlled delivery decisions.

InfiniteVerse is the reference integration, not a dependency.

## Repository map

```text
schemas/    versioned normalized contracts
docs/       architecture, operations, security, adapters, evidence
scripts/    portable reference CLI commands
tests/      contract and decision fixtures
```

## Status

The repository contains the first portable decision primitives and reference
shell CLI. The coordinator daemon, webhook receiver, persistent ledger, and
provider adapters are staged behind the contracts above.

The implementation map in [docs/IMPLEMENTATION_MAP.md](docs/IMPLEMENTATION_MAP.md)
shows how the proven InfiniteVerse tooling maps into this independent project.

## License

Apache-2.0. See [LICENSE](LICENSE).
