# Contributing

1. Start from a real issue describing scope, exclusions, acceptance, and evidence.
2. Use an issue-numbered branch: `<type>/<issue>-<slug>`.
3. Keep changes within the issue-defined paths.
4. Run `make test` and `make lint` (`make lint` runs `git diff --check` and `bash -n scripts/*.sh`).
5. Include the issue number, checks, evidence, and blockers in the PR.
6. Do not add provider-specific behavior to the policy engine.
7. A maintainer must read and acknowledge the delivery record before merge.

Prefer small, reversible changes. New adapters require contract fixtures and rate-limit behavior tests.

## Setup

ACP needs Python 3.11 or later.

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
acp --help
```

`make test` runs the shell syntax check, the decision, CLI and runtime tests, and byte-compiles the modules.

## Conventions

- Commit subjects use a conventional prefix such as `feat:`, `fix:`, `chore:` or `docs:`, as the history does.
- Record notable changes under `## Unreleased` in [`CHANGELOG.md`](CHANGELOG.md).
- Fill in the pull request template: what and why, how it was verified, and notes.

## Conduct, support and security

See [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md), [`SUPPORT.md`](SUPPORT.md) and [`SECURITY.md`](SECURITY.md).
