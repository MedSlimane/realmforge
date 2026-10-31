"""Record the high-resolution curation. Build uses slicing.json, not this research helper.
Only Nintendo imagery is extracted; no source project code is executed or reused.
"""
from pathlib import Path
from PIL import Image
import json,copy,re,base64,io,hashlib
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[2];RAW=ROOT/'assets/_downloads/mario'
c=json.loads((HERE/'slicing.json').read_text());assets=c['assets']

def ref(file,rect=None,resize=None,**extra):
 im=Image.open(RAW/file).convert('RGBA')
 if rect is None:
  x,y,r,b=im.getbbox();rect=[x,y,r-x,b-y]
 out={'source':file,'rect':rect,**extra}
 if resize:out['resize']=resize
 return out

def asset(id,file=None,frames=None,size=(1,1),note=None):
 old=assets.get(id,{})
 a={'path':old.get('path',('items/' if id=='mushroom' else 'dynamic/')+id+'.png'),'frames':frames or [ref(file)],'displaySize':{'w':size[0],'h':size[1]},'anchor':old.get('anchor',{'x':.5,'y':.5})}
 if note:a['note']=note
 assets[id]=a;return a

def mi(n):return 'hires/miyamoto/miyamotodata/sprites/'+n+'.png'
def wiki(n):return 'hires/wiki/'+n+'.png'
def parts(frames,canvas,positions):
 return {'source':frames[0]['source'],'rect':frames[0]['rect'],'compose':{'canvas':canvas,'parts':[{'frame':f,'at':p} for f,p in zip(frames,positions)]}}

asset('crate',mi('reg_box_2x2'),note='Authentic NSMBU wooden crate, Miyamoto image collection (no editor code reused).')
# Use the ball alone; the chain and its anchor remain separate render components.
asset('pendulum_ball',frames=[ref(mi('pendulum_0'),[5,240,140,145])],note='Native NSMBU spiked pendulum ball, cropped from pendulum_0; replaces Chain Chomp.')
asset('seesaw_pivot',mi('seesaw_mushroom_pivot'),size=(.75,.75))
plank=[ref(mi('seesaw_mushroom_left')),ref(mi('seesaw_mushroom_middle')),ref(mi('seesaw_mushroom_middle')),ref(mi('seesaw_mushroom_middle')),ref(mi('seesaw_mushroom_right'))]
# Native segments are 60x60; the upper half forms the thick deck, lower half is stem art.
for f in plank:f['rect']=[0,0,60,30]
for id in ['seesaw','rotating_platform']:
 asset(id,frames=[parts(plank,[300,30],[[i*60,0] for i in range(5)])],size=(5,.5),note='Five native 60px NSMBU mushroom-seesaw deck segments. Pivot is a separate seesaw_pivot entry.')
for id in ['moving_platform','elevator']:
 fs=[ref(mi('wood_platform_left'),[0,0,75,30]),ref(mi('wood_platform_middle'),[0,0,60,30]),ref(mi('wood_platform_right'),[0,0,75,30])]
 asset(id,frames=[parts(fs,[210,30],[[0,0],[75,0],[135,0]])],size=(3,.5))
asset('falling_block',mi('donut_lift'))
asset('spring',mi('springboard'));asset('spring_extended',mi('springboard'))
asset('cannon',mi('bullet_bill_cannon'),frames=[ref(mi('bullet_bill_cannon'),[0,0,60,60])])
asset('walker',wiki('goomba'),frames=[ref(wiki('goomba'),resize=[104,122])],note='Native NSMBU Goomba render from Super Mario Wiki. Static pose; no fabricated walk/stomp frames.')
assets['walker']['animations']={'walk':[0],'stomp':[0]}
asset('flyer',mi('paragoomba'),note='Authentic NSMBU Paragoomba replaces low-resolution composite Koopa + wings.')
assets['flyer']['animations']={'fly':[0]}
asset('powerup_double_jump',wiki('acorn'),frames=[ref(wiki('acorn'),resize=[174,199])])
asset('mushroom',wiki('mushroom'),frames=[ref(wiki('mushroom'),resize=[128,127])],note='Official NSMBU Super Mushroom artwork. Form behavior is implemented in game-core.')
asset('coin',wiki('coin'),frames=[ref(wiki('coin'),resize=[128,167])])
assets['coin']['animations']={'idle':[0]}
asset('coin_side',frames=[ref('hires/wiki/coin.gif',[0,0,52,60],sourceFrame=3)])
asset('big_coin',mi('star_coin'))
asset('pswitch',mi('p_switch_u'))
asset('checkpoint',mi('midway_flag'))
asset('checkpoint_active',mi('midway_flag'),note='Native checkpoint pole; same flag design pending an authentic activated-state render.')
asset('locked_door',frames=copy.deepcopy(assets['door']['frames']),size=(1,2),note='Native closed door, with the separately supplied key indicating lock state in gameplay.')
asset('goal',mi('flag_pole'),size=(1.4,5));asset('goal_wave',mi('flag_pole'),size=(1.4,5))
# The key is a 60px NSMBU tile-sheet icon (not a 16px mirror capture).
asset('key',frames=[ref(wiki('key'),[0,0,60,60])])
# Preserve native question animation, upgrading its static image too. Brick/used artwork is
# official artwork reused in NSMBU (source labels identify the original earlier games).
for theme in ['grass','desert','snow','castle']:
 for typ in ['brick','question','used_block','hard_block']:
  src='used' if typ in ['used_block','hard_block'] else typ
  a=asset(f'{theme}_{typ}',frames=[ref(wiki(src),resize=[128,128])])
  a['note']='Official block artwork from the NSMBU gallery; earlier-game artwork reused in NSMBU. Perspective artwork, not an untouched game texture.'
 for typ in ['slime']:
  asset(f'{theme}_{typ}',frames=[ref(mi('green_mushroom_middle'))],note='NSMBU green mushroom-platform surface stands for sticky terrain; no native NSMBU slime/jelly rip found.')
