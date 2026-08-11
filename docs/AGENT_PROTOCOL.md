# Agent protocol

The portable protocol is line-oriented JSON over standard input/output or an equivalent tool call.

```json
{"operation":"admission","packet":"packet.json"}
{"operation":"qualification","scope_passed":true,"checks_passed":true,"human_acknowledged":false}
```

Every response contains a typed `decision`, stable `policy_version`, `decision_id`, reason, and any blockers/evidence references. Human-readable logs go to stderr; machine-readable decisions go to stdout.
