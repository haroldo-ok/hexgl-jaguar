import unittest,struct,json,hashlib,copy,subprocess
import numpy as np
from native_fx_checks import R,rgb,blend,pixel,depth
from native_audio_checks import decode_stream,nibble,read_stream

class StereoADPCM(unittest.TestCase):
 def test_known_signed_nibbles(self):
  data=struct.pack('>hHhH',0,0,0,0)+bytes([0x7f,0x7f])
  self.assertEqual(list(decode_stream(data)),[11,-11,41,-41])
 def test_saturation_and_index_bounds(self):
  self.assertEqual(nibble(7,32767,88),(32767,88))
  self.assertEqual(nibble(15,-32768,88),(-32768,88))
  self.assertEqual(nibble(0,0,0),(0,0))
 def test_actual_source_stereo_complete_duration_and_quality(self):
  seen_stereo=False
  for m in json.loads((R/'assets/audio.json').read_text()):
   b=read_stream(m['name'])
   self.assertEqual(hashlib.sha256(b).hexdigest(),m['sha256'])
   actual=np.asarray(decode_stream(b),dtype=np.float64)
   original=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(R/'vendor/HexGL/audio'/f'{m["name"]}.ogg'),'-ar','7990','-ac','2','-f','s16be','pipe:1']),dtype='>i2').astype(np.float64)
   self.assertEqual(len(actual),len(original));self.assertEqual(len(actual)//2,m['frames'])
   snr=10*np.log10((original**2).sum()/max(1,((actual-original)**2).sum()))
   self.assertGreater(snr,22);self.assertAlmostEqual(snr,m['snr_db'],places=1)
   channels=original.reshape(-1,2)
   if np.any(channels[:,0]!=channels[:,1]):
    seen_stereo=True
    decoded=actual.reshape(-1,2)
    self.assertGreater(np.corrcoef(channels[:,0]-channels[:,1],decoded[:,0]-decoded[:,1])[0,1],.95)
  self.assertTrue(seen_stereo,'Original spatial sources accidentally collapsed to mono')
 def test_stock_cartridge_audio_slot(self):
  self.assertLessEqual((R/'assets/audio.bin').stat().st_size,0x100000)
  self.assertEqual((R/'rom/hexgl.j64').stat().st_size,6*1024*1024)

class RGBShader(unittest.TestCase):
 def test_decode_table_actual_dac(self):
  from hud_checks import palette
  expected=b''.join(bytes([0,*color]) for color in palette().tolist())
  self.assertEqual((R/'assets/color-decode.bin').read_bytes(),expected)
 def test_packed_alpha_not_part_of_chroma(self):
  self.assertEqual(blend(0xc87aff,0x7740,128,1),blend(0x7aff,0x7740,128,1))
 def test_zero_alpha_over_quantizes_destination_only(self):
  self.assertEqual(blend(0x7aff,0x7740,0,0),blend(0,0x7740,0,1))
 def test_rgb555_nearest_chroma_and_intensity(self):
  from hud_checks import palette
  coeff=palette().astype(np.float64)/255
  enc=np.frombuffer((R/'assets/color-encode.bin').read_bytes(),dtype='>u2').astype(int)
  for start in range(0,32768,1024):
   indices=np.arange(start,start+1024)
   color=np.stack([((indices>>10)&31)*8,((indices>>5)&31)*8,(indices&31)*8],axis=1)
   intensity=np.clip(color@coeff.T/(coeff*coeff).sum(axis=1),0,255)
   error=((color[:,None,:]-intensity[:,:,None]*coeff[None,:,:])**2).sum(axis=2)
   selected=enc[start:start+1024]>>8
   self.assertTrue(np.all(error[np.arange(1024),selected]<=error.min(axis=1)+.003))
   self.assertTrue(np.all(abs((enc[start:start+1024]&255)-intensity[np.arange(1024),selected])<=.501))

class DepthProof(unittest.TestCase):
 def fixture(self):
  d=[0]*32;d[16:20]=[2,2,200,100]
  d[20:23]=[0,(10<<16),10];d[23:26]=[100]*3
  # Relative triangle (0,0),(10,0),(0,10), all same Z.
  d[26:30]=[60,20,20,100];d[30]=0x120000;d[31]=2
  # Quantized reciprocal = 327, so reciprocal inverse rounds to 100.
  return d
 def test_actual_barycentric_depth(self):self.assertTrue(depth(self.fixture()))
 def test_bad_z_rejected(self):
  d=self.fixture();d[19]=200
  with self.assertRaises(AssertionError):depth(d)
 def test_bad_weights_rejected(self):
  d=self.fixture();d[26]+=1
  with self.assertRaises(AssertionError):depth(d)
 def test_odd_commit_ignored(self):
  d=self.fixture();d[31]=3;self.assertFalse(depth(d))

class SourceStereoOracle(unittest.TestCase):
 def test_independent_center_channels(self):
  from material_checks import audio_sample
  self.assertTrue(audio_sample([2,150,275,64,125,50,200,50,0,0]))
 def test_collapsed_center_rejected(self):
  from material_checks import audio_sample
  with self.assertRaises(AssertionError):audio_sample([2,150,150,64,125,50,200,50,0,0])

class SpritePixelProof(unittest.TestCase):
 def fixture(self):
  from native_fx_checks import tables
  a=[0]*32;a[14]=200;a[15]=2;a[25:28]=[20,200,2];a[28:32]=[182,120,10,10]
  a[16]=tables()[2][2*256+8*16+8];a[17]=0x7850;a[18]=(a[16]>>16)*200//256;a[19]=1
  a[20]=blend(a[16],a[17],a[18],1)
  x,y=192,130;a[21]=0x1b4800+y*1536+(x//4)*16+(x%4)*2
  return a
 def test_exact_source_and_output(self):self.assertTrue(pixel(self.fixture()))
 def test_wrong_composite_rejected(self):
  a=self.fixture();a[20]^=1
  with self.assertRaises(AssertionError):pixel(a)
 def test_fixed_size_substitution_rejected(self):
  a=self.fixture();a[25]=16
  with self.assertRaises(AssertionError):pixel(a)
 def test_wrong_source_texel_rejected(self):
  a=self.fixture();a[16]^=1
  with self.assertRaises(AssertionError):pixel(a)
 def test_framebuffer_address_rejected(self):
  a=self.fixture();a[21]=0
  with self.assertRaises(AssertionError):pixel(a)
 def test_odd_pixel_commit_ignored(self):
  a=self.fixture();a[15]=3;self.assertFalse(pixel(a))
