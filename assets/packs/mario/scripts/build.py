"""Rebuild native PNGs/Phaser atlases from exact checked-in source rectangles.
Only crops, alpha trimming/padding, native-asset composites, downsampling and horizontal
mirror repeats are performed. There is no AI art, pixel upscaling, or copied game code.
"""
from pathlib import Path
from PIL import Image, ImageOps
import copy, json, math, base64, io, re
from functools import lru_cache
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[2]
RAW=ROOT/'assets/_downloads/mario';OUT=ROOT/'web/public/packs/mario'

def write_json(path,value):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2)+'\n')

@lru_cache(maxsize=128)
def source_image(source,embedded=-1,frame=0):
 if embedded>=0:
  encoded=re.findall(rb'data:image/[^;]+;base64,([^"\s]+)',(RAW/source).read_bytes())[embedded]
  im=Image.open(io.BytesIO(base64.b64decode(encoded)))
 else:im=Image.open(RAW/source)
 try:
  im.seek(frame)
  return im.convert('RGBA')
 finally:im.close()

def crop(ref):
 if 'compose' in ref:
  c=ref['compose'];im=Image.new('RGBA',tuple(c['canvas']))
  for part in c['parts']:im.alpha_composite(crop(part['frame']),tuple(part['at']))
  return im
 im=source_image(ref['source'],ref.get('embeddedImage',-1),ref.get('sourceFrame',0))
 x,y,w,h=ref['rect']
 if x<0 or y<0 or w<=0 or h<=0 or x+w>im.width or y+h>im.height:raise ValueError(ref)
 im=im.crop((x,y,x+w,y+h))
 if ref.get('flipX'):im=ImageOps.mirror(im)
 if 'resize' in ref:
  size=tuple(ref['resize']);assert size[0]<=im.width and size[1]<=im.height, 'Upsampling source art is forbidden'
  im=im.resize(size,Image.Resampling.LANCZOS)
 return im

def extrude(im,padding=2):
 """Duplicate edge texels into a gutter, without stretching any artwork."""
 w,h=im.size;out=Image.new('RGBA',(w+2*padding,h+2*padding));out.paste(im,(padding,padding))
 for d in range(padding):
  out.paste(im.crop((0,0,w,1)),(padding,d));out.paste(im.crop((0,h-1,w,h)),(padding,padding+h+d))
  out.paste(im.crop((0,0,1,h)),(d,padding));out.paste(im.crop((w-1,0,w,h)),(padding+w+d,padding))
 for x in range(padding):
  for y in range(padding):
   for dx,dy,sx,sy in [(x,y,0,0),(padding+w+x,y,w-1,0),(x,padding+h+y,0,h-1),(padding+w+x,padding+h+y,w-1,h-1)]:out.putpixel((dx,dy),im.getpixel((sx,sy)))
 return out

def save(im,path):
 p=OUT/path;p.parent.mkdir(parents=True,exist_ok=True);im.save(p,optimize=True)

