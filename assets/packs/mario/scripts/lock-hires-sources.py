"""Pin exact bytes of each new source used by slicing.json (not the research cache)."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[2];RAW=ROOT/'assets/_downloads/mario'
c=json.loads((HERE/'slicing.json').read_text());lock=json.loads((HERE/'sources.json').read_text());known={x['file'] for x in lock}
files=set()
def walk(v):
 if isinstance(v,dict):
  if 'source' in v:files.add(v['source'])
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
walk(c)
rev=(RAW/'hires/miyamoto-rev.txt').read_text()
wiki={'mushroom':'b/b5/NSMBU_Mushroom_Artwork.png','coin':'2/22/NSMBU_Coin_Artwork.png','goomba':'e/eb/NSMBU_Goomba_Render.png','acorn':'6/65/SuperAcornNSMBU.png','brick':'f/fb/NSMBW_Brick_Block_Artwork.png','question':'0/02/Question_Block_NSMB.png','used':'9/97/NSMBW_Empty_Block_Artwork.png','key':'1/11/SMM-NSMBU-Key.png'}
for file in sorted(files-known):
 p=RAW/file;parts=Path(file).parts
 if file.startswith('hires/miyamoto/'):
  url='https://raw.githubusercontent.com/aboood40091/Miyamoto/'+rev+'/'+file.removeprefix('hires/miyamoto/');credit='Nintendo NSMBU imagery; Miyamoto editor image collection, AboodXD/Gota7 and contributors. No GPL editor code copied.'
 elif file.startswith('hires/scratch/'):
  url='https://assets.scratch.mit.edu/internalapi/asset/'+p.name+'/get/';credit=f'Raster capture collection shared by PolskyGamer, Scratch project {parts[2]}. Source/game caveats in SOURCES.md.'
 elif file=='hires/wiki/coin.gif':url='https://www.mariowiki.com/images/4/4c/NSMBUCoin.gif';credit='Nintendo NSMBU coin animation; Super Mario Wiki.'
 elif file.startswith('hires/wiki/'):
  url='https://www.mariowiki.com/images/'+wiki[p.stem];credit='Nintendo official artwork/native render, Super Mario Wiki NSMBU gallery. Block artwork reused from NSMB/NSMBW, as labelled by the gallery.'
 else:raise ValueError(file)
 lock.append({'file':file,'url':url,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'credit':credit})
(HERE/'sources.json').write_text(json.dumps(lock,indent=2)+'\n')
print(f'Pinned {len(files-known)} new image sources; {len(lock)} total SHA-256 records.')
