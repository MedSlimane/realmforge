"""Create the checked-in exact slicing configuration from reviewed native images."""
from pathlib import Path
from PIL import Image
import json
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[2];RAW=ROOT/'assets/_downloads/mario'
sources=json.loads((HERE/'sources.json').read_text());groups={}
for s in sources:
 if s.get('sprite'):groups.setdefault(s['sprite'],[]).append(s)
for g in groups.values():g.sort(key=lambda x:x['index'])
for key in ['koopa','shell','chain','chainchomp','spiny','qblock','noteblock','cinta_middle','star','bulletbill','door']:
 if 'hq_'+key in groups:groups['spr_NSMBU_'+key]=groups['hq_'+key]
# The native Koopa sheet also contains prone poses after its first 20 walk frames.
groups['spr_NSMBU_koopa']=[s for s in groups['spr_NSMBU_koopa'] if s['index']<20]
config={'sourceTile':64,'assets':{},'characters':{},'enemies':{},'themes':{}}
def refs(name,limit=None):
 name=name if name.startswith(('spr_','bg_')) else 'spr_NSMBU_'+name
 a=[]
 for s in groups[name][:limit]:
  im=Image.open(RAW/s['file']).convert('RGBA');box=im.getchannel('A').getbbox();x,y,r,b=box
  a.append({'source':s['file'],'rect':[x,y,r-x,b-y]})
 return a
def tile(theme,x,y,w=1,h=1):return {'source':f'tiles/21847-{theme}.png','rect':[x*64,y*64,w*64,h*64]}
def add(id,path,frames,animations=None,display=None,anchor=None,note=None):
 config['assets'][id]={'path':path,'frames':frames}
 if animations:config['assets'][id]['animations']=animations
 if display:config['assets'][id]['displaySize']=dict(zip(('w','h'),display))
 if anchor:config['assets'][id]['anchor']=dict(zip(('x','y'),anchor))
 if note:config['assets'][id]['note']=note

def simple(id,folder,source,display=(1,1),animation='idle',note=None):
 frames=refs(source);add(id,f'{folder}/{id}.png',frames,{animation:list(range(len(frames)))},display,(.5,1) if folder=='enemies' else (.5,.5),note)
for id,n in [('spikes','pinchos'),('lava','lava'),('falling_block','donut')]:simple(id,'hazards',n,note='Donut Block represents the falling-block mechanic.' if id=='falling_block' else None)
im=Image.open(RAW/'grinder.png');add('saw','hazards/saw.png',[{'source':'grinder.png','rect':[0,0,*im.size]}],display=(1,1))
add('crate','dynamic/crate.png',[tile(0,5,0)],display=(1,1),note='Native used/throw block represents the pushable crate; no native NSMBU crate was found.')
for id,n in [('spring','spring'),('spring_extended','spring'),('conveyor_belt','cinta_middle'),('chain_link','chain'),('pendulum_ball','chainchomp'),('seesaw','platform_seesaw'),('moving_platform','platform'),('elevator','platform'),('rotating_platform','platform_seesaw')]:
 simple(id,'moving' if id in ('moving_platform','elevator','rotating_platform') else 'dynamic',n,(1,1),note={'pendulum_ball':'Chained Chain Chomp ball represents a wrecking ball; chain_link is provided separately.','elevator':'Native lift segment reused for the elevator.','rotating_platform':'Native seesaw deck reused for the rotator.'}.get(id))
