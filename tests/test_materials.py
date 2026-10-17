import hashlib,json,unittest
import numpy as np
from material_checks import R,audio_sample

class NativeMaterials(unittest.TestCase):
 def setUp(self):self.meta=json.loads((R/'assets/materials.json').read_text())
 def test_atlas_layout(self):
  blob=(R/'assets/materials.bin').read_bytes()
  self.assertEqual(len(blob),8*9*64*64*2)
  self.assertEqual(hashlib.sha256(blob).hexdigest(),self.meta['sha256'])
  for entry in self.meta['entries']:
   data=blob[entry['offset']:entry['offset']+8192]
   self.assertEqual(hashlib.sha256(data).hexdigest(),entry['sha256'])
 def test_all_original_material_maps(self):
  paths=self.meta['sources']
  self.assertEqual(sum(p.endswith('/normal.jpg') for p in paths),6)
  self.assertEqual(sum(p.endswith('/specular.jpg') for p in paths),6)
  self.assertEqual(sum('/skybox/' in p for p in paths),6)
  for p,digest in paths.items():self.assertEqual(hashlib.sha256((R/p).read_bytes()).hexdigest(),digest)
 def test_no_opaque_texture_holes(self):
  for e in self.meta['entries']:
   if e['material']=='booster':self.assertGreater(e['transparent_texels'],0)
   else:self.assertEqual(e['transparent_texels'],0)
 def test_view_dependent_materials(self):
  for name in ['ship','base','track','scrapers1','scrapers2','start']:
   hashes={e['sha256'] for e in self.meta['entries'] if e['material']==name}
   self.assertGreater(len(hashes),1,name+' lookup banks identical')
 def test_speed_pad_is_source_constant(self):
  from frontend_checks import cry
  from PIL import Image
  color=int.from_bytes(cry(Image.new('RGB',(1,1),'#0096ff')),'big')
  a=np.frombuffer((R/'assets/materials.bin').read_bytes(),dtype='>u2').reshape(8,9,64,64)
  self.assertTrue(np.all(a[:,4]==color))
 def test_static_shadows_are_geometry_bound(self):
  data=json.loads((R/'assets/shadow-faces.json').read_text())
  for p,digest in data['sources'].items():self.assertEqual(hashlib.sha256((R/p).read_bytes()).hexdigest(),digest)
  self.assertEqual(sum(len(v) for v in data['faces'].values()),12206)
  self.assertGreater(data['occluded_faces'],0)
  self.assertLess(data['occluded_faces'],data['receiver_faces'])
  self.assertEqual(sum(v.count(128) for v in data['faces'].values()),data['occluded_faces'])
  for name,v in data['faces'].items():
   if name.startswith(('ship','booster','speed')):self.assertEqual(set(v),{160})
 def test_compiled_face_shadow_inputs(self):
  import re
  shadows=json.loads((R/'assets/shadow-faces.json').read_text())['faces']
  text=''.join(p.read_text() for p in sorted((R/'assets').glob('models_*.inc')))
  for label,values in shadows.items():
   section=text.split(label+'_faces:\n',1)[1].split(label+'_normals:',1)[0]
   actual=[int(x) for x in re.findall(r'dc.w [0-9]+,[0-9]+,[0-9]+,([0-9]+)',section)]
   self.assertEqual(actual,values,label)
 def test_sky_covers_pitch_without_duplicate_width(self):self.assertEqual((R/'assets/sky.bin').stat().st_size,2048*512*2)

class StereoOracle(unittest.TestCase):
 def test_center(self):self.assertTrue(audio_sample([2,150,150,0,100,50,100,50,0,0]))
 def test_pan(self):self.assertTrue(audio_sample([2,125,175,64,100,50,100,50,0,0]))
 def test_negative_sample(self):self.assertTrue(audio_sample([2,-25,-75,64,0,-50,0,-50,0,0]))
 def test_saturation(self):self.assertTrue(audio_sample([2,32767,32767,0,32000,10000,32000,10000,0,0]))
 def test_partial_dsp_write(self):self.assertFalse(audio_sample([3,0,0,0,100,50,100,50,0,0]))
 def test_mono_substitution_rejected(self):
  with self.assertRaises(AssertionError):audio_sample([2,150,150,64,100,50,100,50,0,0])
 def test_reversed_channels_rejected(self):
  with self.assertRaises(AssertionError):audio_sample([2,175,125,64,100,50,100,50,0,0])
 def test_bad_gain_rejected(self):
  with self.assertRaises(AssertionError):audio_sample([2,125,176,64,100,50,100,50,0,0])

class RuntimeMaterialOracle(unittest.TestCase):
 def fixture(self):
  return {'fields':[{'material_state':[0x902000,0,1,0x902000,156+i%5,0,0,180,64,128,20,148]} for i in range(250)]}
 def test_real_face_arithmetic(self):
  from material_checks import materials
  self.assertGreater(materials(self.fixture())['face_light_additions_checked'],50)
 def test_wrong_bank_stride_rejected(self):
  from material_checks import materials
  t=self.fixture()
  for f in t['fields']:f['material_state'][:2]=[0x902000+8192,1]
  with self.assertRaises(AssertionError):materials(t)
 def test_diffuse_table_substitution_rejected(self):
  from material_checks import materials
  t=self.fixture();t['fields'][180]['material_state'][3]=0x40000
  with self.assertRaises(AssertionError):materials(t)
 def test_sprite_only_light_rejected(self):
  from material_checks import materials
  t=self.fixture()
  for f in t['fields']:f['material_state'][2]=0
  with self.assertRaises(AssertionError):materials(t)
 def test_corrupt_face_luminance_rejected(self):
  from material_checks import materials
  t=self.fixture()
  for f in t['fields']:f['material_state'][11]+=1
  with self.assertRaises(AssertionError):materials(t)
 def test_yaw_only_sky_rejected(self):
  from material_checks import materials
  t=self.fixture()
  for f in t['fields']:f['material_state'][4]=156
  with self.assertRaises(AssertionError):materials(t)
