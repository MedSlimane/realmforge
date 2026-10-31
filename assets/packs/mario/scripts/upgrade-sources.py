"""Curate full-resolution Nintendo rip frames from credited shared collections.
The project payloads are research-only raw downloads; no Scratch scripts are reused.
"""
from pathlib import Path
import json,urllib.request,concurrent.futures,hashlib,time
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[2];RAW=ROOT/'assets/_downloads/mario'
sources=json.loads((HERE/'sources.json').read_text())
selection={105733943:{'NSMBU Bullet Bill':'bulletbill','NSMBU Door Costume 1':'door','NSMBU Cannon':'cannon'},105789235:{'NSMBU Question Block':'qblock','NSMBU Note Block':'noteblock','NSMBU Belt Costume 1':'cinta_middle','NSMBU Starman':'star'},107756944:{'NSMBU Green Koopa':'koopa','NSMBU Green Koopa Shell':'shell','NSMBU Chain Chomp Chain':'chain','NSMBU Chain Chomp':'chainchomp','NSMBU Spiny':'spiny'}}
jobs=[]
for id,chosen in selection.items():
 data=json.loads((RAW/f'scratch-{id}.json').read_text());targets=data.get('targets',data.get('children',[]))
 for t in targets:
  name=t.get('name',t.get('objName'))
  if name not in chosen:continue
  costumes=t['costumes'];indices=list(range(len(costumes))) if len(costumes)<=16 else sorted(set(round(i*(len(costumes)-1)/11) for i in range(12)))
  for i in indices:
   c=costumes[i];md5=c.get('md5ext',c.get('baseLayerMD5'));assert md5.endswith('.png'),md5
   jobs.append((id,chosen[name],i,md5))
def get(job):
 id,name,i,md5=job;f=f'scratch/{id}/{md5}';p=RAW/f;p.parent.mkdir(parents=True,exist_ok=True);u='https://assets.scratch.mit.edu/internalapi/asset/'+md5+'/get/'
 if not p.exists():
  for attempt in range(6):
   try:p.write_bytes(urllib.request.urlopen(u,timeout=30).read());break
   except Exception:time.sleep(attempt+1)
 b=p.read_bytes();return {'file':f,'url':u,'sha256':hashlib.sha256(b).hexdigest(),'sprite':'hq_'+name,'index':i,'sourcePage':f'https://scratch.mit.edu/projects/{id}/','credit':'Woody601 (Goomba); collection shared by MarioTheBest' if name=='goomba' else 'Random Talking Bush; collection shared by MarioTheBest'}
with concurrent.futures.ThreadPoolExecutor(10) as pool:upgrades=list(pool.map(get,jobs))
# Re-running curation must not duplicate source records.
new={(s['file'],s.get('sprite'),s.get('index')):s for s in sources+upgrades}
(HERE/'sources.json').write_text(json.dumps(list(new.values()),indent=2)+'\n')
print(f'Curated {len(upgrades)} larger native frames from 3 credited NSMBU collections.')
