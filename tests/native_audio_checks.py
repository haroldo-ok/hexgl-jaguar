"""Independent IMA4 reader: no imports from the production audio converter."""
from pathlib import Path
from functools import lru_cache
from array import array
import struct,json
R=Path(__file__).resolve().parents[1]
STEP=(7,8,9,10,11,12,13,14,16,17,19,21,23,25,28,31,34,37,41,45,50,55,60,66,73,80,88,97,107,118,130,143,157,173,190,209,230,253,279,307,337,371,408,449,494,544,598,658,724,796,876,963,1060,1166,1282,1411,1552,1707,1878,2066,2272,2499,2749,3024,3327,3660,4026,4428,4871,5358,5894,6484,7132,7845,8630,9493,10442,11487,12635,13899,15289,16818,18500,20350,22385,24623,27086,29794,32767)
INDEX=(-1,-1,-1,-1,2,4,6,8)

def nibble(code,predict,index):
 step=STEP[index]
 delta=(step//8)+((step//4) if code%2 else 0)+((step//2) if code&2 else 0)+(step if code&4 else 0)
 predict=max(-32768,min(32767,predict+(-delta if code>=8 else delta)))
 return predict,max(0,min(88,index+INDEX[code%8]))

def decode_stream(data):
 samples=array('h');cursor=0
 while cursor<len(data):
  assert cursor+8<len(data),'Truncated stereo block header'
  pl,il,pr,ir=struct.unpack_from('>hHhH',data,cursor);cursor+=8
  assert il<=88 and ir<=88,'Invalid IMA index'
  for packed in data[cursor:cursor+2048]:
   pl,il=nibble(packed//16,pl,il);pr,ir=nibble(packed%16,pr,ir)
   samples.extend((pl,pr))
  cursor+=min(2048,len(data)-cursor)
 return samples

def read_stream(name):
 m=next(m for m in json.loads((R/'assets/audio.json').read_text()) if m['name']==name)
 offset=int(m['rom_address'],16)-0xb00000
 return (R/'assets/audio.bin').read_bytes()[offset:offset+m['bytes']]

@lru_cache(None)
def bg():return decode_stream(read_stream('bg'))

def verify_music(result):
 samples=bg();checked=0;differences=0
 for f in result['fields'][150:]:
  a=f['audio_state'];g=f['game']
  if not a[0] or a[0]&1 or g[2] not in (1,4):continue
  pos=a[8]-0xb00000
  if not pos:continue # wrap publishes next block pointer after the last sample
  block,within=divmod(pos,2056)
  assert within==0 or within>=9,'Committed music pointer lies inside a block header'
  frame=block*2048-1 if within==0 else block*2048+within-9
  assert 0<=frame<len(samples)//2,'Music pointer outside original complete stream'
  expected=(samples[2*frame]>>2,samples[2*frame+1]>>2)
  assert (a[4],a[6])==expected,('DSP decoded source sample/channel differs',f['f'],a[4:7:2],expected)
  differences+=expected[0]!=expected[1];checked+=1
 assert checked>100,'No original-source DSP sample arithmetic evidence'
 return {'exact_original_music_adpcm_samples':checked,'music_stereo_content_samples':differences}
