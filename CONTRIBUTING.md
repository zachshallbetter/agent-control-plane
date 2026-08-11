# Contributing

1. Start from a real issue describing scope, exclusions, acceptance, and evidence.
2. Use an issue-numbered branch: `<type>/<issue>-<slug>`.
3. Keep changes within the issue-defined paths.
4. Run `bash -n scripts/*.sh` and `git diff --check`.
5. Include the issue number, checks, evidence, and blockers in the PR.
6. Do not add provider-specific behavior to the policy engine.
7. A maintainer must read and acknowledge the delivery record before merge.

Prefer small, reversible changes. New adapters require contract fixtures and rate-limit behavior tests.
