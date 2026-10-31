"""Build the 47 legal blob masks from native 30px quadrants; never paint new art."""
from pathlib import Path
import json,copy
HERE=Path(__file__).resolve().parents[1]
c=json.loads((HERE/'slicing.json').read_text())
for theme,t in c['themes'].items():
 # Strip prior generated masks to make repeated curation idempotent.
 t['variants']={n:id for n,id in t['variants'].items() if not n.startswith('mask_')}
 for mask in range(256):
  n,e,s,w=(bool(mask&b) for b in [1,2,4,8])
  if any(bool(mask&b) and not(a and z) for b,a,z in [(16,n,e),(32,e,s),(64,s,w),(128,w,n)]):continue
  parts=[]
  for corner,a,b,diag,x,y in [('top_left',n,w,128,0,0),('top_right',n,e,16,30,0),('bottom_left',s,w,64,0,30),('bottom_right',s,e,32,30,30)]:
   vertical='top' if y==0 else 'bottom';horizontal='left' if x==0 else 'right'
   name=corner if not a and not b else vertical if not a else horizontal if not b else 'inner_'+corner if not mask&diag else 'fill'
   r=copy.deepcopy(c['assets'][t['variants'][name]]['frames'][0]);r['rect']=[r['rect'][0]+x,r['rect'][1]+y,30,30]
   parts.append({'frame':r,'at':[x,y]})
  id=f'{theme}_mask_{mask}';r=parts[0]['frame'];c['assets'][id]={'path':f'tiles/{theme}/{id}.png','frames':[{'source':r['source'],'rect':r['rect'],'compose':{'canvas':[60,60],'parts':parts}}],'displaySize':{'w':1,'h':1},'anchor':{'x':.5,'y':.5},'note':'47-mask autotile assembled from native 30px quadrants; no upsampling.'};t['variants'][f'mask_{mask}']=id
(HERE/'slicing.json').write_text(json.dumps(c,indent=2)+'\n')
print('Completed 47 legal blob masks per theme, plus named cardinal/inner/pillar/single variants.')
