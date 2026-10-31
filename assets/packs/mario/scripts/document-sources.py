"""Refresh the exact used-source table while retaining reviewed provenance text."""
from pathlib import Path
import json,re
HERE=Path(__file__).resolve().parents[1]
c=json.loads((HERE/'slicing.json').read_text());records=json.loads((HERE/'sources.json').read_text());lock={s['file']:s for s in records};used=set()
def walk(v):
 if isinstance(v,dict):
  if 'source' in v:used.add(v['source'])
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
walk(c)
p=HERE/'SOURCES.md';s=p.read_text();s=re.sub(r'all \d+ retained download records',f'all {len(records)} retained download records',s)
start=s.index('| Raw file | Exact download URL | SHA-256 |');end=s.index('\n## Ancillary public-safe assets',start)
lines=['| Raw file | Exact download URL | SHA-256 |','|---|---|---|']
for f in sorted(used):
 r=lock[f];lines.append(f'| `{f}` | [source]({r["url"]}) | `{r["sha256"]}` |')
p.write_text(s[:start]+'\n'.join(lines)+'\n'+s[end:]);print(f'Documented {len(used)} used images; {len(records)} total pinned records ({len(lock)} unique files).')
