import unittest,copy
import dynamics_checks as dc
class DynamicsOracle(unittest.TestCase):
 def fixture(self):
  result={'fields':[]}
  for i in range(200):
   f={'f':i,'pose':[16,0,0,16,0,0,0,1564,-200,0],'physics':[0]*32,'motion':[0]*17,'mesh_positions':[0,1500,0,0,1500,0],'game':[0]*28}
   q=f['physics'];f['game'][20]=60;q[6]=16*256;q[12]=84*256;q[25]=i+1;f['motion'][16]=i+1
   x,y,z=dc.transformed_vertex(f);q[26]=((x&65535)<<16)|(y&65535);q[27]=(z&65535)<<16;q[28]=z
   rec=32768//max(2,z);xx=(abs(x)*rec)>>7;yy=(abs(y)*rec)>>7
   xx=xx if x>=0 else -xx;yy=-yy if y>=0 else yy;yy=yy*11>>4
   q[29]=((192+xx)&65535)<<16|((100+yy)&65535)
   result['fields'].append(f)
  return result
 def test_exact_vertex(self):self.assertEqual(dc.verify_vertices(self.fixture())['actual_vertices'],50)
 def test_missing_camera_pitch_rejected(self):
  t=self.fixture();t['fields'][170]['physics'][12]=0
  with self.assertRaises(AssertionError):dc.verify_vertices(t)
 def test_missing_ship_pitch_rejected(self):
  t=self.fixture();t['fields'][170]['pose'][0]=0
  with self.assertRaises(AssertionError):dc.verify_vertices(t)
 def test_corrupt_projected_pixel_rejected(self):
  t=self.fixture();t['fields'][170]['physics'][29]+=1
  with self.assertRaises(AssertionError):dc.verify_vertices(t)
 def test_signed_vertex_word(self):self.assertEqual(dc.signed16(65535),-1)
 def test_original_start_height(self):self.assertEqual(dc.height_q8(-9072*256,-3544*256),1548*256)
 def test_slope_table(self):
  import json,math
  data=json.loads((dc.R/'assets/dynamics.json').read_text())
  self.assertEqual(data['atan_q8'],[round(math.atan(i/256)*2048/(2*math.pi)*256) for i in range(129)])
if __name__=='__main__':unittest.main()

class ParticleOracle(unittest.TestCase):
 def fixture(self):
  t={'fields':[]};p=[0,0,0,2,1,-1,12000,0]
  for i in range(200):
   paused=i in (175,176)
   if i in (160,170,180,190):p=[0,0,0,i,1,-1,15360,0]
   if not paused:
    p[6]=max(0,p[6]-256)
    p[:3]=[p[j]+p[j+3] for j in range(3)]
   g=[0]*28;g[2]=1;g[13]=int(paused)
   fx=[0]*16;fx[2]=1;fx[3]=1;fx[4]=50;fx[12]=i+1;fx[14]=256
   t['fields'].append({'f':i,'game':g,'effects':fx,'particles':p[:]+[0]*120})
  return t
 def test_real_time_recurrence(self):self.assertGreater(dc.verify_particles(self.fixture())['particle_integrations'],20)
 def test_pointer_in_lifetime_rejected(self):
  t=self.fixture();t['fields'][165]['particles'][6]=0xf03162
  with self.assertRaises(AssertionError):dc.verify_particles(t)
 def test_integration_error_rejected(self):
  t=self.fixture();t['fields'][165]['particles'][0]+=1
  with self.assertRaises(AssertionError):dc.verify_particles(t)
 def test_pause_motion_rejected(self):
  t=self.fixture();t['fields'][176]['particles'][0]+=1
  with self.assertRaises(AssertionError):dc.verify_particles(t)

class FallMultiplyRange(unittest.TestCase):
 def test_all_video_step_products(self):
  for hz in [50,60]:
   for dt in range(1,7):
    # Model Jaguar MULT's two unsigned low-16 operands explicitly.
    native=(((80*60)&65535)*(dt&65535)<<8)//hz
    self.assertEqual(native,80*256*dt*60//hz)
 def test_old_multiply_order_is_not_equivalent(self):
  self.assertNotEqual(((80*256*4)&65535)*60//60,80*256*4)

class ActiveFallingPauseOracle(unittest.TestCase):
 def fixture(self,pause_while_active):
  result={'fields':[{'physics':[0]*32,'motion':[0]*17,'game':[0]*28} for _ in range(150)]}
  fall=0;height=0;clock=0
  for i in range(160):
   active=fall<90
   paused=10<=i<45 if pause_while_active else i>=100
   if active and not paused:fall+=1;height-=80*256
   clock+=not paused
   g=[0]*28;q=[0]*32;m=[0]*17
   g[2]=1 if fall<90 else 2;g[5]=height;g[13]=int(paused);g[18]=clock;g[20]=60
   q[4]=1;q[5]=fall;q[11]=i+1;m[16]=i+1
   result['fields'].append({'f':150+i,'game':g,'physics':q,'motion':m})
  return result
 def test_active_fall_hold_is_counted(self):self.assertGreater(dc.verify_fall(self.fixture(True))['paused_fall_updates'],20)
 def test_destroyed_pause_is_not_falling_proof(self):self.assertEqual(dc.verify_fall(self.fixture(False))['paused_fall_updates'],0)
