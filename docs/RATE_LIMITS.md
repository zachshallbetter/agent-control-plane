# Provider access and rate limits

Provider checks are target-aware and bounded. A doctor run performs at most one read for the selected Project. It never probes a default or unrelated Project, retries a failed provider request, or mutates state after an access failure.

Use `--owner` and `--project`, or set `GH_PROJECT_OWNER` and `GH_PROJECT_NUMBER`. A rate-limit or authorization failure is a `BLOCKED` provider condition; resume after access recovers.
