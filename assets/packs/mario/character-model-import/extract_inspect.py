#!/usr/bin/env python3
"""Safely extract the two user-supplied ZIPs and inventory unmodified files."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
NS = {'c': 'http://www.collada.org/2005/11/COLLADASchema'}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_members(archive):
    """Validate the entire archive before writing; refuse links and zip bombs."""
    seen, total = set(), 0
    for info in archive.infolist():
        p = PurePosixPath(info.filename)
        mode = info.external_attr >> 16
        if (p.is_absolute() or '..' in p.parts or '\\' in info.filename
                or ':' in info.filename or not p.parts
                or stat.S_ISLNK(mode) or info.flag_bits & 1
                or stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR)):
            raise ValueError(f'Unsafe ZIP member: {info.filename!r}')
        key = str(p).casefold()
        if key in seen:
            raise ValueError(f'Duplicate ZIP path: {p}')
        seen.add(key)
        total += info.file_size
        if info.file_size > 100_000_000 or total > 250_000_000:
            raise ValueError('Archive exceeds extraction budget')
    return archive.infolist()


def inspect(path):
    data = path.read_bytes()
    if b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper():
        raise ValueError('External XML declarations forbidden')
    root = ET.fromstring(data)
    find = lambda query: root.findall(query, NS)
    parents = {child: parent for parent in root.iter() for child in parent}
    bones = []
    for node in find('.//c:node[@type="JOINT"]'):
        parent = parents.get(node)
        bones.append({**node.attrib, 'parent': parent.get('sid', parent.get('id')) if parent is not None else None,
                      'matrix': node.findtext('c:matrix', namespaces=NS)})
    controllers = []
    for node in find('.//c:controller'):
        skin = node.find('c:skin', NS)
        controllers.append({'id': node.get('id'), 'geometry': skin.get('source') if skin is not None else None,
                            'joint_names': [s.text.split() for s in node.findall('.//c:Name_array', NS)],
                            'bind_shape_matrix': node.findtext('.//c:bind_shape_matrix', namespaces=NS),
                            'vertex_weights': [s.attrib for s in node.findall('.//c:vertex_weights', NS)]})
    return {'file': str(path.relative_to(ROOT)), 'sha256': sha256(path),
            'up_axis': root.findtext('c:asset/c:up_axis', namespaces=NS),
            'unit': (root.find('c:asset/c:unit', NS).attrib if root.find('c:asset/c:unit', NS) is not None else None),
            'animations': len(find('.//c:animation')), 'animation_clips': len(find('.//c:animation_clip')),
            'channels': len(find('.//c:channel')), 'samplers': len(find('.//c:animation/c:sampler')),
            'geometries': [s.attrib for s in find('.//c:geometry')],
            'images': [{'id': s.get('id'), 'path': s.findtext('c:init_from', namespaces=NS)} for s in find('.//c:image')],
            'materials': [{'id': s.get('id'), 'effect': s.find('c:instance_effect', NS).get('url')} for s in find('.//c:material')],
            'material_bindings': [s.attrib for s in find('.//c:instance_material')],
            'bones': bones, 'controllers': controllers}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--downloads', type=Path, default=Path.home() / 'Downloads/realmforge-rips')
    args = parser.parse_args()
    sources = []
    for character in ('Mario', 'Luigi'):
        candidates = list(args.downloads.glob(f'* - {character}.zip'))
        if len(candidates) != 1:
            raise ValueError(f'Expected exactly one full-name {character} ZIP: {candidates}')
        archive_path = candidates[0]
        before = sha256(archive_path)
        destination = ROOT / 'extracted' / character.lower()
        if destination.is_symlink() or not destination.resolve().is_relative_to(ROOT):
            raise ValueError(f'Unsafe extraction root: {destination}')
        destination.mkdir(parents=True, exist_ok=True)
        files = []
        with ZipFile(archive_path) as archive:
            for info in safe_members(archive):
                target = destination.joinpath(*PurePosixPath(info.filename).parts)
                if any(p.is_symlink() for p in [target, *target.parents] if p.is_relative_to(ROOT)):
                    raise ValueError(f'Symlink in extraction path: {target}')
                if not target.resolve().is_relative_to(destination.resolve()):
                    raise ValueError(f'Escaping path: {target}')
                if info.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists() and (target.is_symlink() or sha256(target) != hashlib.sha256(archive.read(info)).hexdigest()):
                    raise ValueError(f'Refusing to overwrite differing file: {target}')
                with archive.open(info) as src, target.open('wb') as dst:
                    shutil.copyfileobj(src, dst)
                files.append({'member': info.filename, 'file': str(target.relative_to(ROOT)),
                              'bytes': target.stat().st_size, 'sha256': sha256(target)})
        assert before == sha256(archive_path), 'Source ZIP changed'
        sources.append({'character': character, 'source_file': str(archive_path), 'sha256': before,
                        'bytes': archive_path.stat().st_size, 'files': files})
    models = [inspect(p) for p in sorted((ROOT / 'extracted').rglob('*.dae'))]
    (ROOT / 'source-lock.json').write_text(json.dumps(sources, indent=2) + '\n')
    (ROOT / 'model-inventory.json').write_text(json.dumps(models, indent=2) + '\n')
    print(f'PASS: {len(sources)} original ZIP hashes unchanged; {sum(len(s["files"]) for s in sources)} extracted files')
    print(f'MODELS: {len(models)}; animations={sum(m["animations"] for m in models)}; channels={sum(m["channels"] for m in models)}')
    for model in models:
        print(Path(model['file']).name, 'geometries=', len(model['geometries']), 'bones=', len(model['bones']),
              'skins=', len(model['controllers']), 'textures=', ', '.join(i['path'] for i in model['images']))


if __name__ == '__main__':
    main()
