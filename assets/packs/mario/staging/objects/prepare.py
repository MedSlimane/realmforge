"""Extract real source frames. No drawing, recolouring, interpolation or enlargement.
Run from the repository root; originals remain in the ignored object download cache.
"""
from pathlib import Path
from PIL import Image
import json, hashlib, urllib.request, concurrent.futures
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
RAW=ROOT/'assets/_downloads/objects'
OLD=ROOT/'assets/_downloads/mario'
LOCK=json.loads((ROOT/'assets/packs/mario/sources.json').read_text())
selected={x['name']:x for x in json.loads((RAW/'selected.json').read_text())}
meta=json.loads((RAW/'wiki-source-metadata.json').read_text())['query']['pages']
meta={x['title'].replace(' ','_'):x for x in meta.values()}
manifest={'schema':1,'elements':{},'fx':{},'notes':[
 'STAGING INPUT ONLY: the characters integrator must publish frames or assemble atlases; every path here is relative to staging/objects, not web/public.',
 'Nintendo proprietary imagery, authorized by the team only for its private class demo. No Nintendo copyright licence is claimed.',
 'Single-frame states are explicit stills. Missing named animations are omitted; do not alias a still as an animation.',
 'Source Scratch rasters were enlarged 2x before upload. Exact replicated pixels are decimated back to their original native grid; this pass never upscales.',
 'Existing pack pswitch corresponds to the frozen p_switch object name. Existing falling_block and saw keys mean donut and grinder.',
 'See REPORT.md for unavailable states and unpromoted effect candidates.']}
