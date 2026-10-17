#!/usr/bin/env python3
"""Additional independent checks on traces from the current executed ROM.
No emulation or RAM writes occur here; inputs are explicitly archived observations.
"""
from pathlib import Path
import sys,json,gzip,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tests'))
import dynamics_checks as dc,frontend_checks as fc
sha=hashlib.sha256((R/'rom/hexgl.j64').read_bytes()).hexdigest()
report={'status':'PASS','rom_sha256':sha,'method':'Independent post-run checks of current-ROM recorded observations; original E2E invocations retained.','cases':{}}
for name in ['fall-pause-ntsc-direct','fall-pause-ntsc-bios','fall-pause-pal-direct','fall-pause-pal-bios','replay-ntsc','replay-pal']:
 d=R/'test-results'/name
 assert json.loads((d/'invocation.json').read_text())['rom_sha256']==sha
 p=d/'run_report.json';t=json.loads(p.read_text()) if p.exists() else json.loads(gzip.decompress(p.with_suffix('.json.gz').read_bytes()))
 t['output_dir']=str(d)
 if name.startswith('fall-pause'):
  checks=dc.verify_fall(t);assert checks['paused_fall_updates']>20,'Pause during actual falling not exercised'
 else:checks=fc.replay(t)
 report['cases'][name]=checks
(R/'docs/dynamics-additional-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
