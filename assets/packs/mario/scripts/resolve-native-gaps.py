"""Record reviewed native coin cycles and locked-door state; no fabricated poses.
Historical curation helper. fetch/build require only sources.json and slicing.json.
"""
from pathlib import Path
from PIL import Image
import copy, hashlib, json
from build import crop
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[2];RAW=ROOT/'assets/_downloads/mario'
c=json.loads((HERE/'slicing.json').read_text());records=json.loads((HERE/'sources.json').read_text())
urls={
 'NSMBUCoin.gif':('https://www.mariowiki.com/images/4/4c/NSMBUCoin.gif','https://www.mariowiki.com/File:NSMBUCoin.gif','TheMorningFlash; cropped by Cheese Head (2025); source credits The Spriters Resource'),
 'SMM2-NSMBU-10Coin.gif':('https://www.mariowiki.com/images/0/0d/SMM2-NSMBU-10Coin.gif','https://www.mariowiki.com/File:SMM2-NSMBU-10Coin.gif','Thejohnston7 (2025); file history credits The Spriters Resource'),
 'SMM-NSMBU-Locked-Door.png':('https://www.mariowiki.com/images/8/8c/SMM-NSMBU-Locked-Door.png','https://www.mariowiki.com/File:SMM-NSMBU-Locked-Door.png','Mario Wiki; source credits The Spriters Resource'),
}
for n,(u,page,credit) in urls.items():
 f='resolution/'+n;b=(RAW/f).read_bytes()
 records=[s for s in records if s['file']!=f]+[{'file':f,'url':u,'sha256':hashlib.sha256(b).hexdigest(),'sourcePage':page,'credit':credit,'rights':'Nintendo proprietary; private team authorization is not a copyright licence.'}]
for id,n in [('coin','NSMBUCoin.gif'),('big_coin','SMM2-NSMBU-10Coin.gif')]:
 im=Image.open(RAW/'resolution'/n);count=im.n_frames;w,h=im.size
 a=c['assets'][id];a['frames']=[{'source':'resolution/'+n,'sourceFrame':i,'rect':[0,0,w,h]} for i in range(count)]
 a['animations']={'idle':list(range(count)),'spin':list(range(count))}
 a['animationFrameRates']={'idle':1000/im.info['duration'],'spin':1000/im.info['duration']}
 a['note']=f'Native {count}-frame '+('NSMBU Coin' if id=='coin' else 'SMM2 NSMBU 10-Coin')+' cycle from Mario Wiki; original GIF order and timing, no interpolated or duplicated poses. See RESOLUTION_REPORT.md.'
a=c['assets']['locked_door'];a['frames']=[{'source':'resolution/SMM-NSMBU-Locked-Door.png','rect':[0,0,78,154]}];a['note']='Authentic SMM NSMBU locked-door state with integrated keyhole, sourced from Mario Wiki/TSR. Full texture, not a separately extracted transparent lock overlay.'
# Remove misleading empty margins from undersized static content, preserving its
# exact previous on-screen opaque dimensions. This does not enlarge the art.
for id,a in c['assets'].items():
 if len(a['frames'])!=1 or a.get('animations') or a.get('animationSources') or 'displaySize' not in a:continue
 im=crop(a['frames'][0]);b=im.getbbox()
 if not b:continue
 w,h=b[2]-b[0],b[3]-b[1];d=a['displaySize']
 if max(d['w']*64/w,d['h']*64/h)<=1.25+1e-5:continue
 ref=a['frames'][0]
 if 'compose' in ref or 'resize' in ref:raise ValueError(('Needs manual review',id))
 x,y,_,_=ref['rect'];ref['rect']=[x+b[0],y+b[1],w,h]
 a['displaySize']={'w':d['w']*w/im.width,'h':d['h']*h/im.height}
 a['note']=a.get('note','')+' Transparent source margins removed; previous visible size preserved.'
(HERE/'sources.json').write_text(json.dumps(records,indent=2)+'\n')
(HERE/'slicing.json').write_text(json.dumps(c,indent=2)+'\n')
print('Recorded 16 native Coin frames, 13 native 10-Coin frames, genuine locked-door state; preserved static visible dimensions.')
