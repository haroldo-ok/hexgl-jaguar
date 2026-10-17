#!/usr/bin/env python3
"""Additional read-only checks on current-ROM executed dynamics observations."""
from pathlib import Path
import sys,json,gzip,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tests'))
import material_checks as mc
sha=hashlib.sha256((R/'rom/hexgl.j64').read_bytes()).hexdigest()
report={'status':'PASS','rom_sha256':sha,'method':'Post-run analysis of current-ROM read-only dynamics observations; no new emulator run or game RAM write.','cases':{}}
for name in ['dynamics-route-ntsc','dynamics-route-pal','dynamics-drive-ntsc','dynamics-drive-pal']:
 d=R/'test-results'/name
 assert json.loads((d/'invocation.json').read_text())['rom_sha256']==sha
 p=d/'run_report.json';t=json.loads(p.read_text()) if p.exists() else json.loads(gzip.decompress(p.with_suffix('.json.gz').read_bytes()))
 checks=mc.materials(t)
 if name.startswith('dynamics-route'):assert checks['material_banks']==list(range(8)),'All original-map view banks were not rendered'
 report['cases'][name]=checks
(R/'docs/materials-additional-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
