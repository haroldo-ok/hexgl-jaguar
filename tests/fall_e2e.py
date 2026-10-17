#!/usr/bin/env python3
"""Dedicated real-input pause-during-falling scenarios for both boot/video paths."""
import hashlib,json
from e2e import R,run,common
from dynamics_checks import verify_fall

def main():
 summary={'status':'IN_PROGRESS','rom_sha256':hashlib.sha256((R/'rom/hexgl.j64').read_bytes()).hexdigest(),'cases':{}}
 path=R/'test-results/fall-summary.json';path.write_text(json.dumps(summary))
 try:
  for standard,hz in [('ntsc',60),('pal',50)]:
   go=100+7*hz
   for boot,extra in [('direct',['--no-bios']),('bios',[])]:
    name='fall-pause-'+standard+'-'+boot
    # Deterministic real-input candidates handle renderer/boot field phase.
    # Every candidate is actually emulated from reset; none patches game RAM.
    first=None
    candidates=[('left',False,40),('right',True,25),('left',True,15),('right',True,15),('right',False,40),('left',True,35),('right',True,35)]
    for direction,brake,duration in candidates:
     script=f'100:a,{go+70}:a+{direction}'+('+b' if brake else '')+f',{go+70+duration}:a'
     key=direction+('b' if brake else '')+str(duration)
     probe=run(name+'-probe-'+key,standard,1300,script,extra);common(probe)
     first=next((f for f in probe['fields'][150:] if f['game'][2]==1 and f['physics'][4]),None)
     if first is not None:break
    assert first is not None,'No actual controller path left the source track'
    fall_pause=first['f']+12
    # There must be no later probe input that could overwrite our pause pulse.
    prefix=','.join(e for e in script.split(',') if int(e.split(':')[0])<fall_pause)
    actual=prefix+f',{fall_pause}:pause,{fall_pause+15}:none,{fall_pause+150}:pause,{fall_pause+165}:none'
    t=run(name,standard,1500,actual,[*extra,'--dump-at',f'{fall_pause+50},{fall_pause+200}']);common(t)
    checks=verify_fall(t)
    assert checks['paused_fall_updates']>20,'Pause did not exercise an actual unsupported fall'
    checks['probe_controller_path']=key
    checks['probe_first_fall_field']=first['f'];checks['controller_pause_field']=fall_pause
    checks['checks']=['controller-triggered unsupported fall','exact PAL/NTSC displacement at capped dt','pause freezes falling for >20 native updates','1.5 active seconds to destruction']
    summary['cases'][name]=checks
  summary['status']='PASS'
 except Exception as e:
  summary['status']='FAIL';summary['error']=str(e);raise
 finally:path.write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
