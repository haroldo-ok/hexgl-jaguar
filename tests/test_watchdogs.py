"""Unit tests of the visual assertions. Synthetic traces are unit fixtures only;
positive end-to-end evidence always comes from a fresh emulator execution.
"""
import copy, unittest
import numpy as np
from e2e import common, MAGIC, milliseconds
from gui_e2e import metrics, visible


def healthy():
    fields=[]
    for f in range(400):
        game=[0]*20;game[0]=MAGIC;game[1]=f//3;game[2]=1;game[8]=50
        fields.append(dict(f=f,game=game,world_lit=9000,world_changed=250,audio_samples=f*133,audio_nonzero=400))
    return dict(fields=fields,worst_black_streak=0)

class CoreWatchdog(unittest.TestCase):
    def test_healthy(self):common(healthy())
    def test_black_tail_including_last_field(self):
        r=healthy();r['fields'][-1]['world_lit']=0
        with self.assertRaisesRegex(AssertionError,'World viewport black'):common(r)
    def test_hud_only_cannot_pass(self):
        r=healthy()
        for f in r['fields'][150:]:f['world_lit']=0
        with self.assertRaisesRegex(AssertionError,'World viewport black'):common(r)
    def test_running_telemetry_cannot_hide_frozen_video(self):
        r=healthy()
        for f in r['fields'][150:]:f['world_changed']=0
        with self.assertRaisesRegex(AssertionError,'World framebuffer frozen'):common(r)
    def test_animated_video_cannot_hide_dead_heartbeat(self):
        r=healthy()
        for f in r['fields'][150:]:f['game'][1]=25
        with self.assertRaisesRegex(AssertionError,'heartbeat stalled'):common(r)
    def test_pause_is_allowed_to_be_static(self):
        r=healthy()
        for f in r['fields'][150:]:f['game'][13]=1;f['world_changed']=0
        common(r)
    def test_boot_logo_not_native_game(self):
        r=healthy()
        for f in r['fields']:f['game'][0]=0
        with self.assertRaisesRegex(AssertionError,'native gameplay'):common(r)

class RaceFlow(unittest.TestCase):
    def test_millisecond_format(self):
        self.assertEqual(milliseconds('01:02.345'),62345)
        with self.assertRaises(AssertionError):milliseconds('1:2.3')
    def test_countdown_can_be_static_but_not_black(self):
        r=healthy()
        for f in r['fields']:f['game'][2]=4;f['world_changed']=0
        common(r)
        r['fields'][-1]['world_lit']=0
        with self.assertRaisesRegex(AssertionError,'World viewport black'):common(r)
    def test_finish_can_be_static_but_not_dead(self):
        r=healthy()
        for f in r['fields']:f['game'][2]=3;f['world_changed']=0
        common(r)
        for f in r['fields'][150:]:f['game'][1]=1
        with self.assertRaisesRegex(AssertionError,'heartbeat stalled'):common(r)

class DesktopWatchdog(unittest.TestCase):
    def test_black_rejected(self):self.assertFalse(visible(metrics(np.zeros((80,160,3),dtype=np.uint8))))
    def test_bright_solid_color_rejected(self):self.assertFalse(visible(metrics(np.full((80,160,3),180,dtype=np.uint8))))
    def test_identical_frames_have_zero_motion(self):
        pixels=np.random.default_rng(42).integers(0,255,(80,160,3),dtype=np.uint8)
        self.assertEqual(metrics(pixels,pixels)['changed_fraction'],0)

if __name__=='__main__':unittest.main()
