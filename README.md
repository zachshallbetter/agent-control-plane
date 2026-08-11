# Agent Control Plane

Bounded admission, evidence, and qualification controls for autonomous software delivery.

The control plane enforces:

```text
issue packet → classification → claim/worktree → implementation → evidence → qualification → human approval → merge
```

Provider checks are target-aware and bounded. They never probe unrelated Projects, retry failed access, or mutate state after a provider failure. See [docs/RATE_LIMITS.md](docs/RATE_LIMITS.md).

InfiniteVerse is the reference integration, not a dependency.
