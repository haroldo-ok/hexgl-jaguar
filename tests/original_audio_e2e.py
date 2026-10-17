#!/usr/bin/env python3
"""Controller-only source-stereo boost starts, explicit stop and second restart."""
import json,hashlib
from e2e import R,run,common
from material_checks import audio_sample
m=json.loads((R/'assets/audio.json').read_text())[2]
start=int(m['rom_address'],16);end=start+m['bytes']
summary={'status':'IN_PROGRESS','rom_sha256':hashlib.sha256((R/'rom/hexgl.j64').read_bytes()).hexdigest(),'cases':{}}
path=R/'test-results/original-audio-summary.json';path.write_text(json.dumps(summary))
try:
 for standard in ['ntsc','pal']:
  probe=run('audio-pad-timing-'+standard+'-probe',standard,900,'100:a+c,120:a',['--no-bios']);common(probe)
  pad=next(f['f'] for f in probe['fields'][150:] if f['game'][2]==1 and f['game'][12]>0)
  stop=pad+20;restart=stop+180;again=restart+pad-100;stop2=again+20
  t=run('boost-events-'+standard,standard,stop2+140,f'100:a+c,120:a,{stop}:option,{stop+20}:none,{restart}:a+c,{restart+20}:a,{stop2}:option,{stop2+20}:none',['--no-bios']);common(t)
  fields=t['fields'];episodes=[];stops=[];source_stereo=0;gain_checks=0
  for lo,hi in [(pad-10,stop),(again-10,stop2)]:
   active=[f for f in fields[lo:hi+1] if start<=f['audio_state'][9]<end and f['audio_state'][0] and not f['audio_state'][0]&1]
   assert len(active)>=8,'Controller route did not actually start the source boost stream'
   assert all(b['audio_state'][9]>=a['audio_state'][9] for a,b in zip(active,active[1:])),'One-shot unexpectedly looped'
   assert active[0]['audio_state'][9]<start+2048,'Boost did not restart from its first independent block'
   episodes.append({'first_active_field':active[0]['f'],'observed_active_fields':len(active),'first_cartridge_cursor':hex(active[0]['audio_state'][9])})
   for f in active:
    a=f['audio_state'];source_stereo+=a[3]==0 and a[5]!=a[7] and f['stereo_different']>100
    gain_checks+=audio_sample(a)
  for at in [stop,stop2]:
   stopped=[f for f in fields[at+5:at+60] if f['game'][12]==0 and f['audio_state'][0] and not f['audio_state'][0]&1]
   assert len(stopped)>30,'No completed samples after explicit controller reset'
   assert all(f['audio_state'][9]==end for f in stopped),'Boost kept playing after explicit timer clear'
   stops.append(len(stopped))
  assert source_stereo>=10,'Source channel difference disappeared at zero pan'
  summary['cases'][standard]={'probe_first_pad_field':pad,'boost_episodes':episodes,'completed_zero_timer_stop_samples':stops,'source_stereo_at_zero_pan_fields':source_stereo,'native_stereo_gain_checks':gain_checks,'checks':['actual original-channel boost content at zero pan','real DSP one-shot cursor progression','Option timer-clear stops while stream active','second controller race restarts source at first block','unchanged black/frozen-video and source-HUD gates']}
 summary['status']='PASS'
except Exception as e:
 summary['status']='FAIL';summary['error']=str(e);raise
finally:path.write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
