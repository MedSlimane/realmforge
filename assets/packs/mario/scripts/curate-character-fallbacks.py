"""Transparent same-style native Wii captures; explicitly not mislabelled as NSMBU.
Exact NSMBU Luigi + small-Mario HD pose coverage remains a documented limitation.
"""
from pathlib import Path
from PIL import Image
import json,copy
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[2];RAW=ROOT/'assets/_downloads/mario'
c=json.loads((HERE/'slicing.json').read_text())
def costumes(id):
 d=json.loads((RAW/f'hires/scratch-{id}.json').read_text());return {v['name']:v for t in d['targets'] if not t.get('isStage') for v in t['costumes']}
def make(id,project,poses,height):
 cs=costumes(project);frames=[];anims={}
 for name,names in poses.items():
  anims[name]=list(range(len(frames),len(frames)+len(names)))
  for n in names:
   f=f'hires/scratch/{project}/'+cs[n]['md5ext'];im=Image.open(RAW/f).convert('RGBA');x,y,r,b=im.getbbox();frames.append({'source':f,'rect':[x,y,r-x,b-y]})
 c['assets'][id]={'path':f'characters/{id}/idle.png','frames':frames,'animations':anims,'characterHeight':height,'anchor':{'x':.5,'y':1},'note':f'Authentic NSMB Wii raster captures shared by PolskyGamer (project {project}); same-style fallback, NOT an NSMBU rip. '+('Original ripper credited as Keira Sanchez. ' if id=='mario_small' else 'Original ripper not stated by this collection. ')+'Distinct Fall capture; wallSlide holds the wall-jump capture. '+('Skid reuses a run-transition pose; a separate braking capture was not found.' if id.startswith('luigi') else '')}
 c['characters'][id]=id
for form,prefix,h in [('luigi','Big',1.875),('luigi_small','Small',.9375)]:
 poses={'idle':[f'{prefix}LuigiIdle{i}' for i in [1,5,10]],'walk':[f'{prefix}LuigiWalk{i}' for i in [1,5,9]],'run':[f'{prefix}LuigiRun{i}' for i in [1,4,7]],'skid':[f'{prefix}LuigiRun4'],'jump':[f'{prefix}LuigiJump{i}' for i in [1,8,15]],'fall':[f'{prefix}LuigiFall'],'crouch':[f'{prefix}LuigiDuck4'],'wallSlide':[f'{prefix}Luigi'+('WalJump1' if prefix=='Big' else 'WallJump1')],'dead':['LuigiDead1','LuigiDead7','LuigiDead14']}
 make(form,797092569,poses,h)
make('mario_small',784192278,{'idle':['SmallIdle1','SmallIdle9','SmallIdle17'],'walk':['Walk1','Walk9','Walk17'],'run':['Run1','Run5','Run9'],'skid':['Skid1','Skid2'],'jump':['Jump1','Jump8','Jump15'],'fall':['Fall'],'crouch':['Duck1'],'wallSlide':['WallJump1'],'dead':['Dead1','Dead10']},.9375)
# Keep the existing helper key as an alias of the new authentic capture atlas.
c['characters']['luigi_native_walk']='luigi';c['assets'].pop('luigi_native_walk',None)
# NSMBU big captures have mixed source facing directions; normalize to right.
# Extracted pose ordering comes from curate-hires.py.
for i in [0,1,2,11,14,15]:c['assets']['mario']['frames'][i]['flipX']=True
(HERE/'slicing.json').write_text(json.dumps(c,indent=2)+'\n')
print('Recorded real Luigi big/small + real small Mario; exact-game and skid caveats retained in entry notes.')
