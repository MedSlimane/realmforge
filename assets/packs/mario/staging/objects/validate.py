"""Verify staging against original pixel data, including source enlargement reversal."""
from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib,math
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 data=json.loads((HERE/'objects.json').read_text());lock=json.loads((HERE/'source-lock.json').read_text())
 assert data['schema']==1
 outputs=lock['outputs'];references=set();max_scale=0;animations=stills=0;decimated=0
 for src in lock['sources'].values():
  p=ROOT/src['path'];assert p.is_file(),p;assert sha(p)==src['sha256'],p
 for path,record in outputs.items():
  p=HERE/path;assert p.is_relative_to(HERE) and p.is_file(),p
  assert sha(p)==record['sha256'],p
  im=Image.open(p);assert im.format=='PNG' and im.mode=='RGBA' and im.size==tuple(record['canvas']),p
  r=record['source'];native=Image.open(ROOT/r['path']);native.seek(r['sourceFrame']);native=native.convert('RGBA')
  d=r['decimate']
  if d!=1:
   decimated+=1;px=native.load()
   assert native.width%d==0 and native.height%d==0
   for y in range(0,native.height,d):
    for x in range(0,native.width,d):
     assert all(px[x+dx,y+dy]==px[x,y] for dy in range(d) for dx in range(d)),p
   native=native.resize((native.width//d,native.height//d),Image.Resampling.NEAREST)
  if r.get('resize'):
   w,h=r['resize'];assert w<=native.width and h<=native.height,'Source upscaling'
   native=native.resize((w,h),Image.Resampling.NEAREST)
  if r['rect']:
   x,y,w,h=r['rect'];assert 0<=x<x+w<=native.width and 0<=y<y+h<=native.height
   native=native.crop((x,y,x+w,y+h))
  expected=Image.new('RGBA',im.size);expected.paste(native,tuple(record['offset']))
  assert im.tobytes()==expected.tobytes(),f'Pixels differ from source: {path}'
 for section in ('elements','fx'):
  for name,e in data[section].items():
   assert e['manifestKey']==f'{section}.{name}'
   assert all(e['source'][k] for k in ('url','game','ripper','method'))
   canvases=set();bboxes=[]
   for n,a in e['anims'].items():
    assert a['frames'] and len(a['frames'])==len(set(a['frames'])),(name,n,'Repeated frame path')
    pixels=[]
    for f in a['frames']:
     assert f in outputs and not Path(f).is_absolute() and '..' not in Path(f).parts
     references.add(f);im=Image.open(HERE/f).convert('RGBA');canvases.add(im.size);b=im.getbbox();assert b,(name,n,'Empty frame')
     bboxes.append((b[2]-b[0],b[3]-b[1]));pixels.append(hashlib.sha256(im.tobytes()).hexdigest())
    if a['kind']=='animation':
     assert len(set(pixels))>1 and a['frameRate']>0,(name,n,'Still misrepresented as animation');animations+=1
    else:
     assert len(a['frames'])==1 and a['frameRate']==0,(name,n,'Still state needs explicit zero FPS');stills+=1
    if 'frameDurationsMs' in a:
     assert len(a['frameDurationsMs'])==len(a['frames']) and all(x>0 for x in a['frameDurationsMs'])
   assert len(canvases)==1,(name,canvases)
   # Audit opaque pixels as well as canvas: transparent padding is not resolution.
   w=max(x[0] for x in bboxes);h=max(x[1] for x in bboxes)
   scale=max(e['displaySize']['w']*64/w,e['displaySize']['h']*64/h);max_scale=max(max_scale,scale)
   assert scale<=1.25+1e-9,(name,'Upscale exceeds 1.25x',scale,w,h)
 assert references==set(outputs),'Unreferenced PNG outputs'
 actual={p.relative_to(HERE).as_posix() for p in HERE.rglob('*.png')}
 assert actual==set(outputs),'Unexpected PNG files'
 size=sum(p.stat().st_size for p in HERE.rglob('*') if p.is_file());assert size<=12_000_000,size
 print(f'PASS: {len(data["elements"])} object entries + {len(data["fx"])} fx entries; {len(outputs)} source-matched RGBA PNGs.')
 print(f'PASS: {animations} real animation sequences; {stills} explicitly labelled still states; consistent canvases per entry.')
 print(f'PASS: {len(lock["sources"])} original files SHA-256 verified; {decimated} outputs restore verified exact 2x source duplication.')
 print(f'PASS: max opaque-content display scale {max_scale:.4f}x <= 1.25x; zero source enlargement, recolouring, synthetic frames or pixel mismatches.')
 print(f'PASS: total staging {size:,} bytes <= 12,000,000 bytes.')
 return data
if __name__=='__main__':main()
