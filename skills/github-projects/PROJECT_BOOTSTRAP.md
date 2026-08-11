# GitHub Projects bootstrap

ACP can plan or apply a standard ProjectsV2 setup:

```bash
scripts/github-project-init.sh --owner org --name "Delivery" \
  --repositories org/app,org/services
scripts/github-project-init.sh --owner org --name "Delivery" \
  --repositories org/app,org/services --apply
```

Population uses a JSONL manifest:

```json
{"url":"https://github.com/org/repo/issues/123"}
{"url":"https://github.com/org/repo/issues/124"}
```

```bash
scripts/github-project-populate.sh --owner org --project 3 --manifest project.jsonl
```

Creation and population are separate, explicit mutations. Views, field option
types, native relationships, and issue metadata must be verified after creation;
the bootstrap scripts do not pretend that a Project is ready merely because it
exists.
