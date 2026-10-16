"""Independent geometry/coverage and watchdog negative checks for real HUD art."""
import unittest,sys,struct,json,hashlib,re
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'tools'))
import hud
import hud_checks as oracle
class HUDTests(unittest.TestCase):
    def test_original_provenance(self):
        m=json.loads((R/'assets/hud.json').read_text());self.assertEqual(len(m['layers']),3)
        text=(R/m['clip_source']).read_text()
        self.assertEqual(hashlib.sha256((R/m['clip_source']).read_bytes()).hexdigest(),m['clip_source_sha256'])
        for name,value in [('speedBarRatio',2.91),('shieldBarWRatio',18.3),('shieldBarHRatio',14.3),('shieldBarYRatio',34)]:
            self.assertEqual(float(re.search(r'this\.'+name+r'\s*=\s*([0-9.]+)',text).group(1)),value)
        for l in m['layers']:
            self.assertEqual(hashlib.sha256((R/l['source']).read_bytes()).hexdigest(),l['source_sha256'])
            data=(R/l['native_file']).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(),l['native_sha256'])
            self.assertEqual(len(data),l['records']*8)
    def test_pitch_two_addressing(self):
        offsets={hud.offset(x,y) for y in range(50) for x in range(384)}
        self.assertEqual(len(offsets),384*50)
        self.assertTrue(all(x%2==0 and x%16<8 and x<384*50*4 for x in offsets))
    def test_coverage_from_png(self):
        for layer,(_,mask) in zip(['bg','speed','shield'],oracle.layers()):
            actual=np.zeros_like(mask)
            for metadata,c in struct.iter_unpack('>II',(R/f'assets/hud-{layer}.bin').read_bytes()):
                p=metadata&0xffffff;y=p//1536;x=p%1536//16*4+p%16//2
                actual[y,x]=True;self.assertLessEqual(c,65535)
            self.assertTrue(np.array_equal(actual,mask))
    def test_all_speed_clip_levels(self):
        yy,xx=np.mgrid[:50,:384];required=np.array([[hud.threshold('speed',x,y) for x in range(384)] for y in range(50)])
        for speed in range(29):
            expected=np.abs(xx+.5-192)<=384/2.91*(speed/28)+50-(yy+.5)
            self.assertTrue(np.array_equal(required<=speed,expected))
    def test_all_shield_clip_levels(self):
        yy,xx=np.mgrid[:50,:384];required=np.array([[hud.threshold('shield',x,y) for x in range(384)] for y in range(50)])
        for shield in range(101):
            expected=(abs(xx+.5-192)<=384/18.3)&(yy+.5>=384/34+384/14.3*(1-shield/100))&(yy+.5<384/34+384/14.3)
            self.assertTrue(np.array_equal(required<=shield,expected))
    def picture(self,speed,shield):
        pixels,mask=oracle.expected(speed,shield);a=np.zeros((240,434,3),np.uint8);a[8:58,17:401]=pixels
        return Image.fromarray(a)
    def test_pixels_accept_reference(self):
        self.assertGreater(oracle.check_pixels(self.picture(17,64),17,64,'ntsc'),1500)
    def test_pixels_reject_stuck_speed(self):
        with self.assertRaises(AssertionError):oracle.check_pixels(self.picture(28,100),0,100,'ntsc')
    def test_pixels_reject_stuck_shield(self):
        with self.assertRaises(AssertionError):oracle.check_pixels(self.picture(0,100),0,0,'ntsc')
    def test_pixels_reject_black(self):
        with self.assertRaises(AssertionError):oracle.check_pixels(Image.new('RGB',(434,240)),0,100,'ntsc')
    def test_world_watchdog_excludes_both_huds(self):
        # Native top overlay ends at screenshot y57; footer begins y194 or206.
        source=(R/'tests/vjrunner/vjrun.cpp').read_text()
        self.assertIn('y>110 && y<190',source)
        self.assertLess(8+50,110)
if __name__=='__main__':unittest.main()
