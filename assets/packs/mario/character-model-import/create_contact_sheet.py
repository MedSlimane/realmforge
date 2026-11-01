#!/usr/bin/env python3
"""Place final PNGs at 1:1 on a labelled inspection sheet. No resampling."""
import json
from PIL import Image, ImageDraw, ImageFont
from extract_inspect import ROOT

records = json.loads((ROOT / 'render-results.json').read_text())
font = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 12)
sheet = Image.new('RGB', (832, 64 + ((len(records) + 3) // 4) * 226), '#0f1424')
draw = ImageDraw.Draw(sheet)
draw.text((16, 12), 'NSMBU MODEL INSPECTION — BIND POSES / PARTS ONLY', font=font, fill='white')
draw.text((16, 32), 'No idle, walk, run or other gameplay animations are present.', font=font, fill='#ffc83d')
for i, row in enumerate(records):
    x, y = 8 + i % 4 * 208, 64 + i // 4 * 226
    for cy in range(0, 192, 12):
        for cx in range(0, 192, 12):
            draw.rectangle((x + cx, y + cy, x + cx + 11, y + cy + 11),
                           fill='#242c42' if (cx // 12 + cy // 12) % 2 else '#303a52')
    with Image.open(ROOT.parents[3] / row['file']) as im:
        assert im.size == (192, 192) and im.mode == 'RGBA'
        sheet.paste(im, (x, y), im)
    draw.text((x, y + 196), row['id'], font=font, fill='white')
    draw.text((x, y + 210), row['view'] + ' / bind preview', font=font, fill='#aab3d0')
sheet.save(ROOT / 'PREVIEWS.png')
print(f'PASS: contact sheet {sheet.size}; {len(records)} renders placed at 1:1; no resampling')
