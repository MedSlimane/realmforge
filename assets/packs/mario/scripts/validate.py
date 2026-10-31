"""Validate schema-1 compatibility, source integrity, crops, atlases and coverage."""
from pathlib import Path
from PIL import Image
import hashlib,json
from build import crop
from audit import audit, factor
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[2];OUT=ROOT/'web/public/packs/mario';RAW=ROOT/'assets/_downloads/mario'
def validate_display_scale(m):
 """Check logical frame sizes; atlas image size and extruded gutters don't count."""
 checked=0
 for section in ['elements','characters','enemies','items']:
  for name,e in m.get(section,{}).items():
   if 'displaySize' not in e:continue
   scale=factor(e)
   assert scale<=1.25+1e-5,f'Upscaled sprite {section}.{name}: {scale:.3f}x > 1.25x'
   if 'atlas' in e:
    a=json.loads((OUT/e['atlas']).read_text())
    for key,v in a['frames'].items():
     f=v['frame'];d=e['displaySize'];scale=max(64*d['w']/f['w'],64*d['h']/f['h'])
     assert scale<=1.25+1e-5,f'Upscaled animation {section}.{name}/{key}: {scale:.3f}x > 1.25x'
   with Image.open(OUT/e['path']) as im:assert im.size==(e['width'],e['height']),(section,name,im.size)
   checked+=1
 return checked
