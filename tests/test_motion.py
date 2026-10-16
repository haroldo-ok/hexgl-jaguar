"""Unit fixtures only; shipped E2E evidence comes from fresh Virtual Jaguar runs."""
import copy, random, unittest
from motion_checks import smooth, verify_motion


def fixture():
    fields=[]
    for i in range(155):
        g=[0]*28;g[0]=0x48455847;g[2]=1;g[5]=1548*256;g[20]=60
        m=[0,0,1612*256,0,0,0,1612*256,3,57,168,99,160,0,1612,-159,0,i+1]
        p=[0,0,0,0,0,0,0,1612,-159,0]
        fields.append(dict(f=i,game=g,motion=m,pose=p))
    return dict(fields=fields)


class MotionMath(unittest.TestCase):
    def test_constant_target_converges_without_sticking(self):
        for target in [-84992,-50176,50176,84992,10240]:
            old=0
            for _ in range(300):old=smooth(old,target,57)
            self.assertEqual(old,target)
    def test_no_overshoot(self):
        for old,target in [(-84992,84992),(84992,-84992),(0,10240),(800000,400000)]:
            for alpha in [20,57,99,168,226]:
                new=smooth(old,target,alpha)
                self.assertLessEqual(min(old,target),new)
                self.assertLessEqual(new,max(old,target))
    def test_split_multiply_matches_wide_integer_reference(self):
        rng=random.Random(42)
        for _ in range(10000):
            old=rng.randrange(-4190000,4190000);target=rng.randrange(-4190000,4190000);alpha=rng.randrange(1,256)
            delta=target-old
            self.assertTrue(-32768<=delta>>8<=32767)
            step=(delta>>8)*alpha+(((delta&255)*alpha+128)>>8)
            if step==0 and delta:step=1 if delta>0 else -1
            self.assertEqual(old+step,smooth(old,target,alpha))
    def test_coefficients_normalize_video_rate(self):
        responses=[]
        for hz in [50,60]:
            state=0;alpha=round(256*(1-.92**(60/hz)))
            for _ in range(hz//2):state=smooth(state,50176,alpha)
            responses.append(state)
        self.assertLess(abs(responses[0]-responses[1]),512)


class MotionOracle(unittest.TestCase):
    def test_healthy_fixture(self):self.assertGreater(verify_motion(fixture())['verified_updates'],0)
    def test_wrong_actual_mesh_angle_rejected(self):
        r=fixture();r['fields'][-1]['pose'][2]=4
        with self.assertRaisesRegex(AssertionError,'renderer roll'):verify_motion(r)
    def test_wrong_actual_camera_rejected(self):
        r=fixture();r['fields'][-1]['pose'][7]+=1
        with self.assertRaisesRegex(AssertionError,'Renderer camera differs'):verify_motion(r)
    def test_wrong_filter_recurrence_rejected(self):
        r=fixture();r['fields'][-1]['motion'][0]=256
        with self.assertRaisesRegex(AssertionError,'Bank filter mismatch'):verify_motion(r)

if __name__=='__main__':unittest.main()
