"""Read-only oracles for actual native material, sky and stereo output."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def audio_sample(state):
 seq,left,right,pan,centerL,spatialL,centerR,spatialR,bgPtr,boostPtr=state
 if not seq or seq&1:return False
 assert -112<=pan<=112,'Invalid spatial pan'
 sat=lambda x:max(-32768,min(32767,x))
 assert (left,right)==(sat(centerL+(spatialL*(128-pan)>>7)),sat(centerR+(spatialR*(128+pan)>>7))),'DSP stereo operands differ from native gains'

 return True

def audio(result,both=True):
 fields=result['fields'][150:];checked=sum(audio_sample(f['audio_state']) for f in fields)
 assert checked>len(fields)*.8,'Insufficient completed DSP samples'
 pans=[f['audio_state'][3] for f in fields]
 if both:assert min(pans)<-10 and max(pans)>10,'Both controller-driven stereo directions were not exercised'
 stereo=sum(f['stereo_different']>100 for f in fields)
 assert stereo>5,'Actual emulator stereo PCM remained mono'
 centered=[f for f in fields if f['game'][2]==4 and f['audio_state'][3]==0]
 assert centered and sum(f['stereo_different']<5 for f in centered)>len(centered)*.95,'Centered countdown music is not centered'
 from native_audio_checks import verify_music
 source=verify_music(result)
 return {**source,'completed_dsp_samples_checked':checked,'pan_range':[min(pans),max(pans)],'actual_stereo_fields':stereo}

def materials(result):
 fields=result['fields'][150:];banks=set();lit=0;additions=0;rows=set()
 previous=None
 for f in fields:
  m=f['material_state'];base,bank,count,tex,row=m[:5]
  assert 0<=bank<8 and 0x902000<=base<0x992000,'Invalid ROM material bank'
  assert (0x902000<=tex<0x992000 and (tex-0x902000)%8192==0) or (0x9e0000<=tex<0x9f2000 and (tex-0x9e0000)%8192==0),'Renderer did not consume a source-derived native atlas texture'
  assert 0<=row<=312,'Sky crop outside panorama'
  if previous and m[:2]==previous[:2]:assert base==0x902000+bank*9*8192,'Atlas selection does not match bank'
  if previous and m[9:12]==previous[9:12] and count:
   before,addition,after=m[9:12]
   assert 0<addition<64 and after==min(255,before+addition),'Real face-light accumulator incorrect'
   additions+=1
  banks.add(bank);rows.add(row);lit+=count>0;previous=m
 assert lit>10 and additions>10,'Booster point light never reached scene faces'
 assert len(rows)>3,'Sky never followed changing camera pitch'
 return {'material_banks':sorted(banks),'sky_crop_rows':len(rows),'fields_with_scene_illumination':lit,'face_light_additions_checked':additions}

def sky_pixels(result):
 import numpy as np
 from PIL import Image
 from hud_checks import palette
 from dynamics_checks import trig
 data=np.frombuffer((R/'assets/sky.bin').read_bytes(),dtype='>u2').reshape(512,2048)
 dx,dy=(17,8) if result['video'].lower()=='ntsc' else (18,-4)
 checked=[]
 for path in sorted(Path(result['output_dir']).glob('frame_*.png')):
  n=int(path.stem.split('_')[1]);actual=np.asarray(Image.open(path).convert('RGB'))
  best=0
  for f in result['fields'][max(150,n-16):n+1]:
   if f['game'][2] not in (1,4,5):continue
   co,si=trig(f['physics'][12]>>8)
   shift=abs(si*176)//co
   if si<0:shift=-shift
   row=max(0,min(312,156+shift))
   x=(-f['pose'][9]+np.arange(384))&2047
   codes=data[row+50:row+70,x]
   expected=(palette()[codes>>8]*(codes&255)[...,None])>>8
   crop=actual[50+dy:70+dy,dx:dx+384]
   if crop.shape==expected.shape:best=max(best,int(np.all(expected==crop,axis=2).sum()))
  if best>1000:checked.append({'capture':path.name,'exact_pitch_and_yaw_sky_pixels':best})
 assert len(checked)>=2,'Sky panorama pixels do not match actual camera pitch/yaw'
 return {'sky_pixel_captures':checked}