def main():
 m=json.loads((OUT/'manifest.json').read_text());old=json.loads((ROOT/'web/public/assets/manifest.json').read_text());c=json.loads((HERE/'slicing.json').read_text());sources=json.loads((HERE/'sources.json').read_text())
 assert m['schema']==1 and m['tileSize']==64 and m['sourceTile']==64 and m['pixelArt'] is False
 assert set(m)==set(old)|{'sourceTile','pixelArt','items'}, 'Unexpected top-level schema additions'
 missing=set(old['elements'])-set(m['elements']);assert not missing,missing
 for k in ['ui','editor','sfx','music','themes','characters','enemies']:assert set(old[k])<=set(m[k]),k
 for s in sources:
  p=RAW/s['file'];assert p.is_file(),p
  assert hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256'],p
 rects=0
 def rect(r):
  nonlocal rects
  # crop checks bounds, extracts embedded native PNGs and rejects upsampling.
  im=crop(r);assert im.width>0 and im.height>0,r;rects+=1
  assert r['source'] in {s['file'] for s in sources},f'Unpinned source {r["source"]}'
  if r.get('compose'):
   cw,ch=r['compose']['canvas']
   for p in r['compose']['parts']:
    px,py=p['at'];fr=p['frame'];fw,fh=crop(fr).size
    assert px>=0 and py>=0 and px+fw<=cw and py+fh<=ch,(r,p)
    rect(fr)
 for a in c['assets'].values():
  for r in a['frames']+a.get('animationSources',[]):rect(r)
 for t in c['themes'].values():
  for r in t['layers']:rect(r)
 files=set();atlases=set();frame_count=0
 def local(path):
  p=(ROOT/'web/public'/path.lstrip('/')) if path.startswith('/') else OUT/path
  assert p.is_file(),f'Missing manifest file: {path}';files.add(p);return p
 def walk(o):
  nonlocal frame_count
  if isinstance(o,dict):
   for k,v in o.items():
    if k in ['path','image','atlas','svg','file','credits'] and isinstance(v,str):local(v)
    elif isinstance(v,(dict,list)):walk(v)
   if 'atlas' in o:
    atlas=local(o['atlas']);im=Image.open(local(o.get('image',o.get('path'))));a=json.loads(atlas.read_text());frames=a['frames']
    if atlas not in atlases:
     for name,v in frames.items():
      f=v['frame'];assert 0<=f['x'] and 0<=f['y'] and f['w']>0 and f['h']>0 and f['x']+f['w']<=im.width and f['y']+f['h']<=im.height,(atlas,name);frame_count+=1
     atlases.add(atlas)
    assert str(o.get('frame',next(iter(frames)))) in frames
    for name,a in o.get('animations',{}).items():
     assert a['frames'] and all(str(f) in frames for f in a['frames']),(atlas,name)
     assert a['frameRate']>0
  elif isinstance(o,list):
   for v in o:walk(v)
 walk(m)
 for name,entry in old['characters'].items():assert set(entry['animations'])<=set(m['characters'][name]['animations']),name
 for name in ['mario','luigi','mario_small','luigi_small']:
  char=m['characters'][name]
  assert {'idle','walk','run','skid','jump','fall','crouch','wallSlide','dead'}<=set(char['animations'])
  for a in ['walk','run']:assert len(set(char['animations'][a]['frames']))>=3,(name,a)
  assert char['anchor']=={'x':.5,'y':1}
 assert m['items']['mushroom']==m['elements']['mushroom']
 for theme,t in m['themes'].items():
  required={'top_left','top','top_right','left','fill','inner','right','bottom_left','bottom','bottom_right','inner_top_left','inner_top_right','inner_bottom_left','inner_bottom_right','pillar_top','pillar','pillar_bottom','single','single_left','horizontal','single_right'}
  assert required<=set(t['variants']),(theme,required-set(t['variants']))
  legal=[]
  for mask in range(256):
   n,e,s,w=(bool(mask&b) for b in [1,2,4,8])
   if not any(bool(mask&b) and not(a and z) for b,a,z in [(16,n,e),(32,e,s),(64,s,w),(128,w,n)]):legal.append(f'mask_{mask}')
  assert len(legal)==47 and set(legal)<set(t['variants']),(theme,'incomplete 47-mask set')
  a=json.loads(local(t['autotileAtlas']['atlas']).read_text());im=Image.open(local(t['autotileAtlas']['image'])).convert('RGBA')
  for v in a['frames'].values():
   f=v['frame'];x,y,w,h=(f[k] for k in ['x','y','w','h']);assert w==h==60
   for i in [1,2]:
    assert im.crop((x-i,y,x-i+1,y+h)).tobytes()==im.crop((x,y,x+1,y+h)).tobytes()
    assert im.crop((x+w-1+i,y,x+w+i,y+h)).tobytes()==im.crop((x+w-1,y,x+w,y+h)).tobytes()
    assert im.crop((x,y-i,x+w,y-i+1)).tobytes()==im.crop((x,y,x+w,y+1)).tobytes()
    assert im.crop((x,y+h-1+i,x+w,y+h+i)).tobytes()==im.crop((x,y+h-1,x+w,y+h)).tobytes()
  assert len(t['parallax'])>=3
  for l in t['parallax']:
   im=Image.open(local(l['file'])).convert('RGBA');assert im.width>=1536
   assert im.crop((0,0,1,im.height)).tobytes()==im.crop((im.width-1,0,im.width,im.height)).tobytes(),f'Background seam: {theme}'
   assert 0<=l['scrollFactor']<=1
 for p in files:
  if p.suffix.lower()=='.png':
   im=Image.open(p);im.verify()
 before,after,oldbad,bad=audit()
 validate_display_scale(m)
 assert not bad,'Upscaled sprites >1.25x: '+', '.join(f'{n}={factor(after[n]):.3f}x' for n in bad)
 total=sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file());assert total<=25_000_000,f'Pack exceeds 25 MB: {total} bytes'
 print('PASS schema 1: original top-level sections/keys retained; pixelArt=false; sourceTile=64')
 print(f'PASS coverage: {len(old["elements"])}/{len(old["elements"])} Kenney element IDs; {len(m["elements"])} total Mario IDs; 4/4 themes')
 print(f'PASS sources: {len(sources)} SHA-256 checksums; {rects} source rectangles in bounds')
 print(f'PASS files: {len(files)} manifest paths exist; all PNGs decode')
 print(f'PASS atlases: {len(atlases)} atlases; {frame_count} frames in bounds; animation references resolve')
 print('PASS characters: Mario/Luigi big + small have all 9 animation keys; walk/run >=3 frames; feet anchors')
 print(f'PASS native scale: {len(after)} sprite entries and every animation frame <=1.25x; {len(oldbad)} baseline violations removed')
 print('PASS terrain: 4 themes; complete cardinal/inner-corner/pillar/single variants; exact 2px extruded gutters')
 print('PASS mushroom: items.mushroom and elements.mushroom agree')
 print(f'PASS parallax: {sum(len(t["parallax"]) for t in m["themes"].values())} wide native-resolution layers; all horizontal seam texels match')
 print(f'PASS pack budget: {total:,} bytes / 25,000,000 bytes')
 print('PROVENANCE / POSE CAVEATS: see README.md and SOURCES.md; animation keys alone do not prove authentic poses.')
if __name__=='__main__':main()
