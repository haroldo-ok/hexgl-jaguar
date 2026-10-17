#!/usr/bin/env python3
"""Additional read-only checks on current-ROM complete race observations."""
from pathlib import Path
import json,gzip,hashlib
R=Path(__file__).resolve().parents[1]
sha=hashlib.sha256((R/'rom/hexgl.j64').read_bytes()).hexdigest()
m=json.loads((R/'assets/audio.json').read_text())[2]
start=int(m['rom_address'],16);end=start+m['bytes']
report={'status':'PASS','rom_sha256':sha,'method':'Independent post-run current-ROM complete-race checks; no emulator/game-RAM writes.','cases':{}}
for standard in ['ntsc','pal']:
 d=R/'test-results'/('race-'+standard)
 assert json.loads((d/'invocation.json').read_text())['rom_sha256']==sha
 p=d/'run_report.json';t=json.loads(p.read_text()) if p.exists() else json.loads(gzip.decompress(p.with_suffix('.json.gz').read_bytes()))
 active=monotonic=stopped=nonlooping=center_stereo=0;previous=None
 for f in t['fields'][150:]:
  a=f['audio_state'];flag=f['game'][12];ptr=a[9]
  if not a[0] or a[0]&1:continue
  assert start<=ptr<=end,'DSP boost cursor outside complete source stream'
  active+=ptr<end
  nonlooping+=ptr==end and flag>0
  center_stereo+=a[3]==0 and a[5]!=a[7] and f['stereo_different']>100
  if previous:
   old=previous['audio_state'][9];oldflag=previous['game'][12]
   if not flag and not oldflag and f['f']-previous['f']<3:
    assert ptr==end,'Boost did not stop when its controller timer cleared'
    stopped+=1
   if flag>0 and oldflag>=flag and old<end:
    assert ptr>=old,'Boost source looped without a rising/retrigger event'
    monotonic+=1
  previous=f
 assert active>50 and monotonic>50 and stopped>300,'Native boost cursor/active-timer stop behavior not exercised'
 # Both music/wind sources are dual-mono; boost contains genuine L/R content.
 # Require at least 80% of one source-duration/normalized boost interval.
 # Expiry may now stop the 1.592-second source before its natural end; the
 # obsolete assisted infinite-latch/ended-under-held-signal condition is not a gate.
 expected_fields=min(m['frames']/7990*(60 if standard=='ntsc' else 50),(60 if standard=='ntsc' else 50)*1.5)
 assert center_stereo>expected_fields*.8,'Independent source-channel boost content at zero balance not exercised'
 report['cases'][standard]={'active_boost_dsp_fields':active,'monotonic_nonlooping_cursor_checks':monotonic,'zero_timer_stops_checked':stopped,'observed_ended_one_shot_while_timer_positive_fields':nonlooping,'original_spatial_channel_difference_at_zero_pan_fields':center_stereo}
(R/'docs/particles-audio-additional-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
