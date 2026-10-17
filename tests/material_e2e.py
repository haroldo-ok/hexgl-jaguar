#!/usr/bin/env python3
"""Fresh controller-only NTSC/PAL tests of rendering and actual stereo PCM."""
import hashlib,json
from e2e import R,run,common
import material_checks as mc

def main():
 summary={'status':'IN_PROGRESS','rom_sha256':hashlib.sha256((R/'rom/hexgl.j64').read_bytes()).hexdigest(),'cases':{}}
 path=R/'test-results/material-summary.json';path.write_text(json.dumps(summary))
 try:
  for standard,hz in [('ntsc',60),('pal',50)]:
   go=100+7*hz
   script=f'100:a,{go+40}:a+b+left,{go+55}:a,{go+65}:a+b+right,{go+85}:a'
   shots=','.join(str(n) for n in [180,go+30,go+50,go+60,go+80,go+100,go+130])
   t=run('materials-'+standard,standard,1300,script,['--no-bios','--dump-at',shots,'--dump-max','24']);common(t)
   case=mc.audio(t);case.update(mc.materials(t));case.update(mc.sky_pixels(t))
   case['checks']=['actual interleaved stereo PCM','left/right native spatial bus and centered music','signed saturating DSP gain arithmetic','runtime ROM atlas addresses','real scene-face point-light addition','exact camera-dependent sky framebuffer pixels including seam wrap']
   summary['cases'][standard]=case
  summary['status']='PASS'
 except Exception as e:
  summary['status']='FAIL';summary['error']=str(e);raise
 finally:path.write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
