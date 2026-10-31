"""Regression probes for the requested hard failure, without mutating the pack."""
import copy,json,unittest,tempfile
from unittest.mock import patch
from PIL import Image
from validate import OUT,validate_display_scale,character_fidelity_issues
from audit import content_size
from build import crop,integrate_staged,HERE
class NativeScaleValidation(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.manifest=json.loads((OUT/'manifest.json').read_text())
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
