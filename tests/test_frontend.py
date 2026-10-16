"""Unit fixtures are not substituted for fresh emulator evidence."""
import unittest,hashlib,json,struct,random,tempfile
from pathlib import Path
from PIL import Image
import numpy as np
import frontend_checks as fc
R=Path(__file__).resolve().parents[1]
class FrontendTests(unittest.TestCase):
    def test_source_assets(self):
        m=json.loads((R/'assets/frontend.json').read_text())
        for p,h in m['sources'].items():self.assertEqual(hashlib.sha256((R/p).read_bytes()).hexdigest(),h)
        for p,h in m['outputs'].items():self.assertEqual(hashlib.sha256((R/'assets'/p).read_bytes()).hexdigest(),h)
    def test_all_original_font_glyphs(self):
        raw=(R/'assets/front-font.bin').read_bytes();widths=(R/'assets/front-widths.bin').read_bytes()
        self.assertEqual(len(raw),96*48)
        for i in range(96):
            expected,advance=fc.glyph(chr(32+i));words=struct.unpack_from('>24H',raw,i*48)
            actual=np.array([[(word>>(15-x))&1 for x in range(16)] for word in words],bool)
            self.assertTrue(np.array_equal(actual,expected));self.assertEqual(widths[i],advance)
    def test_font_oracle_rejects_black(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'black.png';Image.new('RGB',(434,240)).save(p)
            with self.assertRaises(AssertionError):fc.text_pixels(p,'MANUAL BEST',126,61)
    def test_valid_journal(self):
        d=bytearray(b'\xff'*128);d[:16]=fc.encode(1,180000,59000)
        self.assertEqual(fc.choose(d,0)['total_ms'],180000);self.assertIsNone(fc.choose(d,16))
    def test_torn_commit(self):
        d=bytearray(b'\xff'*128);d[:16]=fc.encode(1,180000,59000);d[16:32]=fc.encode(2,170000,57000);d[16:18]=b'\0\0'
        self.assertEqual(fc.choose(d,0)['generation'],1)
    def test_bad_checksum(self):
        d=bytearray(b'\xff'*128);d[:16]=fc.encode(1,180000,59000);d[10]^=1
        self.assertIsNone(fc.choose(d,0))
    def test_generation_wrap(self):
        d=bytearray(b'\xff'*128);d[:16]=fc.encode(65535,180000,59000);d[16:32]=fc.encode(0,170000,57000)
        self.assertEqual(fc.choose(d,0)['slot'],8)
    def test_journal_score_bounds(self):
        for total,lap in [(0,0),(6000000,100),(100,101),(100,0)]:self.assertIsNone(fc.decode_slot(fc.encode(1,total,lap),0))
    def test_replay_split_multiply(self):
        rng=random.Random(4190)
        for _ in range(10000):
            delta=rng.randrange(-8388608,8388608);alpha=rng.randrange(256)
            self.assertEqual((delta>>8)*alpha+((delta&255)*alpha>>8),delta*alpha//256)
    def test_shortest_heading(self):
        self.assertEqual((0-2044+1024)%2048-1024,4)
        self.assertEqual((2044-0+1024)%2048-1024,-4)
    def test_record_buffer_bounds(self):
        self.assertGreater(0x150000,0x14acc8)
        self.assertEqual(0x150000+6144*64,0x1b0000)
        self.assertLess(0x1b0000,0x1b4800)
if __name__=='__main__':unittest.main()
