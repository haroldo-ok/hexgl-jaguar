#!/usr/bin/env python3
"""Compile/execute an explicitly separate native-GPU fixture ROM.
All 12 queries call the unchanged production assembly; the host reads RAM only.
This is native unit coverage, not substituted gameplay/physical-hardware evidence.
"""
from pathlib import Path
import shutil,subprocess,hashlib,json,os,re
from native_fx_checks import depth
R=Path(__file__).resolve().parents[1]
W=R.parent/'.cache/native-fx-probe';D=R/'test-results/native-fx-probe'
if W.exists():shutil.rmtree(W)
W.mkdir(parents=True);D.mkdir(parents=True,exist_ok=True)
shutil.copytree(R/'src',W/'src')
for name in ['assets','tests','vendor']:(W/name).symlink_to(R/name,target_is_directory=True)
(W/'tools').mkdir();shutil.copy2(R/'tools/package_rom.py',W/'tools/package_rom.py');(W/'rom').mkdir()
p=W/'src/hexgl.js';p.write_text('FX_SELFTEST EQU 1\n'+p.read_text())
with (D/'build.log').open('w') as log:
 subprocess.run([str(R/'vendor/lyxass/lyxass'),'-sh','hexgl.js'],cwd=W/'src',env={**os.environ,'BJL_ROOT':str(R/'vendor/new_bjl')},stdout=log,stderr=subprocess.STDOUT,check=True)
 subprocess.run(['python3','tools/package_rom.py'],cwd=W,stdout=log,stderr=subprocess.STDOUT,check=True)
symbol=(W/'src/hexgl.equ').read_text()
end=int(re.search(r'MODend_effects\s+EQU \$([0-9a-fA-F]+)',symbol)[1],16)
assert end<0xf03f00,'Diagnostic overlay exceeds stock GPU local RAM'
args=[str(R/'tests/vjrunner/vjrun'),'--symbols',str(W/'src/hexgl.equ'),'--frames','320','--no-bios','--ntsc','--out',str(D),'--quiet',str(W/'rom/hexgl.j64')]
(D/'invocation.json').write_text(json.dumps({'args':args,'production_rom_sha256':hashlib.sha256((R/'rom/hexgl.j64').read_bytes()).hexdigest(),'diagnostic_rom_sha256':hashlib.sha256((W/'rom/hexgl.j64').read_bytes()).hexdigest()},indent=2)+'\n')
with (D/'emulator.log').open('w') as log:subprocess.run(args,cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=180)
t=json.loads((D/'rom_report.json').read_text());last=t['fields'][-1];a=last['fx_aux']
assert a[31]==0x46585054,'Native GPU fixture did not finish'
cases=json.loads((R/'tests/fx_probe_cases.json').read_text())
for i,c in enumerate(cases):
 c['actual']=a[i];assert a[i]==c['expected'],(c['name'],a[i],c['expected'])
assert last['fx_depth'][13]==3,'Behind-plane queries did not actually reject particles'
assert depth(last['fx_depth']) and last['fx_depth'][19]==160,'Perspective varying-Z proof differs'
summary={'status':'PASS','rom_sha256':hashlib.sha256((R/'rom/hexgl.j64').read_bytes()).hexdigest(),'diagnostic_rom_sha256':hashlib.sha256((W/'rom/hexgl.j64').read_bytes()).hexdigest(),'method':'Separate native-GPU fixture ROM, unchanged production fx_occluded assembly, read-only host observations. Not a gameplay trace.','production_depth_source_sha256':hashlib.sha256((R/'src/fx_depth.inc').read_bytes()).hexdigest(),'cases':cases,'actual_occlusion_rejections':last['fx_depth'][13],'varying_vertex_triangle_z':last['fx_depth'][19],'gpu_overlay_end':hex(end)}
(D/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');(D/'ram.bin').unlink(missing_ok=True)
print(json.dumps(summary,indent=2))