sources={};outputs={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wiki(name):
 r=selected[name];p=meta[r['title'].replace(' ','_')];i=p['imageinfo'][0];w=p['revisions'][0]['slots']['main']['*'];
 return {'url':r['descriptionurl'],'imageUrl':r['url'],'game':'New Super Mario Bros. U' if name.startswith('NSMBU') else ('Super Mario Maker 2 (NSMBU style)' if name.startswith('SMM2') else 'Super Mario Maker (NSMBU style)'), 'ripper':f"Mario Wiki uploader {i['user']}; original ripper not identified in file metadata",'method':'Original image downloaded by headless Playwright Chromium; lossless RGBA extraction, no enlargement.','sourceSummary':w.split('== Licensing')[0].split('==Licensing')[0].strip()}
def source_record(path,frame=0,decimate=1,rect=None):
 path=Path(path);key=path.relative_to(ROOT).as_posix()
 sources[key]={'path':key,'sha256':sha(path),'size':list(Image.open(path).size)}
 return {'path':key,'sourceFrame':frame,'decimate':decimate,'rect':rect}
def read(record):
 im=Image.open(ROOT/record['path']);im.seek(record['sourceFrame']);im=im.convert('RGBA');d=record['decimate']
 if d!=1:
  assert im.width%d==0 and im.height%d==0
  # Assert source enlargement, rather than estimating it from dimensions.
  px=im.load()
  for y in range(0,im.height,d):
   for x in range(0,im.width,d):
    assert all(px[x+dx,y+dy]==px[x,y] for dy in range(d) for dx in range(d)),(record['path'],x,y)
  im=im.resize((im.width//d,im.height//d),Image.Resampling.NEAREST)
 if record.get('resize'):
  w,h=record['resize'];assert w<=im.width and h<=im.height,'No enlargement'
  im=im.resize((w,h),Image.Resampling.NEAREST)
 if record['rect']:
  x,y,w,h=record['rect'];assert x>=0 and y>=0 and x+w<=im.width and y+h<=im.height
  im=im.crop((x,y,x+w,y+h))
 return im

def entry(key,animation_specs,source,display,anchor=(.5,.5),note='',missing=()):
 """Specs contain original source references, never synthesized keyframes."""
 unique=[]
 for _,refs,_,_ in animation_specs:
  for ref in refs:
   if ref not in unique:unique.append(ref)
 decoded=[read(r) for r in unique];w=max(im.width for im in decoded);h=max(im.height for im in decoded)
 # Centre/bottom only pads genuine native pixels to one consistent canvas.
 prefix=key.replace('.','/');files=[]
 for idx,(r,im) in enumerate(zip(unique,decoded)):
  f=Image.new('RGBA',(w,h));at=((w-im.width)//2,h-im.height);f.paste(im,at)
  rel=f'{prefix}/{idx:03d}.png';out=HERE/rel;out.parent.mkdir(parents=True,exist_ok=True);f.save(out,optimize=True)
  files.append(rel);outputs[rel]={'source':r,'offset':list(at),'canvas':[w,h],'sha256':sha(out)}
 anims={}
 for name,refs,fps,extras in animation_specs:
  anims[name]={'frames':[files[unique.index(r)] for r in refs],'frameRate':fps,'kind':'still' if len(refs)==1 else 'animation',**extras}
 e={'manifestKey':key,'path':files[0],'anims':anims,'anchor':{'x':anchor[0],'y':anchor[1]},'displaySize':{'w':display[0],'h':display[1]},'source':source,'canvas':{'w':w,'h':h},'note':note,'missingAnimations':list(missing)}
 section,name=key.split('.');manifest[section][name]=e

def wr(name,frame=0,rect=None):return source_record(RAW/name,frame,rect=rect)
def still(key,name,display,anim='idle',note='',missing=(),anchor=(.5,.5)):
 entry(key,[(anim,[wr(name)],0,{})],wiki(name),display,anchor,note,missing)
def scratch(sprite_name,project):
 data=json.loads((OLD/f'scratch-{project}.json').read_text());targets=data.get('targets',data.get('children',[]));t=next(x for x in targets if x.get('name',x.get('objName'))==sprite_name)
 refs=[]
 for c in t['costumes']:
  md5=c.get('md5ext',c.get('baseLayerMD5'));p=RAW/'scratch'/str(project)/md5
  if not p.exists():
   p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(urllib.request.urlopen('https://assets.scratch.mit.edu/internalapi/asset/'+md5+'/get/',timeout=25).read())
  refs.append(source_record(p,decimate=2))
 return refs,{'url':f'https://scratch.mit.edu/projects/{project}/','game':'Super Mario Maker (NSMBU style), collection labelled NSMBU','ripper':'Random Talking Bush (credited in MarioTheBest project notes); image collection shared by MarioTheBest','method':'Extract PNG image costumes only; no Scratch code reused. Verify exact 2x2 pixel replication and decimate by 2 to restore native pixels. Original costume order preserved. Playback rate is a chosen presentation rate, not a verified game clock.'}

still('elements.spring','SMM-NSMBU-Spring.png',(1,1),note='Genuine normal-state still; compressed and extended source states unavailable.',missing=['compress','extend'],anchor=(.5,1))
still('elements.checkpoint','SMM-NSMBU-Checkpoint-Flag.png',(1.25,2.02),note='Inactive Bowser checkpoint only. No invented recoloured Mario flag.',missing=['active'],anchor=(.5,1))
still('elements.goal','NSMBU_Flagpole.png',(1.54,5),note='Native tall pole and Mario flag still. No wave loop supplied.',missing=['wave'],anchor=(.5,1))
still('elements.brick','NSMBU_Ground_Big_Brick_Block.png',(1,1),note='Native 120px Mega Block sprite down-displayed to a one-tile brick; no resize in source files.')
q,qs=scratch('NSMBU Question Block',105789235)
used=dict(wr('NSMBU_Ground_Big_Empty_Block.png'),resize=[64,64])
entry('elements.question_block',[('idle',q,20,{}),('used',[used],0,{})],qs,(1,1),note='16 genuine native 64px question-symbol scroll frames. Used state is Mario Wiki native Big Empty Block; see per-frame source lock. No captured bump poses.',missing=['bump'])
entry('elements.pswitch',[('idle',[wr('SMM2-NSMBU-PSwitch.gif',i) for i in range(12)],12000/820,{'frameDurationsMs':[80,60,60,100,60,60,60,60,60,100,60,60]})],wiki('SMM2-NSMBU-PSwitch.gif'),(1,1),(.5,1),'Real P-switch highlight cycle; this GIF never depresses. Existing pack key pswitch corresponds to requested p_switch.',missing=['pressed'])
entry('elements.switch', [('idle',[wr('SMM2-NSMBU-OnSwitch.png')],0,{}),('on',[wr('SMM2-NSMBU-OnSwitch.png')],0,{}),('off',[wr('SMM2-NSMBU-OffSwitch.png')],0,{})],wiki('SMM2-NSMBU-OnSwitch.png'),(1,1),note='Two genuine still states, not an invented interpolated transition. OFF image source is separately pinned.')
entry('elements.switch_block',[(n,[wr(f'SMM2-NSMBU-{f}.png')],0,{}) for n,f in [('idle','RedBlock'),('on','RedBlock'),('off','RedDottedLineBlock'),('blue_on','BlueBlock'),('blue_off','BlueDottedLineBlock')]],wiki('SMM2-NSMBU-RedBlock.png'),(1,1),note='Solid and dotted red/blue still states. Not a flashing animation.')
still('elements.falling_block','SMM-NSMBU-DonutBlock.png',(1,1),note='Donut idle only; shake is gameplay movement, no fabricated sprite cycle.',missing=['shake'])
still('elements.saw','SMM-NSMBU-Grinder.png',(1.5,1.5),note='149px captured grinder still. No pre-rotated frames manufactured.',missing=['spin'])
d,ds=scratch('NSMBU Door Costume 1',105733943)
entry('elements.door',[('closed',[d[0]],0,{}),('open',d[:6],20,{'repeat':0}),('close',[d[5]]+d[6:]+[d[0]],20,{'repeat':0})],ds,(1,2),(.5,1),'Actual six-position opening cycle and original closing poses. No warping or generated in-between frames.')
still('elements.pipe','SMM-NSMBU-WarpPipe.png',(2,2),note='Native 120px pipe, displayed at 128px (1.067x; below 1.25x limit).')
still('elements.cannon','SMM-NSMBU-BillBlaster.png',(1,2),note='Bill Blaster idle still. Fire smoke candidate in ignored research has unverified rip attribution and is not integrated.',missing=['fire'])
conv,cs=scratch('NSMBU Belt Costume 1',105789235)
# Costume centres vary; select an aligned, native one-tile middle segment.
centres=[186,186,184,182,176,182,184,186]
conv=[dict(r,rect=[x//2-32,0,64,57]) for r,x in zip(conv,centres)]
entry('elements.conveyor_belt',[('idle',conv,16,{}),('scroll',conv,16,{})],cs,(1,57/64),note='Eight genuine scroll frames. Restore exact native pixels, then crop aligned 64x57 centre segments; no belt translated to synthesize frames.')
entry('elements.mushroom',[('idle',[wr('SMM-NSMBU-Mushroom.gif',i) for i in range(16)],20,{})],wiki('SMM-NSMBU-Mushroom.gif'),(1,1),(.5,1),'Genuine 16-frame wobble cycle, not an emerge capture. Emerge motion must be supplied by gameplay.',missing=['emerge'])
coin=[wr('NSMBUCoin.gif',i) for i in range(16)]
entry('fx.coin_pop',[('idle',coin,20,{}),('spin',coin,20,{})],wiki('NSMBUCoin.gif'),(.75,.875),note='Actual 16-frame coin spin usable as the sprite of a coin-pop effect. Pop trajectory is renderer movement; no captured rise/burst claimed.')
star,ss=scratch('NSMBU Starman',105789235)
entry('fx.star',[('idle',star,20,{})],ss,(.75,.8),note='Actual 21-frame Super Star wobble, usable as a decorative star effect. This is the power-up sprite, not an invincibility-particle rip.')
# These four source cells are actual separate rock/brick fragments in the game's tile sheet.
tile=OLD/'tiles/21847-0.png';s=next(x for x in LOCK if x['file']=='tiles/21847-0.png')
refs=[source_record(tile,rect=[x*64,320,64,64]) for x in range(4)]
entry('fx.brick_debris',[(f'piece_{i}',[r],0,{}) for i,r in enumerate(refs)],{'url':s['url'],'game':'Super Mario Maker 2 (NSMBU tileset)','ripper':'Original ripper not credited by smm2viewer mirror','method':'Lossless crop of four actual debris cells from pinned native tileset. Pieces are independent static particle variants, never played as an animation.'},(.45,.45),note='Four native fragment variants; select a piece for each particle. No brick was quartered or hand-painted to invent debris.')
# Include additional source metadata for every wiki file used by mixed-source states.
(HERE/'source-lock.json').write_text(json.dumps({'schema':1,'sources':sources,'wikiSources':{n:wiki(n) for n in selected},'outputs':outputs},indent=2)+'\n')
(HERE/'objects.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f"Prepared {len(manifest['elements'])} object entries, {len(manifest['fx'])} fx entries, {len(outputs)} PNG files.")
