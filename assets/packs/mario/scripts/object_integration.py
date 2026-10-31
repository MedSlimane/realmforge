"""Pack completed, provenance-locked object staging without changing source pixels.

Preparation writes only the owned source directory. Publication is an explicit
build option because public object paths are outside the character lane.
"""
from pathlib import Path
from PIL import Image
import copy, hashlib, json, math, shutil

HERE=Path(__file__).resolve().parents[1]
OUT=HERE.parents[2]/'web/public/packs/mario'

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def prepare(folder=None,destination=None):
 folder=folder or HERE/'staging/objects'
 destination=destination or HERE/'integrated'
 assert (folder/'DONE').is_file(),'Object staging is incomplete'
 data=json.loads((folder/'objects.json').read_text())
 lock=json.loads((folder/'source-lock.json').read_text())
 assert data['schema']==lock['schema']==1
 result={'schema':1,'elements':{},'fx':{},'notes':data.get('notes',[])};files={}
 for section in ('elements','fx'):
  for name,e in data[section].items():
   assert e['manifestKey']==f'{section}.{name}'
   paths=list(dict.fromkeys([e['path']]+[p for a in e['anims'].values() for p in a['frames']]))
   images=[];names={};w,h=e['canvas']['w'],e['canvas']['h']
   for i,path in enumerate(paths):
    p=Path(path);assert not p.is_absolute() and '..' not in p.parts
    source=folder/p;assert digest(source)==lock['outputs'][path]['sha256'],path
    with Image.open(source) as image:im=image.convert('RGBA')
    assert im.size==(w,h),(name,path,im.size)
    images.append(im);names[path]=f'{name}_{i:03}'
   columns=min(12,len(images));atlas=Image.new('RGBA',(w*columns,h*math.ceil(len(images)/columns)));table={}
   for i,(path,im) in enumerate(zip(paths,images)):
    x,y=(i%columns)*w,(i//columns)*h;atlas.paste(im,(x,y))
    table[names[path]]={'frame':{'x':x,'y':y,'w':w,'h':h},'rotated':False,'trimmed':False,'sourceSize':{'w':w,'h':h},'spriteSourceSize':{'x':0,'y':0,'w':w,'h':h}}
   relative=Path('objects')/section/name;target=destination/relative;target.mkdir(parents=True,exist_ok=True)
   images[0].save(target/'default.png',optimize=True);atlas.save(target/'atlas.png',optimize=True)
   (target/'atlas.json').write_text(json.dumps({'frames':table,'meta':{'image':'atlas.png','size':{'w':atlas.width,'h':atlas.height},'scale':'1'}},indent=2)+'\n')
   entry={'texture':f'mario-{name}' if section=='elements' else f'mario-fx-{name}','path':str(relative/'default.png'),'image':str(relative/'atlas.png'),'atlas':str(relative/'atlas.json'),'frame':names[e['path']],'width':w,'height':h,'source':e['source']['url'],'provenance':copy.deepcopy(e['source']),'pack':'mario-nsmbu','anchor':e['anchor'],'displaySize':e['displaySize'],'note':e.get('note',''),'missingAnimations':e.get('missingAnimations',[])}
   animations={}
   for anim,a in e['anims'].items():
    if a['kind']=='still':
     assert len(a['frames'])==1 and a['frameRate']==0,(name,anim)
     # Single artwork variants stay named still states, never temporal FX.
     if section=='fx':continue
    else:
     assert a['frameRate']>0 and len({images[paths.index(p)].tobytes() for p in a['frames']})>1,(name,anim)
    animations[anim]={'frames':[names[p] for p in a['frames']],'frameRate':a['frameRate'] or 1,'repeat':-1 if anim in ('idle','scroll') and a['kind']=='animation' else 0,'kind':a['kind']}
    if 'frameDurationsMs' in a:animations[anim]['frameDurationsMs']=a['frameDurationsMs']
   if animations:entry['animations']=animations
   if section=='fx':
    idle=animations.get('idle')
    if idle:entry.update({'frames':idle['frames'],'frameRate':idle['frameRate']})
    else:entry['variants']=[names[p] for p in paths]
   result[section][name]=entry
   for filename in ('default.png','atlas.png','atlas.json'):
    p=relative/filename;files[p.as_posix()]={'path':str((destination/p).relative_to(HERE)),'sha256':digest(destination/p)}
 # Confirm packing preserved every original RGBA byte, including alpha.
 for section in ('elements','fx'):
  for name,e in result[section].items():
   original=data[section][name];paths=list(dict.fromkeys([original['path']]+[p for a in original['anims'].values() for p in a['frames']]))
   with Image.open(destination/e['image']) as packed:
    table=json.loads((destination/e['atlas']).read_text())['frames']
    for i,path in enumerate(paths):
     f=table[f'{name}_{i:03}']['frame'];actual=packed.crop((f['x'],f['y'],f['x']+f['w'],f['y']+f['h'])).convert('RGBA')
     with Image.open(folder/path) as source:assert actual.tobytes()==source.convert('RGBA').tobytes(),(name,path)
 destination.mkdir(parents=True,exist_ok=True)
 (destination/'manifest-fragment.json').write_text(json.dumps(result,indent=2)+'\n')
 (destination/'files.json').write_text(json.dumps(files,indent=2)+'\n')
 print(f'PREPARED staging: {len(result["elements"])} object entries + {len(result["fx"])} FX entries; {len(files)} files; all atlas frames match staged RGBA bytes')
 return result,files

def publish(files,out=None):
 out=out or OUT
 for relative,record in files.items():
  path=Path(relative);assert path.parts[0]=='objects' and '..' not in path.parts
  source=HERE/record['path'];assert digest(source)==record['sha256']
  target=out/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
 print(f'PUBLISHED staging: {len(files)} validated files under objects/')

def published(files,out=None):
 out=out or OUT
 return all((out/path).is_file() and digest(out/path)==record['sha256'] for path,record in files.items())

if __name__=='__main__':prepare()
