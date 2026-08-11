"""Validated project-local ACP policy with explicit defaults and overrides."""
import json
from pathlib import Path

DEFAULTS={"policy_version":"0.1.0","statuses":{"ready":"Ready","review":"In review","done":"Done","verified":"Verified"},"retry":{"max_attempts":3,"base_seconds":2,"max_seconds":60},"snapshot_interval_seconds":60,"require_human_acknowledgement":True,"providers":{"github":{"enabled":True},"railway":{"enabled":False},"vercel":{"enabled":False}}}

def load(path='.acp/config.json'):
    data=json.loads(Path(path).read_text()) if Path(path).exists() else {}
    policy=dict(DEFAULTS); policy.update(data); policy['statuses']={**DEFAULTS['statuses'],**data.get('statuses',{})}; policy['retry']={**DEFAULTS['retry'],**data.get('retry',{})}; policy['providers']={**DEFAULTS['providers'],**data.get('providers',{})}
    if policy['retry']['max_attempts'] < 1 or policy['snapshot_interval_seconds'] < 0: raise ValueError('policy limits must be non-negative and max_attempts must be positive')
    return policy
