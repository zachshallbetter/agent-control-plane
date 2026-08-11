#!/usr/bin/env python3
"""Generate deterministic ACP context and a source-hash manifest."""
import hashlib,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'.llms'; OUT.mkdir(exist_ok=True)
paths=[ROOT/'README.md',ROOT/'CONTRIBUTING.md',ROOT/'docs',ROOT/'schemas',ROOT/'skills',ROOT/'agents']
files=[]
for source in paths:
    candidates=[source] if source.is_file() else sorted(source.rglob('*'))
    files += [p for p in candidates if p.is_file() and '.git' not in p.parts]
files=sorted(set(files)); chunks=[]; entries=[]
for path in files:
    data=path.read_bytes(); rel=path.relative_to(ROOT).as_posix(); digest=hashlib.sha256(data).hexdigest(); entries.append({'path':rel,'sha256':digest}); chunks.append(f'\n## {rel}\n\n{data.decode("utf-8", "replace")}')
full=''.join(chunks); index='\n'.join(f'- {entry["path"]} sha256={entry["sha256"]}' for entry in entries)+'\n'
(OUT/'llms-full.txt').write_text(full); (OUT/'llms.txt').write_text(index)
manifest={'schema':'acp.context-manifest.v1','policy_version':'0.1.0','generated_at':int(time.time()),'files':entries,'llms_sha256':hashlib.sha256(index.encode()).hexdigest(),'llms_full_sha256':hashlib.sha256(full.encode()).hexdigest()}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n'); print(f'generated {len(files)} context sources in {OUT}')
