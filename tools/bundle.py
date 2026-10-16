#!/usr/bin/env python3
"""Create a source + ROM + evidence archive, excluding host build products."""
from pathlib import Path
import zipfile,hashlib,json,gzip
R=Path(__file__).resolve().parents[1]
path=R.parent/'HexGL-Jaguar-source-and-ROM.zip'
summary=json.loads((R/'test-results/summary.json').read_text())
romsha=hashlib.sha256((R/'rom/hexgl.j64').read_bytes()).hexdigest()
assert summary['status']=='PASS' and summary['rom_sha256']==romsha
gui=json.loads((R/'test-results/gui/summary.json').read_text())
assert gui['status']=='PASS' and gui['rom_sha256']==romsha,'Stock GUI regression gate has not passed for this ROM'
hud=json.loads((R/'test-results/hud-summary.json').read_text())
assert hud['status']=='PASS' and hud['rom_sha256']==romsha,'Focused live HUD gate has not passed'
front=json.loads((R/'test-results/frontend-summary.json').read_text())
assert front['status']=='PASS' and front['rom_sha256']==romsha,'Frontend/replay/persistence gate has not passed'
dynamics=json.loads((R/'test-results/dynamics-summary.json').read_text())
assert dynamics['status']=='PASS' and dynamics['rom_sha256']==romsha,'Dynamics/effects gate has not passed'
clean=json.loads((R/'docs/dynamics-clean-rebuild.json').read_text())
assert clean['status']=='PASS' and clean['rom_sha256']==romsha,'Clean rebuild proof is not current'
extra=json.loads((R/'docs/dynamics-additional-checks.json').read_text())
assert extra['status']=='PASS' and extra['rom_sha256']==romsha,'Additional observed-state checks are not current'
# Keep complete per-field evidence, losslessly compressed, in the delivered tree.
# The tests always execute fresh and never consume these saved traces.
for trace in (R/'test-results').rglob('*_report.json'):
    packed=gzip.compress(trace.read_bytes(),compresslevel=6,mtime=0)
    trace.with_suffix(trace.suffix+'.gz').write_bytes(packed)
    trace.unlink()
# Retain representative desktop phases; never prune fault-control screenshots.
# All measured sample metrics stay in result.json; core sampling is separately logged.
retention=R/'test-results/gui/screenshot-retention.json'
record=json.loads(retention.read_text()) if retention.exists() else {'policy':'First and last saved capture per contiguous desktop countdown segment; all moving/fault screenshots and complete metrics retained.','removed':[]}
if record.get('rom_sha256')!=romsha:record['removed']=[]
record['rom_sha256']=romsha
record['policy']='Desktop moving/countdown phases retain first/last saved screenshots; other static phases retain the last saved screenshot. Complete metrics and every negative-control screenshot retained.'
for result in (R/'test-results/gui').glob('*/result.json'):
    if result.parent.name.startswith('negative-'):continue
    samples=json.loads(result.read_text()).get('samples',[])
    segment=[];phase=None
    def trim(segment,phase):
        pictures=[result.parent/f'capture-{i+1:03d}.png' for i in segment]
        pictures=[p for p in pictures if p.exists()]
        if not pictures:return
        keep={pictures[-1]}
        if phase in {'countdown','throttle-autopilot','resume','restart-moving'}:keep.add(pictures[0])
        for p in pictures:
            if p not in keep:
                record['removed'].append({'path':str(p.relative_to(R/'test-results/gui')),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
                p.unlink()
    for i,sample in enumerate(samples):
        if phase!=sample['phase']:
            trim(segment,phase);segment=[];phase=sample['phase']
        segment.append(i)
    trim(segment,phase)
retention.write_text(json.dumps(record,indent=2)+'\n')
# Sample old core screenshots without discarding any per-field trace or verdict.
# Keep countdown glyphs, final frame, bank examples, and representative gauge states.
core_retention=R/'test-results/screenshot-retention.json'
pruned=json.loads(core_retention.read_text()) if core_retention.exists() else {}
if pruned.get('rom_sha256')!=romsha:pruned={'rom_sha256':romsha,'policy':'Representative core screenshots; every per-field trace and executed assertion result retained. Frontend feature screenshots are retained.','removed':[]}
evidence=dict(summary.get('bitmap_hud',{}))
for name,case in hud['cases'].items():evidence['hud-live-'+name]=case['bitmap_hud']
for name,case in evidence.items():
    directory=R/'test-results'/name
    keep={'frame_00180.png','frame_00280.png','frame_00580.png','final.png'}
    for frame in summary['cases'].get(name,{}).get('capture_fields',{}).values():keep.add(f'frame_{frame:05d}.png')
    captures=case.get('captures',[])
    for predicate in [lambda c:c['speed']==0,lambda c:0<c['speed']<28,lambda c:c['speed']==28,lambda c:c['shield']==100,lambda c:0<c['shield']<100,lambda c:c['shield']==0]:
        found=next((c for c in captures if predicate(c)),None)
        if found:keep.add(found['capture'])
    for image in directory.glob('frame_*.png'):
        if image.name not in keep:
            pruned['removed'].append({'path':str(image.relative_to(R/'test-results')),'sha256':hashlib.sha256(image.read_bytes()).hexdigest()})
            image.unlink()
core_retention.write_text(json.dumps(pruned,indent=2)+'\n')
skipdirs={'.git','__pycache__','.venv','node_modules','obj','.cache'}
with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(R.rglob('*')):
        if not p.is_file():continue
        rel=p.relative_to(R)
        if any(part in skipdirs for part in rel.parts):continue
        if p.suffix in {'.o','.a','.d','.P','.pyc','.exe','.cof','.abs','.jag'}:continue
        if rel.as_posix() in {'tests/vjrunner/vjrun','vendor/lyxass/lyxass','vendor/HexGL/package.zip','vendor/virtualjaguar/src/m68000/build68k','vendor/virtualjaguar/src/m68000/gencpu'}:continue
        if rel.parts[:3] in [('vendor','lyxass','bin'),('vendor','jag_3d_engine','bin')]:continue
        if p.name.endswith('.log') and rel.parts[0]=='vendor':continue
        z.write(p,Path('hexgl-jaguar')/rel)
print(path, path.stat().st_size, 'bytes')
(R.parent/'HexGL-Jaguar-source-and-ROM.sha256').write_text(hashlib.sha256(path.read_bytes()).hexdigest()+'  '+path.name+'\n')
