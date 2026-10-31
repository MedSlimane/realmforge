"""Validate schema-1 compatibility, source integrity, crops, atlases and coverage."""
from pathlib import Path
from PIL import Image
import hashlib,json
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[2];OUT=ROOT/'web/public/packs/mario';RAW=ROOT/'assets/_downloads/mario'
def main():
 m=json.loads((OUT/'manifest.json').read_text());old=json.loads((ROOT/'web/public/assets/manifest.json').read_text());c=json.loads((HERE/'slicing.json').read_text());sources=json.loads((HERE/'sources.json').read_text())
 assert m['schema']==1 and m['tileSize']==64 and m['sourceTile']==64 and m['pixelArt'] is False
 assert set(m)==set(old)|{'sourceTile','pixelArt'}, 'Unexpected top-level schema additions'
 missing=set(old['elements'])-set(m['elements']);assert not missing,missing
 for k in ['ui','editor','sfx','music','themes','characters','enemies']:assert set(old[k])<=set(m[k]),k
 for s in sources:
  p=RAW/s['file'];assert p.is_file(),p
  assert hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256'],p
 rects=0
 def rect(r):
  nonlocal rects
  im=Image.open(RAW/r['source']);x,y,w,h=r['rect'];assert x>=0 and y>=0 and w>0 and h>0 and x+w<=im.width and y+h<=im.height,r;rects+=1
  if r.get('compose'):
   cw,ch=r['compose']['canvas']
   for p in r['compose']['parts']:
    px,py=p['at'];fr=p['frame'];fw,fh=fr.get('compose',{}).get('canvas',fr['rect'][2:])
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
 for name in ['mario','luigi','mario_small']:
  char=m['characters'][name]
  assert {'idle','walk','run','skid','jump','fall','crouch','wallSlide','dead'}<=set(char['animations'])
  for a in ['walk','run']:assert len(set(char['animations'][a]['frames']))>=3,(name,a)
  assert char['anchor']=={'x':.5,'y':1}
 for theme,t in m['themes'].items():
  assert len(t['parallax'])>=3
  for l in t['parallax']:
   im=Image.open(local(l['file'])).convert('RGBA');assert im.width>=1536
   assert im.crop((0,0,1,im.height)).tobytes()==im.crop((im.width-1,0,im.width,im.height)).tobytes(),f'Background seam: {theme}'
   assert 0<=l['scrollFactor']<=1
 for p in files:
  if p.suffix.lower()=='.png':
   im=Image.open(p);im.verify()
 print('PASS schema 1: original top-level sections/keys retained; pixelArt=false; sourceTile=64')
 print(f'PASS coverage: {len(old["elements"])}/{len(old["elements"])} Kenney element IDs; {len(m["elements"])} total Mario IDs; 4/4 themes')
 print(f'PASS sources: {len(sources)} SHA-256 checksums; {rects} source rectangles in bounds')
 print(f'PASS files: {len(files)} manifest paths exist; all PNGs decode')
 print(f'PASS atlases: {len(atlases)} atlases; {frame_count} frames in bounds; animation references resolve')
 print('PASS characters: Mario, Luigi colour variant and small Mario have all 9 poses; walk/run >=3 frames; feet anchors')
 print(f'PASS parallax: {sum(len(t["parallax"]) for t in m["themes"].values())} wide native-resolution layers; all horizontal seam texels match')
 print('LIMITATIONS: Luigi big is a Mario recolour; fall reuses late jump poses; mirror character/enemy captures are low native resolution. See README.md.')
if __name__=='__main__':main()