for id in ['used_block','hard_block']:
 asset(id,frames=[ref(wiki('used'),resize=[128,128])])
asset('slime',mi('green_mushroom_middle'),note='NSMBU green mushroom-platform surface represents high-friction slime.')
# Each source cell has a 60px content region and 2px repeated edge padding.
# Previous left/right/fill crops accidentally selected underside/slope cells.
variants={'ground':(1,12),'top':(1,12),'top_left':(2,15),'top_right':(4,15),'fill':(5,12),'inner':(5,12),'left':(10,12),'right':(11,12),'bottom':(9,15),'bottom_left':(8,15),'bottom_right':(10,15),'pillar_top':(4,13),'pillar':(5,13),'pillar_bottom':(6,13),'single':(0,13),'horizontal':(2,13),'single_left':(1,13),'single_right':(3,13),'inner_top_left':(1,14),'inner_top_right':(0,14),'inner_bottom_left':(7,13),'inner_bottom_right':(8,13)}
for theme,index in [('grass',0),('desert',7),('snow',6),('castle',2)]:
 c['themes'][theme]['variants']={}
 for name,(x,y) in variants.items():
  id=f'{theme}_{name}';asset(id,frames=[ref(f'tiles/21847-{index}.png',[x*64+2,y*64+2,60,60])]);c['themes'][theme]['variants'][name]=id
 # Preserve actual platform appearance for the theme; remove source-cell padding.
 for typ in ['one_way','semi_solid','ice']:
  a=assets[f'{theme}_{typ}'];r=a['frames'][0]['rect'];a['frames'][0]['rect']=[r[0]+2,r[1]+2,60,60]
asset('ice',frames=[ref('tiles/21847-0.png',[514,450,60,60])])
# A one-tile tiled spike strip from the native NSMBU spike pillar (not its tiny icon).
asset('spikes',frames=[ref(mi('spike_pillar_up'),[0,0,240,60],resize=[120,30])],size=(1,.5))
# Native lava textures contain more than enough pixels for one tile.
asset('lava',frames=[ref(mi('liquid_lava'),[0,0,128,128])])
# Native rope bridge module remains a 60px tile.
assets['chain_bridge']['frames']=[ref('tiles/21847-0.png',[66,194,60,60])]
# NSMBU Mario: extract the original embedded raster, never rasterize or trace the SVG.
file='hires/scratch/839078033/b6230b64e7270d4fc48fe43b3c08fc27.svg'
encoded=re.findall(rb'data:image/[^;]+;base64,([^"\s]+)',(RAW/file).read_bytes())
def mario_frame(i,h):
 im=Image.open(io.BytesIO(base64.b64decode(encoded[i])));w=round(im.width*h/im.height);return {'source':file,'embeddedImage':i,'rect':[0,0,im.width,im.height],'resize':[w,h]}
poses={'idle':[(0,160),(2,160),(4,160)],'walk':[(11,160),(12,160),(13,160),(14,160)],'run':[(59,160),(60,160),(63,160),(64,160)],'skid':[(44,150)],'jump':[(55,150),(56,160)],'fall':[(45,160),(48,160)],'crouch':[(68,96)],'wallSlide':[(35,160)],'dead':[(33,160)]}
frames=[];anims={}
for name,seq in poses.items():
 anims[name]=list(range(len(frames),len(frames)+len(seq)));frames += [mario_frame(i,h) for i,h in seq]
a=asset('mario',frames=frames);a.pop('displaySize');a['characterHeight']=1.875;a['animations']=anims;a['anchor']={'x':.5,'y':1};a['note']='NSMBU raster captures credited to PolskyGamer, Scratch project 839078033. Cropped extracted PNGs; pose scales normalized only by downsampling. Distinct fall capture.'
(HERE/'slicing.json').write_text(json.dumps(c,indent=2)+'\n')
print(f'Curated {len(assets)} source assets; source lock updated separately.')
