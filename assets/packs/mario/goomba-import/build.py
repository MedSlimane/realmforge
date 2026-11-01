#!/usr/bin/env python3
"""Offline lossless source crops. Writes only the Goomba import's two owned trees.
Requires the existing mario pack's Pillow==12.3.0 (MIT-CMU/HPND).
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PUBLIC = ROOT / 'web/public/packs/mario/enemies/goomba-import'
PACK_PREFIX = 'enemies/goomba-import/'
SOURCE_NAME = 'Nintendo Switch - Super Mario Maker 2 - New Super Mario Bros. U_ Enemies - Goomba (NSMBU).png'
SOURCE_PAGE = 'https://www.spriters-resource.com/nintendo_switch/supermariomaker2/asset/238649/'
CYAN = (0, 162, 232, 255)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pixels(im):
    return hashlib.sha256(im.tobytes()).hexdigest()


def dump(path, obj):
    path.write_text(json.dumps(obj, indent=2) + '\n')


def crops():
    recipe = json.loads((HERE / 'recipe.json').read_text())
    source_path = HERE / recipe['source']
    assert sha(source_path) == recipe['sourceSha256'], 'Source checksum mismatch'
    source = Image.open(source_path).convert('RGBA')
    assert list(source.size) == recipe['sourceSize']
    canvas_size = tuple(recipe['canvas'])
    frames, records, sequences = {}, {}, {}
    for name, seq in recipe['sequences'].items():
        names = []
        for y, count in seq['rows']:
            for col in range(count):
                x = recipe['left'] + col * recipe['columnStride']
                cell = (x, y, x + recipe['cellWidth'], y + recipe['cellHeight'])
                assert 0 <= cell[0] < cell[2] <= source.width
                assert 0 <= cell[1] < cell[3] <= source.height
                crop = source.crop(cell)
                # The sheet uses transparent cells, not a colour key. Keep all RGBA pixels.
                assert CYAN not in crop.get_flattened_data(), 'Sheet border/credit area in crop'
                bounds = crop.getchannel('A').getbbox()
                assert bounds is not None
                tight = crop.crop(bounds)
                assert tight.width <= canvas_size[0] and tight.height <= canvas_size[1]
                offset = ((canvas_size[0] - tight.width) // 2, canvas_size[1] - tight.height)
                canvas = Image.new('RGBA', canvas_size)
                canvas.paste(tight, offset)  # No alpha mask: preserves semi-transparent source RGBA.
                key = f'goomba_{name}_{len(names):02}'
                frames[key] = canvas
                records[key] = {
                    'sequence': name, 'sourceCellXYXY': list(cell),
                    'sourceContentXYXY': [x+bounds[0], y+bounds[1], x+bounds[2], y+bounds[3]],
                    'nativeOpaqueSize': list(tight.size), 'canvasOffset': list(offset),
                    'rgbaSha256': pixels(canvas), 'contentRgbaSha256': pixels(tight),
                }
                names.append(key)
        sequences[name] = names
    return recipe, frames, records, sequences


def build():
    recipe, frames, records, sequences = crops()
    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / 'frames').mkdir(exist_ok=True)
    width, height = recipe['canvas']
    cols, gutter = 8, 2
    stride_x, stride_y = width + 2*gutter, height + 2*gutter
    atlas = Image.new('RGBA', (cols*stride_x, math.ceil(len(frames)/cols)*stride_y))
    atlas_json = {'frames': {}, 'meta': {'app': 'RealmForge lossless Goomba import', 'image': 'atlas.png', 'format': 'RGBA8888', 'size': {'w': atlas.width, 'h': atlas.height}, 'scale': '1'}}
    for i, (name, frame) in enumerate(frames.items()):
        x, y = (i % cols)*stride_x+gutter, (i // cols)*stride_y+gutter
        atlas.paste(frame, (x, y))
        frame.save(PUBLIC / 'frames' / f'{name}.png')
        atlas_json['frames'][name] = {'frame': {'x': x, 'y': y, 'w': width, 'h': height}, 'rotated': False, 'trimmed': False, 'spriteSourceSize': {'x': 0, 'y': 0, 'w': width, 'h': height}, 'sourceSize': {'w': width, 'h': height}}
    atlas.save(PUBLIC / 'atlas.png')
    dump(PUBLIC / 'atlas.json', atlas_json)
    frames[sequences['walk'][0]].save(PUBLIC / 'goomba.png')
    # Explicit common canvas preserves the flattened shape and uniform runtime scale.
    animations = {name: {'frames': sequences[name], 'frameRate': recipe['sequences'][name]['frameRate'], 'repeat': recipe['sequences'][name]['repeat']} for name in ('walk', 'stomp')}
    entry = {'texture': 'mario-walker', 'path': PACK_PREFIX+'goomba.png', 'image': PACK_PREFIX+'atlas.png', 'atlas': PACK_PREFIX+'atlas.json', 'width': width, 'height': height, 'frame': sequences['walk'][0], 'displaySize': {'w': 1.2, 'h': 1}, 'anchor': {'x': 0.5, 'y': 1}, 'animations': animations, 'source': 'goomba-import/source/goomba-tsr-238649.png', 'sourceUrl': SOURCE_PAGE, 'pack': 'mario-nsmbu', 'note': 'Nintendo; SMM2 NSMBU Goomba ripped by DogToon64 (TSR 238649). Native lossless crops; 16 walk + 14 flattened stomp frames. Actions inferred visually; sheet has no action labels or timing. Authored playback: 12 / 24 fps. Smaller than previous still; no enlargement. Common 120x100 canvas; 76.8x64 display keeps uniform 0.64x pixel scale.'}
    fragment = {section: {key: entry for key in ('walker', 'goomba')} for section in ('elements', 'enemies')}
    dump(HERE / 'manifest-fragment.json', fragment)
    dump(HERE / 'frames.json', {'canvas': recipe['canvas'], 'anchor': {'x': 0.5, 'y': 1}, 'sequences': {name: {**recipe['sequences'][name], 'frames': names} for name, names in sequences.items()}, 'frames': records})
    # Full contact sheet, each pixel displayed once. Presentation background is separate.
    sheet = Image.new('RGB', (8*144, 4*34+9*128), '#182238')
    draw = ImageDraw.Draw(sheet)
    y = 0
    for name, names in sequences.items():
        draw.text((8, y+6), f'{name}: {len(names)} source frames; {recipe["sequences"][name]["frameRate"]} fps preview', fill='white')
        y += 34
        for i, key in enumerate(names):
            x, row = (i % 8)*144, i//8
            # Native-resolution frame on a neutral background, baseline guide below feet.
            sheet.paste(frames[key], (x+12, y+row*128), frames[key])
            draw.line((x+8, y+row*128+100, x+136, y+row*128+100), fill='#6e829e')
            draw.text((x+8, y+row*128+106), key.replace('goomba_', ''), fill='white')
        y += math.ceil(len(names)/8)*128
    sheet.crop((0, 0, sheet.width, y)).save(HERE / 'contact-sheet.png')
    # GIF is a lossy preview only (GIF has no partial alpha); runtime uses untouched RGBA PNGs.
    previews, durations = [], []
    for name, names in sequences.items():
        for key in names:
            preview = Image.new('RGB', (300, 145), '#182238')
            preview.paste(frames[key], (90, 32), frames[key])
            d = ImageDraw.Draw(preview)
            d.text((8, 5), f'{name} / {key.rsplit("_",1)[1]} / native 1:1', fill='white')
            # Encode nearest centisecond; intended timings remain in recipe/manifest.
            previews.append(preview)
            durations.append(round(100 / recipe['sequences'][name]['frameRate']) * 10)
    previews[0].save(HERE / 'preview.gif', save_all=True, append_images=previews[1:], duration=durations, loop=0, disposal=2, optimize=False)
    baseline = HERE / 'reference/previous-walker.png'
    old = Image.open(baseline).convert('RGBA')
    ob = old.getchannel('A').getbbox()
    comparison = Image.new('RGB', (660, 240), '#182238')
    d = ImageDraw.Draw(comparison)
    d.text((8, 8), 'Previous output (native)', fill='white')
    comparison.paste(old, (55, 40), old)
    d.text((220, 8), 'New walk (native)', fill='white')
    comparison.paste(frames[sequences['walk'][0]], (240, 62), frames[sequences['walk'][0]])
    d.text((435, 8), 'New stomp (native)', fill='white')
    comparison.paste(frames[sequences['stomp'][0]], (450, 62), frames[sequences['stomp'][0]])
    d.text((8, 185), 'PNG source pixels are unchanged. Shared feet baseline = bottom of 120x100 canvas.', fill='white')
    d.text((8, 205), 'Game: old 64x64; new canvas 76.8x64 / walk envelope 54.4x64 (0.64x uniform).', fill='white')
    comparison.save(HERE / 'comparison.png')
    dump(HERE / 'provenance.json', {'source': {'downloadedFile': SOURCE_NAME, 'originalDirectory': '/Users/slimane/Downloads/realmforge-rips', 'copy': 'source/goomba-tsr-238649.png', 'sha256': recipe['sourceSha256'], 'size': list(Image.open(HERE/recipe['source']).size), 'url': SOURCE_PAGE, 'sheetCredit': ['Goomba [NSMBU] from Super Mario Maker 2 ripped by DogToon64.', 'If used, give credit to Nintendo.', 'Credit to DogToon64 is optional, but would be nice.'], 'timing': 'Not supplied; rates are author-selected, not claimed original game timing.', 'rights': 'Nintendo. Private educational demo restriction; not CC0 or an open licence.'}, 'previousOutput': {'file': 'reference/previous-walker.png', 'originalFile': 'web/public/packs/mario/enemies/walker.png', 'sha256': sha(baseline), 'canvas': list(old.size), 'opaqueXYXY': list(ob)}, 'previousOriginalSource': {'file': 'assets/_downloads/mario/hires/wiki/goomba.png', 'sha256': 'd2082794e455f5489b715cdfdc8a783e147dd6b6b3c2e7d20a3671d5a3f47b70', 'nativeSize': [208, 243], 'note': 'Existing slicing.json downsamples this original to the 104x122 current output.'}})
    paths = [HERE / p for p in ('recipe.json', 'build.py', 'verify-registry.ts', 'manifest-fragment.json', 'frames.json', 'provenance.json', 'contact-sheet.png', 'preview.gif', 'comparison.png', 'source/goomba-tsr-238649.png', 'reference/previous-walker.png')]
    paths += sorted(PUBLIC.rglob('*.png')) + [PUBLIC / 'atlas.json']
    dump(HERE / 'sha256.json', {str(p.relative_to(ROOT)): sha(p) for p in paths})
    validate()


def validate():
    recipe, frames, records, sequences = crops()
    source_hash = recipe['sourceSha256']
    original = Path('/Users/slimane/Downloads/realmforge-rips') / SOURCE_NAME
    if original.exists():
        assert sha(original) == source_hash, 'Original download changed'
        print('PASS original download unchanged: '+source_hash)
    checksums = json.loads((HERE / 'sha256.json').read_text())
    for path, digest in checksums.items():
        assert sha(ROOT / path) == digest, f'Hash mismatch: {path}'
    print(f'PASS SHA-256: {len(checksums)} input/output files')
    assert json.loads((HERE/'frames.json').read_text())['frames'] == records
    atlas = Image.open(PUBLIC / 'atlas.png').convert('RGBA')
    metadata = json.loads((PUBLIC / 'atlas.json').read_text())
    assert set(metadata['frames']) == set(frames)
    rects = []
    for name, expected in frames.items():
        stored = Image.open(PUBLIC/'frames'/f'{name}.png').convert('RGBA')
        assert stored.size == expected.size and stored.tobytes() == expected.tobytes(), name
        f = metadata['frames'][name]['frame']
        box = (f['x'], f['y'], f['x']+f['w'], f['y']+f['h'])
        assert 0 <= box[0] < box[2] <= atlas.width and 0 <= box[1] < box[3] <= atlas.height
        assert all(box[2] <= b[0] or box[0] >= b[2] or box[3] <= b[1] or box[1] >= b[3] for b in rects)
        rects.append(box)
        assert atlas.crop(box).tobytes() == expected.tobytes(), name
        assert expected.getchannel('A').getbbox()[3] == recipe['canvas'][1], name
        assert CYAN not in expected.get_flattened_data(), name
    assert Image.open(PUBLIC/'goomba.png').convert('RGBA').tobytes() == frames[sequences['walk'][0]].tobytes()
    print(f'PASS atlas bounds/non-overlap and exact source RGBA: {len(frames)} frames, {atlas.width}x{atlas.height}; feet baseline 100')
    for name, names in sequences.items():
        unique = len({pixels(frames[key]) for key in names})
        assert unique == len(names), f'Duplicate pixels in {name}'
        dims = [records[key]['nativeOpaqueSize'] for key in names]
        print(f'PASS {name}: {len(names)} frames, {unique} unique; native opaque widths {min(d[0] for d in dims)}..{max(d[0] for d in dims)}, heights {min(d[1] for d in dims)}..{max(d[1] for d in dims)}')
    assert len({record['contentRgbaSha256'] for record in records.values()}) == len(records), 'Cross-sequence duplicate content'
    print(f'PASS global uniqueness: {len(records)} distinct native content crops')
    fragment = json.loads((HERE/'manifest-fragment.json').read_text())
    canonical = fragment['elements']['walker']
    for section in ('elements', 'enemies'):
        assert set(fragment[section]) == {'walker', 'goomba'}
        for entry in fragment[section].values():
            assert entry == canonical
            for anim, value in entry['animations'].items():
                assert value['frames'] == sequences[anim]
                assert all(f in frames for f in value['frames'])
            for key in ('path', 'image', 'atlas'):
                assert (ROOT/'web/public/packs/mario'/entry[key]).is_file()
    current = json.loads((ROOT/'web/public/packs/mario/manifest.json').read_text())
    existing = []
    for section in ('elements', 'enemies'):
        for key, entry in current.get(section, {}).items():
            if key in ('walker','goomba') or entry.get('texture') == 'mario-walker':
                assert key in fragment[section], f'Missing existing alias: {section}.{key}'
                existing.append(section+'.'+key)
    print('PASS aliases: elements/enemies x walker/goomba; existing coverage '+', '.join(existing))
    with Image.open(HERE/'preview.gif') as gif:
        assert gif.n_frames == len(frames)
        print(f'PASS preview GIF: {gif.n_frames} real frames; runtime PNG alpha retained')
    print('PASS lossless build: no resize, recolour, interpolated or repeated animation frames')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    validate() if args.verify_only else build()
