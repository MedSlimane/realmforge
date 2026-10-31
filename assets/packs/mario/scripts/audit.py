"""Audit opaque native pixels, never treating transparent canvas as image detail."""
from pathlib import Path
from functools import lru_cache
from PIL import Image
import json
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[2];OUT=ROOT/'web/public/packs/mario'

def entries(m):
 return {f'{section}.{name}':e for section in ['elements','characters','enemies','items'] for name,e in m.get(section,{}).items() if 'displaySize' in e}

def factor(e,native=None):
 w,h=native or (e['width'],e['height']);d=e['displaySize']
 return max(64*d['w']/w,64*d['h']/h)

def opaque_size(im):
 b=im.convert('RGBA').getchannel('A').getbbox()
 assert b is not None,'Empty sprite has no native opaque pixels'
 return b[2]-b[0],b[3]-b[1]

@lru_cache(maxsize=64)
def read_image(path):
 with Image.open(path) as im:return im.convert('RGBA')

def native_frames(e):
 if 'atlas' not in e:return [(None,read_image(str(OUT/e['path'])))]
 a=json.loads((OUT/e['atlas']).read_text());im=read_image(str(OUT/e['image']));result=[]
 for name,v in a['frames'].items():
  f=v['frame'];result.append((name,im.crop((f['x'],f['y'],f['x']+f['w'],f['y']+f['h']))))
 return result

def content_size(e):
 """Pose envelope: narrow edge-on coins/crouches keep the cycle's common scale.
 Empty border around every frame cannot enlarge this native content budget.
 """
 sizes=[opaque_size(im) for _,im in native_frames(e)]
 return max(w for w,h in sizes),max(h for w,h in sizes)

def audit():
 read_image.cache_clear()
 before=entries(json.loads((HERE/'audit-before.json').read_text()));after=entries(json.loads((OUT/'manifest.json').read_text()))
 lines=['# Mario pack native-resolution audit','',
 'Current factors compare **native opaque content** against `displaySize × 64`, excluding transparent margins and atlas gutters. For an animation the maximum opaque width/height over its genuine poses defines a common content envelope: a naturally narrow edge-on coin or crouch does not get enlarged independently. Every frame below also lists its own opaque dimensions and the opaque dimensions actually drawn by the canvas-based renderer. No transparent canvas counts as native detail. The builder rejects source upsampling.','',
 'The frozen baseline only recorded canvas dimensions; its factors are historical canvas measurements, not newly verified opaque-content measurements. A scale pass does not certify exact-game provenance. See RESOLUTION_REPORT.md.','',
 '| Sprite | Before canvas → display px | Historical factor | After opaque envelope → display px | Content factor | Status / caveat |','|---|---|---:|---|---:|---|']
 for name in dict.fromkeys([*before,*after]):
  b=before.get(name);a=after.get(name);note=(a or b).get('note','').replace('|','/')
  def size(e,native):return f'{native[0]}×{native[1]} → {64*e["displaySize"]["w"]:.1f}×{64*e["displaySize"]["h"]:.1f}'
  old=size(b,(b['width'],b['height'])) if b else '—';new=size(a,content_size(a)) if a else '—'
  f=factor(a,content_size(a)) if a else 0;status='REMOVED' if a is None else 'FAIL >1.25' if f>1.25+1e-5 else 'PASS'
  lines.append(f'| `{name}` | {old} | '+(f'{factor(b):.3f}×' if b else '—')+f' | {new} | '+(f'{f:.3f}×' if a else '—')+f' | {status}'+(f'; {note}' if note else '')+' |')
 lines+=['','## Animation frames','',
 'Opaque display dimensions include the real fraction of each fixed canvas occupied by the pose. Frame names resolve to exact source crops in slicing.json. The final column checks the shared opaque envelope against the requested display size; it cannot be improved by adding transparent padding.','',
 '| Sprite / frame | Native opaque px | Actual opaque display px | Content-envelope factor |','|---|---|---|---:|']
 seen=set()
 for name,e in after.items():
  if 'atlas' not in e or e['atlas'] in seen:continue
  seen.add(e['atlas']);common=factor(e,content_size(e));d=e['displaySize']
  for key,im in native_frames(e):
   w,h=opaque_size(im)
   lines.append(f'| `{name}/{key}` | {w}×{h} | {64*d["w"]*w/im.width:.1f}×{64*d["h"]*h/im.height:.1f} | {common:.3f}× |')
 badbefore=[n for n,e in before.items() if factor(e)>1.25+1e-5];badafter=[n for n,e in after.items() if factor(e,content_size(e))>1.25+1e-5]
 lines+=['','## Result','',f'- Historical canvas baseline: **{len(badbefore)}/{len(before)}** entries above 1.25×.',f'- Current opaque-content audit: **{len(badafter)}/{len(after)}** entries above 1.25×.', '- Remaining semantic substitutions are disclosed in README.md and RESOLUTION_REPORT.md.']
 (HERE/'AUDIT.md').write_text('\n'.join(lines)+'\n')
 return before,after,badbefore,badafter
if __name__=='__main__':
 b,a,bb,ba=audit();print(f'AUDIT: {len(bb)}/{len(b)} historical canvas violations; {len(ba)}/{len(a)} opaque-content violations. See AUDIT.md.')
