#!/usr/bin/env python3
"""Full-duration stereo IMA ADPCM, 2048-frame independent native blocks.
One byte per stereo frame, eight-byte big-endian predictor/index block headers.
"""
from pathlib import Path
import subprocess,json,math,struct,hashlib
R=Path(__file__).resolve().parents[1]
STEPS=[7,8,9,10,11,12,13,14,16,17,19,21,23,25,28,31,34,37,41,45,50,55,60,66,73,80,88,97,107,118,130,143,157,173,190,209,230,253,279,307,337,371,408,449,494,544,598,658,724,796,876,963,1060,1166,1282,1411,1552,1707,1878,2066,2272,2499,2749,3024,3327,3660,4026,4428,4871,5358,5894,6484,7132,7845,8630,9493,10442,11487,12635,13899,15289,16818,18500,20350,22385,24623,27086,29794,32767]
DELTA=[-1,-1,-1,-1,2,4,6,8]
BLOCK=2048

def decode(code,predictor,index):
 step=STEPS[index];diff=step>>3
 if code&1:diff+=step>>2
 if code&2:diff+=step>>1
 if code&4:diff+=step
 if code&8:diff=-diff
 return max(-32768,min(32767,predictor+diff)),max(0,min(88,index+DELTA[code&7]))

def encode(value,predictor,index):
 delta=value-predictor;code=8 if delta<0 else 0;delta=abs(delta);step=STEPS[index]
 for flag,threshold in [(4,step),(2,step>>1),(1,step>>2)]:
  if delta>=threshold:code|=flag;delta-=threshold
 return code,*decode(code,predictor,index)

def convert(samples):
 out=bytearray();predict=[0,0];index=[0,0];decoded=[]
 for i in range(0,len(samples),2):
  if i//2%BLOCK==0:out+=struct.pack('>hHhH',predict[0],index[0],predict[1],index[1])
  codes=[]
  for channel in range(2):
   code,predict[channel],index[channel]=encode(samples[i+channel],predict[channel],index[channel]);codes.append(code);decoded.append(predict[channel])
  out.append(codes[0]<<4|codes[1])
 return bytes(out),decoded

def main():
 offset=0xb00000;manifest=[];equ=[];blob=bytearray()
 for name in ['bg','wind','boost','crash','destroyed']:
  source=R/'vendor/HexGL/audio'/f'{name}.ogg'
  pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(source),'-ac','2','-ar','7990','-f','s16be','pipe:1'])
  samples=struct.unpack('>'+str(len(pcm)//2)+'h',pcm)
  data,decoded=convert(samples)
  while len(blob)%8:blob.append(0);offset+=1
  equ.extend([f'{name}_start equ ${offset:x}',f'{name}_end equ ${offset+len(data):x}'])
  signal=sum(v*v for v in samples);noise=sum((a-b)**2 for a,b in zip(samples,decoded))
  manifest.append(dict(name=name,bytes=len(data),frames=len(samples)//2,rom_address=hex(offset),sample_rate=7990,channels=2,block_frames=BLOCK,format='interleaved stereo IMA4 with big-endian predictor/index block headers',truncated=False,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),sha256=hashlib.sha256(data).hexdigest(),snr_db=round(10*math.log10(signal/max(1,noise)),2)))
  blob+=data;offset+=len(data)
 assert len(blob)<=0x100000,'Stereo audio exceeds stock cartridge slot'
 (R/'assets/audio.bin').write_bytes(blob)
 (R/'assets/audio.inc').write_text('\n'.join(equ)+'\n')
 (R/'assets/audio.json').write_text(json.dumps(manifest,indent=2)+'\n')
 (R/'assets/adpcm.inc').write_text(' align 4\nadpcm_steps:\n dc.l '+','.join(map(str,STEPS))+'\nadpcm_delta:\n dc.l '+','.join(map(str,DELTA))+'\n')
 for pattern in ['*.s8','*.adpcm']:
  for p in (R/'assets').glob(pattern):p.unlink()
 print('Full-duration source stereo:',len(blob),'bytes, end',hex(offset))
if __name__=='__main__':main()
