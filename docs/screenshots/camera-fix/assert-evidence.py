"""Check recorded real-browser trajectories; no dependencies or browser mocks."""
import gzip
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def read(name):
    path = ROOT / (name + '.json')
    if path.exists():
        return json.loads(path.read_text())
    with gzip.open(str(path) + '.gz', 'rt') as f:
        return json.load(f)

def span(values):
    return max(values) - min(values)

records = {}
for pack in ['mario', 'kenney']:
    for mode in ['play', 'editor']:
        name = f'after-{pack}-{mode}'
        record = read(name)
        records[name] = record
        samples = record['data']['samples']
        assert len(samples) > 200, name
        assert not any(s['visualTarget'] or s['round'] or s['renderRound'] for s in samples), name
        assert all(s['canvas']['same'] for s in samples), name
        assert record['summary']['counts']['resize'] == 0, name
        assert record['summary']['counts']['canvasReplacements'] == 0, name
        assert record['summary']['counts']['internalCanvasResizes'] == 0, name
        assert all(abs(s['physical']['x'] - s['sprite']['x']) < 1e-8 for s in samples), name
        assert {'idle', 'walk', 'run', 'jump', 'fall'} <= {s['physical']['mode'] for s in samples}, name
        assert max(v['maxParallaxError'] for v in record['summary']['phases'].values()) < 1e-8, name
        flat_name = f'verified-{pack}-{mode}-flat'
        record = read(flat_name)
        records[flat_name] = record
        samples = record['data']['samples']
        jumping = [s for s in samples if s['phase'] in ['jump', 'land']]
        assert span([s['scroll']['y'] for s in jumping]) < 1e-8, flat_name
        assert span([s['physical']['foot'] for s in jumping]) > 200, flat_name
        assert record['summary']['counts']['resize'] == 2, flat_name
        assert record['summary']['counts']['canvasReplacements'] == 0, flat_name
        for s in samples:
            for layer in s['layers']:
                assert int(layer['w']) == layer['w'] and int(layer['h']) == layer['h'], flat_name
                assert layer['w'] * s['zoom'] >= s['canvas']['width'], flat_name
                assert layer['h'] * s['zoom'] >= s['canvas']['height'], flat_name
        assert max(v['maxParallaxError'] for v in record['summary']['phases'].values()) < 1e-8, flat_name
        if mode == 'play':
            assert record['data']['events'][0]['name'] == 'react-pause-resume', flat_name

for pack, mode in [('mario', 'play'), ('kenney', 'editor')]:
    for kind in ['slope', 'fall', 'spring', 'forms']:
        name = f'verified-{pack}-{mode}-{kind}'
        record = read(name)
        records[name] = record
        samples = record['data']['samples']
        assert all(s['canvas']['same'] and not s['visualTarget'] for s in samples), name
        assert max(v['maxParallaxError'] for v in record['summary']['phases'].values()) < 1e-8, name
        if kind == 'slope':
            grounded = [s for s in samples if s['physical']['mode'] in ['idle', 'walk', 'run', 'skid']]
            assert span([s['physical']['foot'] for s in grounded]) > 80, name
            assert span([s['scroll']['y'] for s in grounded]) > 50, name
        if kind in ['fall', 'spring']:
            assert span([s['scroll']['y'] for s in samples]) > 500, name
            for s in samples:
                feet = s['canvas']['height'] / 2 + (s['physical']['foot'] - s['scroll']['y'] - s['canvas']['height'] / 2) * s['zoom']
                assert 0 < feet < s['canvas']['height'], (name, feet)
        if kind == 'forms':
            assert max(s['physical']['physicalHeight'] for s in samples) > 100, name
            assert span([s['scroll']['y'] for s in samples]) < 1e-8, name

for name, record in records.items():
    print(f"PASS {name}: {len(record['data']['samples'])} rendered frames")
print(f"PASS {len(records)} real-browser trajectories; physical follow, ordinary-jump baseline, same-frame parallax, slopes, vertical travel, forms, resize and canvas identity")
