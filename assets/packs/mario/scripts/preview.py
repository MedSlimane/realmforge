"""Contact sheet of every manifest element, native character strips and layered scenery."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[2];OUT=ROOT/'web/public/packs/mario'
W=1920;M=24
try:FONT=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',14);TITLE=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',23)
except OSError:FONT=ImageFont.load_default();TITLE=FONT
m=json.loads((OUT/'manifest.json').read_text());char_names=['mario','luigi','mario_small','luigi_native_walk'];char_rows=sum(len(m['characters'][c]['animations']) for c in char_names)
H=140+math.ceil(len(m['elements'])/12)*146+80+char_rows*120+4*520
canvas=Image.new('RGB',(W,H),'#182438');d=ImageDraw.Draw(canvas);y=20

def text(x,y,s,font=FONT,fill='#ffffff'):d.text((x,y),s,font=font,fill=fill)
def paste(im,box):
 x,y,w,h=box;im=im.convert('RGBA');scale=min(w/im.width,h/im.height);im=im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))),Image.Resampling.LANCZOS);canvas.paste(im,(x+(w-im.width)//2,y+(h-im.height)//2),im)
text(M,y,'RealmForge — NSMBU private class demo pack',TITLE);y+=38
text(M,y,'Nintendo property. No public distribution. Native source pixels; linear filtering; sourceTile = 64.');y+=24
text(M,y,'Luigi big = disclosed Mario colour variant. Pink/purple/beige = Mario aliases; green = Luigi.');y+=32
start=y
for i,(id,e) in enumerate(m['elements'].items()):
 x=M+i%12*156;y=start+i//12*146;d.rounded_rectangle((x,y,x+148,y+138),radius=8,fill='#30435a')
 paste(Image.open(OUT/e['path']),(x+6,y+4,136,100))
 label=id if len(id)<=20 else id[:19]+'…';text(x+5,y+110,label,fill='#f3cf70')
y=start+math.ceil(len(m['elements'])/12)*146+25
text(M,y,'Character animation strips — common canvas, bottom-centred feet',TITLE);y+=45
for name in char_names:
 e=m['characters'][name];atlas=Image.open(OUT/e['image']).convert('RGBA');frames=json.loads((OUT/e['atlas']).read_text())['frames']
 for anim,a in e['animations'].items():
  text(M,y,f'{name}:{anim}',fill='#ffc83d')
  for i,f in enumerate(a['frames']):
   r=frames[f]['frame'];im=atlas.crop((r['x'],r['y'],r['x']+r['w'],r['y']+r['h']));paste(im,(300+i*120,y,110,105))
  y+=120
for theme,t in m['themes'].items():
 text(M,y,f'{theme} — {len(t["parallax"])} native layers (stacked below)',TITLE);y+=40
 # Show each layer as a separate strip, then the full composition at source alignment.
 composition=Image.new('RGBA',(1536,432))
 for i,l in enumerate(t['parallax']):
  im=Image.open(OUT/l['file']).convert('RGBA');strip=Image.new('RGBA',(1536,432))
  for x in range(0,1536,im.width):strip.alpha_composite(im,(x,0))
  composition.alpha_composite(strip)
  paste(strip,(M+i*260,y,250,100));text(M+i*260,y+102,f'{i}: factor {l["scrollFactor"]}')
 y+=130;paste(composition,(M,y,W-2*M,310));y+=340
canvas=canvas.crop((0,0,W,y+20));canvas.save(OUT/'PREVIEW.png',optimize=True)
print(f'PREVIEW.png: {canvas.width}x{canvas.height}; {len(m["elements"])} element IDs, {char_rows} character animation strips, 4 stacked backgrounds')
