---
name: github-projects
description: Govern GitHub Issues, ProjectsV2, pull requests, claims, evidence, and status transitions through ACP.
---

# GitHub Projects skill

Use this skill whenever work involves a GitHub issue, Project board, PR, dependency, claim, or status change.

## Required sequence

1. Run the local doctor and verify authentication/scopes.
2. Read the issue, parent/epic, dependencies, exclusions, acceptance criteria, and evidence requirements.
3. Resolve the owning repository and verify its origin.
4. Refresh or consume the bounded Project snapshot.
5. Run ACP admission; only `APPROVED` permits a claim or worktree.
6. Implement only within authorized paths.
7. Run scope audit and repository checks.
8. Record evidence and run qualification.
9. Require explicit human acknowledgement before merge or status promotion.

## Stop conditions

Stop on incomplete metadata, stale corpus/policy, repository mismatch, blocked dependency, missing authentication, rate limit, unauthorized path, or unavailable required check. Resolve only the named blocker and resubmit the same packet.