# Spring compression and extension use actual native poses.
# Middle segment of the 3-tile native conveyor, without squashing the full belt.
for r in config['assets']['conveyor_belt']['frames']:
 x,y,w,h=r['rect'];r['rect']=[x+(w-128)//2,y,128,h]
config['assets']['chain_link']['displaySize']={'w':.25,'h':.25}
# The three native lift frames are left/middle/right parts, not animation frames.
parts=[]
for i,r in enumerate(refs('platform')[:3]):
 r={**r,'rect':[r['rect'][0],r['rect'][1],16,8]};parts.append({'frame':r,'at':[i*16,0]})
lift={**refs('platform')[0],'compose':{'canvas':[48,8],'parts':parts}}
for id in ['moving_platform','elevator']:
 config['assets'][id].update(frames=[lift],animations={'idle':[0]},displaySize={'w':3,'h':.5})
config['assets']['spring']['frames']=refs('spring')+refs('spring_end')
config['assets']['spring']['animations']={'idle':[0],'bounce':list(range(len(config['assets']['spring']['frames']))),'move':list(range(len(config['assets']['spring']['frames'])))}
add('chain_bridge','dynamic/chain_bridge.png',[tile(0,1,3)],display=(1,1),note='Native rope bridge plank segment; chain_link is supplied for the constraint chain.')
for id,n in [('coin','coin'),('coin_side','coin'),('big_coin','coin_10'),('key','key'),('powerup_double_jump','superacorn'),('powerup_dash','star')]:simple(id,'items',n,note={'powerup_double_jump':'Super Acorn represents double jump.','powerup_dash':'Super Star represents dash.'}.get(id))
config['assets']['coin_side']['frames']=[refs('coin')[len(refs('coin'))//2]]
config['assets']['coin_side']['animations']={'idle':[0]}
for id,n in [('start','arrow_start_hd'),('checkpoint','checkpoint'),('checkpoint_active','checkpoint_mario'),('door','door'),('door_open','door_close'),('locked_door','doorlock_anim'),('switch','pswitch'),('switch_on','pswitch'),('switch_block','onoffblock_on')]:simple(id,'flow',n,(1,2) if id in ('door','door_open','locked_door') else (1,1))
config['assets']['switch_on']['frames']=[refs('pswitch')[-1]]
config['assets']['switch_on']['animations']={'idle':[0]}
# ON/OFF switch and toggled blocks at full native 64px resolution.
config['assets']['switch'].update(frames=[tile(0,2,23)],animations={'idle':[0]})
config['assets']['switch_on'].update(frames=[tile(0,3,23)],animations={'idle':[0]})
config['assets']['switch_block'].update(frames=[tile(0,2,21)],animations={'idle':[0]})
add('switch_block_off','flow/switch_block_off.png',[tile(0,2,22)],display=(1,1))
simple('pswitch','flow','pswitch')
# Goal is a native pole + flag + brick base, composed without redrawing.
for id,flag in [('goal','flag_bowser'),('goal_wave','flag_mario')]:
 pole=refs('flagpole',1)[0];frame={**pole,'compose':{'canvas':[48,171],'parts':[{'frame':pole,'at':[16,0]},{'frame':refs(flag,1)[0],'at':[18,16]},{'frame':refs('flag_base',1)[0],'at':[8,153]}]}}
 add(id,f'flow/{id}.png',[frame],display=(1.4,5),anchor=(.5,1))
add('pipe','flow/pipe.png',[tile(0,14,0,2,2)],display=(2,2),anchor=(.5,1))
add('hard_block','tiles/shared/hard_block.png',[tile(0,5,0)],display=(1,1))
add('used_block','tiles/shared/used_block.png',[tile(0,5,0)],display=(1,1))
add('ice','tiles/shared/ice.png',[tile(0,8,7)],display=(1,1))
add('slime','tiles/shared/slime.png',[tile(0,4,0)],display=(1,1),note='Native Note Block is the visual substitute for high-friction slime; physics stays slime.')
for theme,index in [('grass',0),('desert',7),('snow',6),('castle',2)]:
 coords={'ground':(1,12),'top':(1,12),'top_left':(0,12),'top_right':(3,12),'fill':(5,12),'left':(6,12),'right':(8,12),'bottom':(5,13),'brick':(1,0),'question':(2,0),'one_way':(1,3),'semi_solid':(4,2),'hard_block':(5,0),'used_block':(5,0),'ice':(8,7),'slime':(4,0)}
 for variant,(x,y) in coords.items():
  id=f'{theme}_{variant}';add(id,f'tiles/{theme}/{id}.png',[tile(index,x,y)],display=(1,1))
 # Actual animated question block, retaining 64px first image for native terrain grid.
 config['assets'][f'{theme}_question']['animationSources']=refs('qblock')
 original={'grass':'overworld','desert':'desert','snow':'snow','castle':'castle'}[theme]
 names=[n for n in groups if n.startswith(f'bg_NSMBU_{original}_')]
 # The foreground tree is supplied with all other original layers; native full-height alignment stays intact.
 layers=[]
 for n in names:
  s=groups[n][0];im=Image.open(RAW/s['file']);layers.append({'source':s['file'],'rect':[0,0,*im.size],'file':f'backgrounds/{theme}/{n.removeprefix("bg_NSMBU_")}.png','scrollFactor':round(.06+len(layers)*.065,3)})
 config['themes'][theme]={'layers':layers}
# Enemies keep native poses and feet anchors. Flyer's wings are composited from the native wing frames.
for id,n in [('walker','goomba'),('shell','koopa'),('flyer','koopa_fly'),('jumper','spiny'),('cannon','bullebill_base')]:
 f=refs(n);an={'idle':[0],'move':list(range(len(f)))}
 if id=='walker':an['stomp']=[len(f)];f+=refs('goomba_stomped',1)
 if id=='shell':
  an['walk']=list(range(len(f)));start=len(f);f+=refs('shell');an['idle']=[start];an['kick']=list(range(start,len(f)));an['spin']=an['kick']
 if id=='jumper':an['jump']=list(range(len(f)))
 if id=='flyer':
  wings=refs('wings_enemigos')
  f=[{**r,'compose':{'canvas':[48,40],'parts':[{'frame':wings[i%len(wings)],'at':[14,1]},{'frame':r,'at':[16,8]}]}} for i,r in enumerate(f)]
 add(id,f'enemies/{id}.png',f,an,(1,1.5) if id=='shell' else (1,1),(.5,1));config['enemies'][id]=id
simple('bullet_bill','enemies','bulletbill')
# Keep a constant native-size flyer canvas while using the larger authentic Koopa rip.
# The native low-resolution wing capture is supplied with the original flyer poses.
config['assets']['seesaw']['displaySize']={'w':5,'h':.875}
config['assets']['rotating_platform']['displaySize']={'w':5,'h':.875}
config['assets']['door']['frames']=[refs('door')[0]]
config['assets']['door']['animations']={'idle':[0]}
config['assets']['door_open']['frames']=[refs('door')[5]]
config['assets']['door_open']['animations']={'idle':[0]}
# Both native Mario forms. Luigi big is explicitly a colour substitution, not passed off as a native Luigi rip.
for name,size in [('mario','big'),('mario_small','small'),('luigi','big')]:
 frames=[];an={}
 for a,n in [('idle','idle'),('walk','walk'),('run','run'),('skid','skid'),('jump','jump1'),('fall','jump1'),('crouch','crouch'),('wallSlide','wall_slide'),('dead','dead1')]:
  f=refs(f'mario_{size}_{n}')
  if a=='fall':f=f[-2:]
  if a=='crouch':f=f[-2:]
  an[a]=list(range(len(frames),len(frames)+len(f)));frames+=f
 add(name,f'characters/{name}/idle.png',frames,an,None,(.5,1), 'Luigi colour variant of the big Mario capture; native Luigi walk is separately supplied as luigi_native_walk.' if name=='luigi' else None)
 config['assets'][name]['characterHeight']=1 if size=='small' else 2
 if name=='luigi':config['assets'][name]['recolor']='luigi'
 config['characters'][name]=name
simple('luigi_native_walk','characters','luigi_walk',(1,2),'walk',note='Native Luigi walk capture only; additional authentic Luigi poses were not available.')
config['characters']['luigi_native_walk']='luigi_native_walk'
(HERE/'slicing.json').write_text(json.dumps(config,indent=2)+'\n')
print(f'Curated {len(config["assets"])} assets, {sum(len(v["frames"]) for v in config["assets"].values())} exact source rectangles, {sum(len(t["layers"]) for t in config["themes"].values())} background layers.')
