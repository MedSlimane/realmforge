#!/usr/bin/env python3
"""pycollada preview bridge. Refuses animation; preserves source bind geometry/UVs."""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import collada
import numpy as np

ROOT = Path(__file__).resolve().parent
NS = {'c': 'http://www.collada.org/2005/11/COLLADASchema'}


def node_matrices(document):
    result = {}
    def visit(node, parent):
        if not isinstance(node, collada.scene.Node):
            return
        matrix = parent @ node.matrix
        result[node.id] = matrix
        for child in node.children:
            visit(child, matrix)
    for node in document.scene.nodes:
        visit(node, np.eye(4))
    return result


def load_model(path):
    xml = ET.parse(path).getroot()
    assert not xml.findall('.//c:animation', NS), 'Animation requires a separate verified importer'
    document = collada.Collada(str(path))
    assert document.assetInfo.upaxis == 'Y_UP'
    matrices = node_matrices(document)
    # The source skins are already in rest/bind geometry. Never silently ignore deformation.
    errors, skins = [], []
    for bound in document.scene.objects('controller'):
        assert np.allclose(bound.matrix, np.eye(4)), 'Unexpected controller scene transform'
    for skin in document.controllers:
        assert np.allclose(skin.bind_shape_matrix, np.eye(4)), skin.id
        for name, inverse_bind in skin.joint_matrices.items():
            matches = [n for n in xml.findall('.//c:node', NS) if n.get('sid') == name]
            assert len(matches) == 1, name
            bind = matrices[matches[0].get('id')]
            error = float(np.max(np.abs(bind @ inverse_bind - np.eye(4))))
            assert error < 0.001, (path, name, error)
            errors.append(error)
        for indices in skin.weight_index:
            assert abs(float(np.sum(skin.weights[indices])) - 1) < 0.001
        skins.append({'id': skin.id, 'geometry': skin.geometry.id,
                      'inverse_bind_matrices': {str(k): v.tolist() for k, v in skin.joint_matrices.items()},
                      'weighted_vertices': len(skin.weight_index),
                      'max_influences_per_vertex': max(len(i) for i in skin.weight_index),
                      'bind_shape_matrix': skin.bind_shape_matrix.tolist()})
    materials = {}
    for material in document.materials:
        effect = material.effect
        diffuse = effect.diffuse
        assert isinstance(diffuse, collada.material.Map), material.id
        image_path = (path.parent / diffuse.sampler.surface.image.path).resolve()
        assert image_path.is_relative_to((ROOT / 'extracted').resolve()) and image_path.is_file()
        sampler = effect.xmlnode.find('.//c:sampler2D', NS)
        wraps = [sampler.findtext(f'c:wrap_{axis}', namespaces=NS) for axis in ('s', 't')]
        assert all(w in ('MIRROR', 'WRAP', 'CLAMP') for w in wraps), (material.id, wraps)
        materials[material.id] = {'texture': str(image_path.relative_to(ROOT)), 'wrap': wraps,
                                  'sha256': hashlib.sha256(image_path.read_bytes()).hexdigest()}
    # Resolve the actual instance_material symbol mapping, not filename guesses.
    bindings = {m.get('symbol'): m.get('target').lstrip('#') for m in xml.findall('.//c:instance_material', NS)}
    parts = []
    for geometry in document.geometries:
        for primitive in geometry.primitives:
            assert isinstance(primitive, collada.triangleset.TriangleSet)
            assert len(primitive.texcoordset) == 1
            material_id = bindings[primitive.material]
            parts.append({'name': geometry.id, 'material': material_id, **materials[material_id],
                          'vertices': primitive.vertex.tolist(), 'triangles': primitive.vertex_index.tolist(),
                          'normals': primitive.normal[primitive.normal_index].tolist(),
                          'uv': primitive.texcoordset[0][primitive.texcoord_indexset[0]].tolist()})
    bones = {n.get('sid'): matrices[n.get('id')] for n in xml.findall('.//c:node[@type="JOINT"]', NS)}
    return {'file': str(path.relative_to(ROOT)), 'parts': parts,
            'bounds': [np.concatenate([np.array(p['vertices']) for p in parts]).min(axis=0).tolist(),
                       np.concatenate([np.array(p['vertices']) for p in parts]).max(axis=0).tolist()],
            'max_bind_identity_error': max(errors), 'skins': skins,
            'bones': {k: v.tolist() for k, v in bones.items()}}


def main():
    models = {p.stem.removesuffix('_model'): load_model(p) for p in sorted((ROOT / 'extracted').rglob('*.dae'))}
    assemblies = []
    # Primary form labels use measured geometry, source normal-form materials and archive identity.
    for character, normal, small, variants in [
        ('mario', ('MB', 'MH'), ('SMB', 'SMH'), [('MMB', 'MMH'), ('PMB', 'PMH'), ('PLMB', 'PLMH')]),
        ('luigi', ('LB', 'LH'), ('SLB', 'SLH'), [('MLB', 'MLH'), ('PLB', 'PLH'), ('PLLB', 'PLLH')]),
    ]:
        for label, pair in [('big', normal), ('small', small)] + [(b.lower(), (b, h)) for b, h in variants]:
            body, head = pair
            assert 'face_1' in models[body]['bones']
            assemblies.append({'id': f'{character}-{label}', 'kind': 'assembled-bind-pose',
                               'body': body, 'head': head,
                               'head_transform': models[body]['bones']['face_1'],
                               'target_height_px': 60 if label == 'small' else 120,
                               'views': ['side', 'front'] if label in ('big', 'small') else ['side']})
        for cap in (('MC', 'SMC') if character == 'mario' else ('LC', 'SLC')):
            assemblies.append({'id': f'{character}-{cap.lower()}-cap-part', 'kind': 'standalone-bind-part',
                               'part': cap, 'target_height_px': 60, 'views': ['side'],
                               'note': 'Detached cap in source-local coordinates; not stacked on the head hat.'})
    output = {'schema': 1, 'purpose': 'inspection-only; no actions, no animation, no runtime manifest',
              'parser': f'pycollada {collada.__version__}', 'models': models, 'assemblies': assemblies}
    (ROOT / 'preview-scene.json').write_text(json.dumps(output, separators=(',', ':')) + '\n')
    summary = {k: {key: value for key, value in model.items() if key != 'parts'} |
                  {'triangles': sum(len(p['triangles']) for p in model['parts']),
                   'bindings': [{key: p[key] for key in ('name', 'material', 'texture', 'wrap', 'sha256')} for p in model['parts']]}
               for k, model in models.items()}
    (ROOT / 'geometry-evidence.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(f'PASS: pycollada {collada.__version__}; {len(models)} models, source skin bind identities/weights verified')
    print(f'PASS: {len(assemblies)} preview entries; all diffuse image bindings exist; source MIRROR/WRAP/CLAMP preserved per axis')


if __name__ == '__main__':
    main()
