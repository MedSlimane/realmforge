"""Scale/import regression probes, including two real reproducible pack builds."""
import copy,json,unittest,tempfile,subprocess,sys,hashlib
from unittest.mock import patch
from PIL import Image
from validate import OUT,validate_display_scale,character_fidelity_issues
from audit import content_size
from build import crop,integrate_staged,HERE,build_goomba_import,integrate_goomba,retained_import_output,published_art_matches
class NativeScaleValidation(unittest.TestCase):
 def setUp(self):self.manifest=json.loads((OUT/'manifest.json').read_text())
 def test_real_pack_passes(self):self.assertGreater(validate_display_scale(self.manifest),400)
 def test_character_fidelity_rejects_renamed_identical_frames(self):
  im=Image.new('RGBA',(64,120),(255,0,0,255));keys=[f'frame_{i}' for i in range(6)]
  entry={'animations':{pose:{'frames':keys} for pose in ('walk','run')}}
  with patch('validate.native_frames',return_value=[(key,im) for key in keys]):
   issues=character_fidelity_issues({'characters':{'probe':entry}})
  self.assertEqual(len(issues),2)
  self.assertTrue(all('only 1 distinct pixel frames' in issue for issue in issues))
 def test_character_fidelity_rejects_disclosed_fallback_with_long_cycle(self):
  keys=[f'frame_{i}' for i in range(6)]
  entry={'fallback':True,'fallbackReasons':['wrong source game'],'animations':{pose:{'frames':keys} for pose in ('walk','run')}}
  frames=[(key,Image.new('RGBA',(64,120),(i,0,0,255))) for i,key in enumerate(keys)]
  with patch('validate.native_frames',return_value=frames):
   self.assertEqual(character_fidelity_issues({'characters':{'probe':entry}}),['probe: fallback remains: wrong source game'])
 def test_staging_ignores_incomplete_fragment(self):
  with tempfile.TemporaryDirectory(dir=HERE) as path:
   from pathlib import Path
   folder=Path(path);(folder/'objects.json').write_text('not complete JSON')
   m={'elements':{'spring':{'path':'existing.png'}}};before=copy.deepcopy(m)
   integrate_staged(m,folder)
   self.assertEqual(m,before)
 def test_staging_merges_finished_fragment_without_publishing_art(self):
  from pathlib import Path
  with tempfile.TemporaryDirectory(dir=HERE) as path:
   folder=Path(path);(folder/'DONE').touch()
   fragment={'schema':1,'elements':{'spring':self.manifest['elements']['spring']},'fx':{}}
   (folder/'objects.json').write_text(json.dumps(fragment));m={}
   integrate_staged(m,folder);self.assertEqual(m['elements'],fragment['elements'])
 def test_staging_rejects_unpublished_art(self):
  from pathlib import Path
  with tempfile.TemporaryDirectory(dir=HERE) as path:
   folder=Path(path);(folder/'DONE').touch()
   (folder/'objects.json').write_text(json.dumps({'fx':{'dust':{'path':'missing-staged-art.png'}}}))
   with self.assertRaisesRegex(AssertionError,'Object owner has not published'):integrate_staged({},folder)
 def test_goomba_merge_retains_unrelated_entries_and_aliases(self):
  m=copy.deepcopy(self.manifest);before=copy.deepcopy(m)
  integrate_goomba(m)
  fragment=json.loads((HERE/'goomba-import/manifest-fragment.json').read_text())
  for section in ('elements','enemies'):
   for name,entry in fragment[section].items():self.assertEqual(m[section][name],entry)
   for name,entry in before[section].items():
    if name not in fragment[section]:self.assertEqual(m[section][name],entry)
  for section in set(before)-set(fragment):self.assertEqual(m[section],before[section])
 def test_goomba_build_runs_pinned_import_when_source_exists(self):
  with patch('build.subprocess.run') as run:
   build_goomba_import()
   run.assert_called_once_with([sys.executable,str(HERE/'goomba-import/build.py')],check=True)
 def test_goomba_and_inspection_deliverables_survive_two_real_rebuilds(self):
  protected=[p for folder in ('enemies/goomba-import','characters/model-preview') for p in (OUT/folder).rglob('*') if p.is_file()]
  before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
  previous=json.loads((OUT/'manifest.json').read_text())
  for iteration in range(2):
   result=subprocess.run([sys.executable,str(HERE/'scripts/build.py')],capture_output=True,text=True)
   self.assertEqual(result.returncode,0,result.stdout+result.stderr)
   self.assertIn('GOOMBA: final entry-by-entry merge',result.stdout)
   manifest=json.loads((OUT/'manifest.json').read_text())
   fragment=json.loads((HERE/'goomba-import/manifest-fragment.json').read_text())
   for section,entries in fragment.items():
    for name,entry in entries.items():self.assertEqual(manifest[section][name],entry)
   for section,values in previous.items():
    if section in fragment:
     for name,entry in values.items():
      if name not in fragment[section]:self.assertEqual(manifest[section][name],entry)
    else:self.assertEqual(manifest[section],values)
   if iteration==0:first=manifest
   else:self.assertEqual(manifest,first)
   for p,digest in before.items():
    self.assertTrue(retained_import_output(p));self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),digest)
 def test_published_objects_allow_only_encoding_changes_not_pixel_changes(self):
  from pathlib import Path
  with tempfile.TemporaryDirectory(dir=HERE) as path:
   root=Path(path);source=root/'source.png';target=root/'published.png'
   image=Image.new('RGBA',(8,8),(31,50,90,128))
   image.save(source,compress_level=0);image.save(target,compress_level=9)
   files={'published.png':{'path':str(source.relative_to(HERE)),'sha256':hashlib.sha256(source.read_bytes()).hexdigest()}}
   with patch('build.OUT',root):
    self.assertTrue(published_art_matches(files))
    image.putpixel((3,4),(1,2,3,4));image.save(target)
    self.assertFalse(published_art_matches(files))
 def test_reviewed_object_files_are_preserved_while_verifying_current_staging(self):
  paths=[p for folder in (HERE/'integrated',OUT/'objects') for p in folder.rglob('*') if p.is_file()]
  before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
  m={};integrate_staged(m)
  self.assertEqual({p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},before)
  for section in ('elements','fx'):
   for name,entry in json.loads((HERE/'integrated/manifest-fragment.json').read_text())[section].items():
    self.assertEqual(m[section][name],entry)
 def test_goomba_source_native_aspect_ratio_for_every_runtime_frame(self):
  fragment=json.loads((HERE/'goomba-import/manifest-fragment.json').read_text())
  e=fragment['elements']['walker'];atlas=json.loads((OUT/e['atlas']).read_text())
  self.assertEqual(e['anchor'],{'x':0.5,'y':1})
  self.assertEqual(len(e['animations']['walk']['frames']),16)
  self.assertEqual(len(e['animations']['stomp']['frames']),14)
  for animation in e['animations'].values():
   for name in animation['frames']:
    frame=atlas['frames'][name]['sourceSize']
    sx=64*e['displaySize']['w']/frame['w'];sy=64*e['displaySize']['h']/frame['h']
    self.assertAlmostEqual(sx,sy);self.assertAlmostEqual(sx,0.64)
 def test_rejects_undersized_static_sprite(self):
  m=copy.deepcopy(self.manifest);e=m['elements']['crate'];e['displaySize']['w']=e['width']*1.26/64
  with self.assertRaisesRegex(AssertionError,'Upscaled sprite elements.crate'):validate_display_scale(m)
 def test_rejects_undersized_animation_canvas(self):
  m=copy.deepcopy(self.manifest);e=m['characters']['mario'];e['displaySize']['h']=e['height']*1.26/64;e['height']*=2
  with self.assertRaisesRegex(AssertionError,'Upscaled animation characters.mario'):validate_display_scale(m)
 def test_rejects_native_pixel_enlargement(self):
  with self.assertRaisesRegex(AssertionError,'Upsampling source art is forbidden'):crop({'source':'tiles/21847-0.png','rect':[0,0,1,1],'resize':[2,2]})
 def test_rejects_transparent_padding_as_resolution(self):
  # An 8px source pasted into a 128px canvas must not pass a 128px display check.
  im=Image.new('RGBA',(128,128));im.paste((255,255,255,255),(60,60,68,68))
  e={'path':'synthetic-regression-only.png','width':128,'height':128,'displaySize':{'w':2,'h':2}}
  with patch('audit.native_frames',return_value=[(None,im)]):
   self.assertEqual(content_size(e),(8,8))
   with self.assertRaisesRegex(AssertionError,'Upscaled opaque content elements.probe'):
    validate_display_scale({'elements':{'probe':e}})
 def test_native_coin_frames_are_distinct_and_keep_source_timing(self):
  m=self.manifest
  for name,count,rate in [('coin',16,20),('big_coin',13,1000/60)]:
   e=m['elements'][name];self.assertEqual(len(e['animations']['spin']['frames']),count)
   self.assertEqual(e['animations']['idle']['frameRate'],rate)
   from audit import native_frames
   self.assertEqual(len({im.tobytes() for _,im in native_frames(e)}),count)
 def test_rejects_padding_around_entire_animation_cycle(self):
  e=copy.deepcopy(self.manifest['elements']['coin'])
  im=Image.new('RGBA',(e['width'],e['height']));im.paste((255,255,255,255),(20,20,28,28))
  with patch('audit.native_frames',return_value=[('probe_0',im),('probe_1',im)]):
   with self.assertRaisesRegex(AssertionError,'Upscaled opaque content elements.probe'):
    validate_display_scale({'elements':{'probe':e}})
 def test_legacy_one_way_tile_keeps_empty_space_below_deck(self):
  # The legacy grid must not stretch a 23px deck into a 64px solid block.
  original=json.loads((OUT.parents[1]/'assets/manifest.json').read_text())
  for theme,t in self.manifest['themes'].items():
   order=list(original['themes'][theme]['tiles']);index=order.index('one_way')
   with Image.open(OUT/t['path']) as sheet:
    x=index%8*64;y=index//8*64
    self.assertIsNone(sheet.convert('RGBA').getchannel('A').crop((x+2,y+32,x+62,y+62)).getbbox())
if __name__=='__main__':unittest.main(verbosity=2)
