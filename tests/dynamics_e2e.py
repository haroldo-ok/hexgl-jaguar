#!/usr/bin/env python3
"""All inputs are real controller events; observe physics, GPU vertices and particles."""
import json,hashlib
from e2e import R,run,common
import dynamics_checks as dc

def main():
 summary={'status':'IN_PROGRESS','rom_sha256':hashlib.sha256((R/'rom/hexgl.j64').read_bytes()).hexdigest(),'cases':{}}
 path=R/'test-results/dynamics-summary.json';path.write_text(json.dumps(summary))
 try:
  for standard,h in [('ntsc',60),('pal',50)]:
   go=100+7*h
   script=f'100:a,{go+70}:a+b+left,{go+85}:a,{go+150}:pause,{go+165}:none,{go+210}:pause,{go+225}:a'
   shots=','.join(map(str,[go+55,go+100,go+130,go+145,go+250,go+280,go+310]))
   name='dynamics-drive-'+standard
   t=run(name,standard,1600,script,['--no-bios','--effects','--dump-max','24','--dump-at',shots]);common(t)
   case=dc.verify_dynamics(t);case.update(dc.verify_fall(t));case.update(dc.verify_particles(t));case.update(dc.source_sprite_pixels(t))
   assert case['drifting_updates']>2 and case['repulsion_updates']>2 and case['fall_updates']>5,'Drift/contact/fall not exercised'
   assert t['fields'][-1]['game'][2]==2,'Unsupported fall did not end in destruction'
   case['checks']=['airbrake lateral force','contact recoil','bilinear hover','active-time fall/destruction','real ship/camera vertex and projection','original sprite pixels','bounded world-space spark/cloud emitters','lifetime integration','particle pause']
   summary['cases'][name]=case
   name='dynamics-route-'+standard
   t=run(name,standard,3000,'100:a+c,120:a',['--no-bios']);common(t)
   case=dc.verify_dynamics(t)
   assert max(abs(f['physics'][6]) for f in t['fields'][150:])>1024,'Terrain pitch never moved'
   assert len({f['physics'][8] for f in t['fields'][600:]})>50,'Bilinear terrain heights never changed'
   case['checks']=['source-map slopes','actual pitched GPU mesh and look-at camera','bilinear hover over varied track heights','bounded PAL/NTSC response']
   summary['cases'][name]=case
  summary['status']='PASS'
 except Exception as e:
  summary['status']='FAIL';summary['error']=str(e);raise
 finally:path.write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
