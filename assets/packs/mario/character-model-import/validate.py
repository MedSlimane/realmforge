#!/usr/bin/env python3
"""Verify source integrity, extraction safety, bind-only outputs and repeatability."""
import io
import json
from pathlib import Path
import stat
import unittest
from zipfile import ZipFile, ZipInfo

from PIL import Image

from extract_inspect import ROOT, safe_members, sha256


class ArchiveSafety(unittest.TestCase):
    def archive(self, names):
        stream = io.BytesIO()
        with ZipFile(stream, 'w') as archive:
            for name in names:
                archive.writestr(name, b'x')
        stream.seek(0)
        return ZipFile(stream)

    def test_traversal_absolute_windows_and_case_collisions(self):
        for names in (['../escape'], ['/tmp/escape'], ['x/../../escape'],
                      ['C:/escape'], ['x\\..\\escape'], ['A.png', 'a.png']):
            with self.subTest(names=names), self.archive(names) as archive:
                with self.assertRaises(ValueError):
                    safe_members(archive)

    def test_symlink_rejected(self):
        stream = io.BytesIO()
        with ZipFile(stream, 'w') as archive:
            entry = ZipInfo('link')
            entry.create_system = 3
            entry.external_attr = (stat.S_IFLNK | 0o777) << 16
            archive.writestr(entry, '../escape')
        stream.seek(0)
        with ZipFile(stream) as archive, self.assertRaises(ValueError):
            safe_members(archive)

    def test_directory_and_regular_file_allowed(self):
        with self.archive(['Mario/', 'Mario/model.dae']) as archive:
            self.assertEqual(len(safe_members(archive)), 2)


def main():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ArchiveSafety)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    assert result.wasSuccessful()
    locks = json.loads((ROOT / 'source-lock.json').read_text())
    count = 0
    for source in locks:
        assert sha256(Path(source['source_file'])) == source['sha256']
        for file in source['files']:
            assert sha256(ROOT / file['file']) == file['sha256']
            count += 1
    print(f'PASS: 2 original ZIPs and {count} extracted source files match SHA-256 locks')
    inventory = json.loads((ROOT / 'model-inventory.json').read_text())
    assert len(inventory) == 24
    assert all(not m[key] for m in inventory for key in ('animations', 'animation_clips', 'channels', 'samplers'))
    print('PASS: 24 DAE files; 0 animations, animation clips, channels or animation samplers')
    data = json.loads((ROOT / 'preview-scene.json').read_text())
    for model in data['models'].values():
        assert model['max_bind_identity_error'] < 0.001
        for part in model['parts']:
            assert sha256(ROOT / part['texture']) == part['sha256']
            assert len(part['triangles']) == len(part['uv']) == len(part['normals'])
    print('PASS: source diffuse textures, per-corner UV/normal counts and skin bind identities')
    records = json.loads((ROOT / 'render-results.json').read_text())
    assert len(records) == 18
    pixel_results = []
    for row in records:
        path = ROOT.parents[3] / row['file']
        assert path.is_relative_to(ROOT.parents[3] / 'web/public/packs/mario/characters/model-preview')
        assert sha256(path) == row['sha256']
        assert row['camera'] == 'orthographic' and row['actions'] == 0
        with Image.open(path) as im:
            assert im.mode == 'RGBA' and im.size == (192, 192)
            alpha = im.getchannel('A')
            assert alpha.getextrema() == (0, 255)
            bbox = alpha.getbbox()
            assert bbox and bbox[0] > 0 and bbox[1] > 0 and bbox[2] < 192 and bbox[3] < 192, (path, bbox)
            # Antialiasing can add one texel at each silhouette edge.
            assert bbox[3] - bbox[1] <= row['target_height_px'] + 2, (path, bbox)
            pixel_results.append({'file': path.name, 'alpha_bbox': bbox})
    assert not (ROOT / 'manifest-fragment.json').exists()
    print('PASS: 18 RGBA 192x192 orthographic stills; alpha background; no clipping; 60/120px height budgets; no actions/manifest fragment')
    first = ROOT / 'evidence/first-render-results.json'
    if first.exists():
        original = {r['file']: r['sha256'] for r in json.loads(first.read_text())}
        assert original == {r['file']: r['sha256'] for r in records}
        print('PASS: repeated Blender render has identical SHA-256 for all 18 PNGs')
    (ROOT / 'evidence/pixel-checks.json').write_text(json.dumps(pixel_results, indent=2) + '\n')


if __name__ == '__main__':
    main()
