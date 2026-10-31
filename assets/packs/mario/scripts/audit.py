"""Native pixel/display audit. The saved baseline is the unmodified starting manifest."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[2];OUT=ROOT/'web/public/packs/mario'

def entries(m):
 return {f'{section}.{name}':e for section in ['elements','characters','enemies','items'] for name,e in m.get(section,{}).items() if 'displaySize' in e}

def factor(e):
 d=e['displaySize'];return max(64*d['w']/e['width'],64*d['h']/e['height'])

def size(e):
 if e is None:return '—'
 return f'{e["width"]}×{e["height"]} → {64*e["displaySize"]["w"]:.1f}×{64*e["displaySize"]["h"]:.1f}'

def audit():
 before=entries(json.loads((HERE/'audit-before.json').read_text()));after=entries(json.loads((OUT/'manifest.json').read_text()))
 lines=['# Mario pack native-resolution audit','',
 'Each row compares the native frame canvas to `displaySize × 64` gameplay pixels. Atlas padding is excluded. A uniform atlas canvas preserves pose scale and feet; transparent space is not detail. Individual source crop rectangles and any **downsampling** are in `slicing.json`. The builder forbids source upsampling. Background layers have no `displaySize` and are audited for native pixels/seams separately. No AI-generated art is used.','',
 'Before is frozen in `audit-before.json`, captured before this pass. Before/after factors include both axes; entries above 1.25 fail `npm run validate`. New entries have no before value. Compatibility aliases appear explicitly.','',
 '| Sprite | Before native → display px | Before factor | After native → display px | After factor | Status / caveat |','|---|---|---:|---|---:|---|']
 for name in dict.fromkeys([*before,*after]):
  b=before.get(name);a=after.get(name);note=(a or b).get('note','').replace('|','/')
  status='REMOVED' if a is None else 'FAIL >1.25' if factor(a)>1.25+1e-5 else 'PASS'
  lines.append(f'| `{name}` | {size(b)} | {factor(b):.3f}×' if b else f'| `{name}` | — | —')
  lines[-1]+=f' | {size(a)} | '+(f'{factor(a):.3f}×' if a else '—')+f' | {status}'+(f'; {note}' if note else '')+' |'
 lines+=['','## Animation frames','',
 'Every current atlas frame is listed below. The factor applies to the full fixed native canvas, including deliberately transparent pose margins; no animation may use a different runtime scale. Frame names map to exact native source crops in `slicing.json`.','',
 '| Sprite / frame | Native px | Display px | Upscale |','|---|---|---|---:|']
 seen=set()
 for name,e in after.items():
  if 'atlas' not in e or e['atlas'] in seen:continue
  seen.add(e['atlas']);a=json.loads((OUT/e['atlas']).read_text())
  for key,r in a['frames'].items():
   f=r['frame'];d=e['displaySize'];scale=max(d['w']*64/f['w'],d['h']*64/f['h'])
   lines.append(f'| `{name}/{key}` | {f["w"]}×{f["h"]} | {64*d["w"]:.1f}×{64*d["h"]:.1f} | {scale:.3f}× |')
 badbefore=[n for n,e in before.items() if factor(e)>1.25+1e-5];badafter=[n for n,e in after.items() if factor(e)>1.25+1e-5]
 lines+=['','## Result','',f'- Before: **{len(badbefore)}/{len(before)}** sprite entries above 1.25×.',f'- After: **{len(badafter)}/{len(after)}** sprite entries above 1.25×.', '- Known semantic substitutions are disclosed in README.md and the entry notes; a scale pass is not a provenance or pose-completeness claim.']
 (HERE/'AUDIT.md').write_text('\n'.join(lines)+'\n')
 return before,after,badbefore,badafter
if __name__=='__main__':
 b,a,bb,ba=audit();print(f'AUDIT: {len(bb)}/{len(b)} above limit before; {len(ba)}/{len(a)} after. See AUDIT.md.')