def make_asset(id,spec):
 raw=[crop(r) for r in spec['frames']]
 assert not spec.get('recolor'), 'Recoloured character substitutes are forbidden'
 # A uniform native canvas prevents feet jitter. Cropped pixels are never scaled.
 w=max(i.width for i in raw);h=max(i.height for i in raw)
 frames=[]
 for im in raw:
  f=Image.new('RGBA',(w,h));f.alpha_composite(im,((w-im.width)//2,h-im.height));frames.append(f)
 save(frames[0],spec['path'])
 entry={'texture':f'mario-{id}','path':spec['path'],'width':w,'height':h,'source':spec['frames'][0]['source'],'pack':'mario-nsmbu'}
 for key in ['displaySize','anchor','note']:
  if key in spec:entry[key]=spec[key]
 if spec.get('characterHeight'):
  # Native idle artwork is exactly 1 or 2 gameplay tiles tall; other poses retain scale.
  idle_index=spec['animations']['idle'][0];reference=raw[idle_index].height;scale=spec['characterHeight']/reference
  entry['displaySize']={'w':round(w*scale,5),'h':round(h*scale,5)}
 animations=spec.get('animations',{})
 if spec.get('animationSources'):
  frames=[crop(r) for r in spec['animationSources']];w=max(i.width for i in frames);h=max(i.height for i in frames)
  padded=[]
  for im in frames:
   f=Image.new('RGBA',(w,h));f.alpha_composite(im,((w-im.width)//2,h-im.height));padded.append(f)
  frames=padded
  animations={'idle':list(range(len(frames)))}
 if animations:
  columns=min(12,len(frames));atlas=Image.new('RGBA',(w*columns,h*math.ceil(len(frames)/columns)));table={}
  for i,im in enumerate(frames):
   x=i%columns*w;y=i//columns*h;atlas.alpha_composite(im,(x,y));table[f'{id}_{i}']={'frame':{'x':x,'y':y,'w':w,'h':h},'rotated':False,'trimmed':False,'spriteSourceSize':{'x':0,'y':0,'w':w,'h':h},'sourceSize':{'w':w,'h':h}}
  folder=Path(spec['path']).parent/id if not spec.get('characterHeight') else Path(spec['path']).parent
  image=str(folder/'atlas.png');atlas_path=str(folder/'atlas.json');save(atlas,image)
  write_json(OUT/atlas_path,{'frames':table,'meta':{'app':'RealmForge native asset slicer','image':'atlas.png','size':{'w':atlas.width,'h':atlas.height},'scale':'1'}})
  entry.update({'image':image,'atlas':atlas_path,'frame':f'{id}_{animations.get("idle",list(animations.values())[0])[0]}','animations':{}})
  for name,indices in animations.items():
   rate=14 if name=='run' else 10 if name in ('walk','move','bounce','spin','kick') else 8 if len(indices)>1 else 1
   entry['animations'][name]={'frames':[f'{id}_{i}' for i in indices],'frameRate':rate,'repeat':-1 if name in ('idle','run','walk','move','spin') else 0}
 return entry

def build():
 c=json.loads((HERE/'slicing.json').read_text());old=json.loads((ROOT/'web/public/assets/manifest.json').read_text())
 m={k:copy.deepcopy(old[k]) for k in ['schema','tileSize','ui','editor','sfx','music']}
 m.update({'baseUrl':'/packs/mario/','license':'Nintendo proprietary; private educational class demo only. Ancillary Kenney UI/audio: CC0-1.0.','pixelArt':False,'sourceTile':64,'elements':{},'characters':{},'enemies':{},'themes':{},'credits':'credits.json'})
 # Preserve original keys and CC0 ancillary references without modifying or duplicating the Kenney pack.
 for section in ['ui','editor','sfx','music']:
  for entry in m[section].values():
   for key in ['path','image','atlas','svg']:
    if key in entry:entry[key]='/assets/'+entry[key]
 entries={id:make_asset(id,spec) for id,spec in c['assets'].items()}
 chars=set(c['characters'].values());m['elements']={id:e for id,e in entries.items() if id not in chars}
 for name,id in c['characters'].items():m['characters'][name]=entries[id]
 for name,target in [('green','luigi'),('pink','mario'),('purple','mario'),('beige','mario')]:
  m['characters'][name]=copy.deepcopy(entries[target]);m['characters'][name]['note']=f'Schema-1 compatibility name mapped to {target}; not a separate character rip.'
 for name,id in c['enemies'].items():m['enemies'][name]=entries[id]
 m['items']={'mushroom':entries['mushroom']}
 # 64px native theme sheets retain the original Kenney tile indices.
 tile_order=list(old['themes']['grass']['tiles'])
 for theme,t in c['themes'].items():
  sheet=Image.new('RGBA',(8*64,2*64))
  for i,variant in enumerate(tile_order):
   id=f'{theme}_{variant}' if f'{theme}_{variant}' in entries else variant
   im=crop(c['assets'][id]['frames'][0])
   # Keep the legacy 64px grid; 60px native terrain carries 2px edge extrusion.
   if im.size==(60,60):im=extrude(im)
   elif im.size!=(64,64):im=im.resize((64,64),Image.Resampling.LANCZOS)
   sheet.alpha_composite(im,(i%8*64,i//8*64))
  path=f'tiles/{theme}/tileset.png';save(sheet,path)
  layers=[]
  for layer in t['layers']:
   native=crop(layer);pair=Image.new('RGBA',(native.width*2,native.height));pair.alpha_composite(native,(0,0));pair.alpha_composite(ImageOps.mirror(native),(native.width,0))
   # Mirrored native modules have matching boundary texels, giving a seamless period.
   count=max(1,math.ceil(1536/pair.width));wide=Image.new('RGBA',(pair.width*count,pair.height))
   for i in range(count):wide.alpha_composite(pair,(i*pair.width,0))
   save(wide,layer['file']);layers.append({'file':layer['file'],'scrollFactor':layer['scrollFactor']})
  first=layers[0]['file'];im=Image.open(OUT/first)
  bg={'texture':f'background_{theme}','path':first,'width':im.width,'height':im.height,'source':t['layers'][0]['source'],'pack':'mario-nsmbu'}
  m['themes'][theme]={**copy.deepcopy(old['themes'][theme]),'path':path,'background':bg,'parallax':layers}
  m['elements'][f'background_{theme}']=bg
  # An additive atlas for renderers that consume explicit autotile variants.
  variants=t.get('variants',{})
  if variants:
   columns=8;cell=64;atlas=Image.new('RGBA',(columns*cell,math.ceil(len(variants)/columns)*cell));table={}
   for i,(variant,id) in enumerate(variants.items()):
    im=crop(c['assets'][id]['frames'][0]);assert im.size==(60,60),(id,im.size)
    x=i%columns*cell;y=i//columns*cell;atlas.paste(extrude(im),(x,y))
    table[variant]={'frame':{'x':x+2,'y':y+2,'w':60,'h':60},'rotated':False,'trimmed':False,'spriteSourceSize':{'x':0,'y':0,'w':60,'h':60},'sourceSize':{'w':60,'h':60}}
   folder=f'tiles/{theme}';save(atlas,f'{folder}/autotiles.png');write_json(OUT/f'{folder}/autotiles.json',{'frames':table,'meta':{'image':'autotiles.png','size':{'w':atlas.width,'h':atlas.height},'scale':'1','padding':2}})
   m['themes'][theme]['autotileAtlas']={'texture':f'mario-{theme}-autotiles','image':f'{folder}/autotiles.png','atlas':f'{folder}/autotiles.json','padding':2}
   m['themes'][theme]['variants']={name:entries[id] for name,id in variants.items()}
 # Compatibility aliases are fully materialized: the existing registry need not understand aliasOf.
 for id,entry in old['elements'].items():
  if id not in m['elements']:
   target=entry.get('aliasOf')
   if target not in m['elements']:raise ValueError(f'Uncovered {id} -> {target}')
   m['elements'][id]={**copy.deepcopy(m['elements'][target]),'aliasOf':target}
 # pipe deliberately remains a real pipe rather than the legacy Kenney door alias.
 write_json(OUT/'manifest.json',m)
 write_json(OUT/'credits.json',{'notice':'Nintendo property, used for a private educational class demo only; do not distribute publicly; Kenney CC0 pack remains the public-safe fallback.','provenance':'See assets/packs/mario/SOURCES.md and sources.json for source URLs and SHA-256 checksums.','ancillary':'/assets/credits.json'})
 # Remove obsolete generated rips, including unused low-resolution atlases. Only
 # this pack is owned by the slicer; absolute ancillary /assets URLs are untouched.
 keep={'manifest.json','credits.json','PREVIEW.png'}
 def referenced(v):
  if isinstance(v,dict):
   for k,x in v.items():
    if k in ['path','image','atlas','file'] and isinstance(x,str) and not x.startswith('/'):keep.add(x)
    elif isinstance(x,(dict,list)):referenced(x)
  elif isinstance(v,list):
   for x in v:referenced(x)
 referenced(m)
 for p in OUT.rglob('*'):
  if p.is_file() and p.relative_to(OUT).as_posix() not in keep:p.unlink()
 # Every actual element and compatibility alias is reviewable without reading code.
 lines=['# Mario pack coverage','', '| Element | File |','|---|---|']
 lines += [f'| `{id}` | `{e["path"]}` |' for id,e in m['elements'].items()]
 (HERE/'COVERAGE.md').write_text('\n'.join(lines)+'\n')
 print(f'Built {len(m["elements"])} element IDs, {len(m["characters"])} character keys, {len(m["enemies"])} enemies, {len(m["themes"])} themes and {sum(len(t["parallax"]) for t in m["themes"].values())} parallax layers.')
if __name__=='__main__':build()
