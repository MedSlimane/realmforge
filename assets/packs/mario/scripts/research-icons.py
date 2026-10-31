"""Research-only mirror icon inventory; no executable game sources are copied."""
from pathlib import Path
import concurrent.futures, json, urllib.request, time
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[4];RAW=ROOT/'assets/_downloads/mario'
d=json.loads((RAW/'SMM2LevelViewer-tree.json').read_text())
paths=[x['path'] for x in d['tree'] if '/21847/OBJ/' in x['path'] and x['path'].endswith('.png')]
def download(p):
 f=RAW/'icons'/Path(p).name;f.parent.mkdir(exist_ok=True)
 if not f.exists():
  for _ in range(5):
   try:f.write_bytes(urllib.request.urlopen('https://raw.githubusercontent.com/JiXiaomai/SMM2LevelViewer/master/'+p,timeout=20).read());break
   except Exception:time.sleep(1)
 return f
with concurrent.futures.ThreadPoolExecutor(12) as pool:files=list(pool.map(download,paths))
im=Image.new('RGB',(1600,((len(files)+15)//16)*110),'#64717f');draw=ImageDraw.Draw(im)
for i,f in enumerate(files):
 if not f.exists():continue
 s=Image.open(f).convert('RGBA');s.thumbnail((96,80));x=i%16*100;y=i//16*110;im.paste(s,(x,y+22),s);draw.text((x,y),f.stem,fill='white')
im.save(RAW/'icons-review.png');print(len(files),'icons')
