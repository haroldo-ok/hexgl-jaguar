#!/usr/bin/env python3
"""Separate source build and real NTSC/PAL boot checks; produces hash-bound proof."""
from pathlib import Path
import shutil,subprocess,sys,hashlib,json
main=Path(__file__).resolve().parents[1];clean=main.parent/'.cache/dynamics-clean'/main.name
if clean.exists():shutil.rmtree(clean)
def ignore(path,names):
 out=[]
 for n in names:
  p=Path(path)/n
  if n in {'.git','__pycache__','obj','test-results','rom','.cache'} or p.suffix in {'.o','.a','.d','.P','.pyc'}:out.append(n)
  elif p.is_file() and n in {'vjrun','lyxass','build68k','gencpu'}:out.append(n)
 return out
shutil.copytree(main,clean,ignore=ignore)
(clean/'rom').mkdir(exist_ok=True)
log=main/'docs/dynamics-clean-build.log'
with log.open('w') as f:subprocess.run(['make','rom','emulator'],cwd=clean,stdout=f,stderr=subprocess.STDOUT,check=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(clean/'rom/hexgl.j64')==sha(main/'rom/hexgl.j64')
sys.path.insert(0,str(clean/'tests'))
import e2e,motion_checks,dynamics_checks
record={'status':'PASS','rom_sha256':sha(main/'rom/hexgl.j64'),'method':'Separate source tree; removed ROM, GPU payload and generated native host build products. Fresh make rom emulator, byte-identical ROM.','cases':{}}
for standard,extra in [('ntsc',['--no-bios']),('pal',[])]:
 t=e2e.run('clean-'+standard,standard,1200,'100:a+c,120:a',extra)
 e2e.common(t);e2e.countdown(t);e2e.rendered_hud(t)
 record['cases'][standard]={'boot':t['boot_mode'],'fields':1200,'motion':motion_checks.verify_motion(t),'dynamics':dynamics_checks.verify_dynamics(t)}
(main/'docs/dynamics-clean-rebuild.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
