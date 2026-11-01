"""Run with Blender --background --factory-startup --python render_previews.py.

Creates native target-size orthographic inspection stills; never animation frames.
"""
import hashlib
import json
from pathlib import Path
import sys

import bpy
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from png_metadata import stable_png
REPO = ROOT.parents[3]
OUT = REPO / 'web/public/packs/mario/characters/model-preview'
DATA = json.loads((ROOT / 'preview-scene.json').read_text())
# Source Y-up, +Z forward => Blender Z-up, +X forward. Right-handed rotation only.
AXIS = Matrix(((0, 0, 1, 0), (-1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1)))


def add_model(name, transform):
    objects = []
    for part in DATA['models'][name]['parts']:
        mesh = bpy.data.meshes.new(f'{name}/{part["name"]}')
        mesh.from_pydata(part['vertices'], [], part['triangles'])
        mesh.update()
        uv = mesh.uv_layers.new(name='CHANNEL0')
        for polygon, coords in zip(mesh.polygons, part['uv']):
            polygon.use_smooth = True
            for loop, coord in zip(polygon.loop_indices, coords):
                uv.data[loop].uv = coord
        mesh.normals_split_custom_set([n for triangle in part['normals'] for n in triangle])
        obj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(obj)
        obj.matrix_world = AXIS @ transform
        material = bpy.data.materials.new(f'{name}/{part["material"]}')
        material.use_nodes = True
        nodes = material.node_tree.nodes
        shader = nodes.get('Principled BSDF')
        shader.inputs['Roughness'].default_value = 1
        shader.inputs['Specular IOR Level'].default_value = 0
        image = nodes.new('ShaderNodeTexImage')
        image.image = bpy.data.images.load(str(ROOT / part['texture']), check_existing=True)
        same_wrap = part['wrap'][0] == part['wrap'][1]
        image.extension = {'MIRROR': 'MIRROR', 'WRAP': 'REPEAT', 'CLAMP': 'EXTEND'}[part['wrap'][0]] if same_wrap else 'REPEAT'
        if not same_wrap:
            coords = nodes.new('ShaderNodeTexCoord')
            separate = nodes.new('ShaderNodeSeparateXYZ')
            combine = nodes.new('ShaderNodeCombineXYZ')
            links = material.node_tree.links
            links.new(coords.outputs['UV'], separate.inputs[0])
            for axis, wrap in zip(('X', 'Y'), part['wrap']):
                value = separate.outputs[axis]
                if wrap == 'MIRROR':
                    mirror = nodes.new('ShaderNodeMath')
                    mirror.operation = 'PINGPONG'
                    mirror.inputs[1].default_value = 1
                    links.new(value, mirror.inputs[0])
                    value = mirror.outputs[0]
                elif wrap == 'CLAMP':
                    clamp = nodes.new('ShaderNodeClamp')
                    links.new(value, clamp.inputs['Value'])
                    value = clamp.outputs[0]
                links.new(value, combine.inputs[axis])
            links.new(combine.outputs[0], image.inputs['Vector'])
        image.interpolation = 'Linear'
        material.node_tree.links.new(image.outputs['Color'], shader.inputs['Base Color'])
        # DAE phong has no transparent input: preserve its opaque diffuse semantics.
        mesh.materials.append(material)
        objects.append(obj)
    return objects


def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()


def render(entry, view):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 32
    scene.cycles.seed = 0
    scene.cycles.use_denoising = False
    scene.render.threads_mode = 'FIXED'
    scene.render.threads = 4
    scene.render.resolution_x = scene.render.resolution_y = 192
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.film_transparent = True
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'None'
    scene.view_settings.exposure = 0
    scene.view_settings.gamma = 1
    world = bpy.data.worlds.new('Neutral inspection studio')
    world.use_nodes = True
    world.node_tree.nodes.get('Background').inputs[0].default_value = (1, 1, 1, 1)
    world.node_tree.nodes.get('Background').inputs[1].default_value = 0.8
    scene.world = world
    if 'body' in entry:
        objects = add_model(entry['body'], Matrix.Identity(4))
        objects += add_model(entry['head'], Matrix(entry['head_transform']))
    else:
        objects = add_model(entry['part'], Matrix.Identity(4))
    points = [obj.matrix_world @ Vector(corner) for obj in objects for corner in obj.bound_box]
    lo = Vector(tuple(min(p[i] for p in points) for i in range(3)))
    hi = Vector(tuple(max(p[i] for p in points) for i in range(3)))
    center = (hi + lo) / 2
    height = hi.z - lo.z
    # Camera-only framing: never rescale textures, meshes or rendered PNGs.
    scale = height * 192 / entry['target_height_px']
    if view == 'front':
        scale = max(scale, (hi.y - lo.y) * 1.2)
    camera_data = bpy.data.cameras.new('Orthographic inspection camera')
    camera_data.type = 'ORTHO'
    camera_data.ortho_scale = scale
    camera = bpy.data.objects.new('Camera', camera_data)
    scene.collection.objects.link(camera)
    camera.location = center + Vector((0, -100, 0) if view == 'side' else (100, 0, 0))
    aim(camera, center)
    scene.camera = camera
    lamp_data = bpy.data.lights.new('Soft studio key', 'AREA')
    lamp_data.energy = 6000
    lamp_data.shape = 'DISK'
    lamp_data.size = 50
    lamp = bpy.data.objects.new('Soft studio key', lamp_data)
    scene.collection.objects.link(lamp)
    lamp.location = center + Vector((35, -50, 60))
    aim(lamp, center)
    assert len(bpy.data.actions) == 0
    path = OUT / f'{entry["id"]}-{view}-bind-preview.png'
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)
    stable_png(path)
    record = {'id': entry['id'], 'view': view, 'kind': entry['kind'], 'file': str(path.relative_to(REPO)),
              'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'camera': 'orthographic',
              'ortho_scale': scale, 'resolution': [192, 192], 'target_height_px': entry['target_height_px'],
              'actions': len(bpy.data.actions), 'bounds_blender': [list(lo), list(hi)]}
    print('PREVIEW_OK', json.dumps(record), flush=True)
    return record


OUT.mkdir(parents=True, exist_ok=True)
records = [render(entry, view) for entry in DATA['assemblies'] for view in entry['views']]
(ROOT / 'render-results.json').write_text(json.dumps(records, indent=2) + '\n')
print(f'PASS: {len(records)} transparent inspection stills; 0 animation actions; no runtime manifest generated')
