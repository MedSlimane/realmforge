"""Regression probes for the requested hard failure, without mutating the pack."""
import copy,json,unittest
from validate import OUT,validate_display_scale
from build import crop
class NativeScaleValidation(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.manifest=json.loads((OUT/'manifest.json').read_text())
 def test_real_pack_passes(self):self.assertGreater(validate_display_scale(self.manifest),400)
 def test_rejects_undersized_static_sprite(self):
  m=copy.deepcopy(self.manifest);e=m['elements']['crate'];e['displaySize']['w']=e['width']*1.26/64
  with self.assertRaisesRegex(AssertionError,'Upscaled sprite elements.crate'):validate_display_scale(m)
 def test_rejects_undersized_animation_canvas(self):
  m=copy.deepcopy(self.manifest);e=m['characters']['mario'];e['displaySize']['h']=e['height']*1.26/64;e['height']*=2
  with self.assertRaisesRegex(AssertionError,'Upscaled animation characters.mario'):validate_display_scale(m)
 def test_rejects_native_pixel_enlargement(self):
  with self.assertRaisesRegex(AssertionError,'Upsampling source art is forbidden'):crop({'source':'tiles/21847-0.png','rect':[0,0,1,1],'resize':[2,2]})
if __name__=='__main__':unittest.main(verbosity=2)
