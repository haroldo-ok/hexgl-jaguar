#!/usr/bin/env python3
"""Create a source + ROM + evidence archive, excluding host build products."""
from pathlib import Path
import zipfile,hashlib,json,gzip
R=Path(__file__).resolve().parents[1]
path=R.parent/'HexGL-Jaguar-source-and-ROM.zip'
summary=json.loads((R/'test-results/summary.json').read_text())
romsha=hashlib.sha256((R/'rom/hexgl.j64').read_bytes()).hexdigest()
pa=json.loads((R/'docs/particles-audio-additional-checks.json').read_text())
assert pa['status']=='PASS' and pa['rom_sha256']==romsha
probe=json.loads((R/'test-results/native-fx-probe/summary.json').read_text())
assert probe['status']=='PASS' and probe['rom_sha256']==romsha
assert probe['production_depth_source_sha256']==hashlib.sha256((R/'src/fx_depth.inc').read_bytes()).hexdigest()

assert summary['status']=='PASS' and summary['rom_sha256']==romsha
gui=json.loads((R/'test-results/gui/summary.json').read_text())
assert gui['status']=='PASS' and gui['rom_sha256']==romsha,'Stock GUI regression gate has not passed for this ROM'
hud=json.loads((R/'test-results/hud-summary.json').read_text())
assert hud['status']=='PASS' and hud['rom_sha256']==romsha,'Focused live HUD gate has not passed'
front=json.loads((R/'test-results/frontend-summary.json').read_text())
assert front['status']=='PASS' and front['rom_sha256']==romsha,'Frontend/replay/persistence gate has not passed'
dynamics=json.loads((R/'test-results/dynamics-summary.json').read_text())
assert dynamics['status']=='PASS' and dynamics['rom_sha256']==romsha,'Dynamics/effects gate has not passed'
original_audio=json.loads((R/'test-results/original-audio-summary.json').read_text())
assert original_audio['status']=='PASS' and original_audio['rom_sha256']==romsha,'Original-channel audio/event gate is not current'
materials=json.loads((R/'test-results/material-summary.json').read_text())
assert materials['status']=='PASS' and materials['rom_sha256']==romsha,'Native materials/stereo gate has not passed'
fall=json.loads((R/'test-results/fall-summary.json').read_text())
assert fall['status']=='PASS' and fall['rom_sha256']==romsha,'Dedicated fall/pause gate has not passed'
gameplay=json.loads((R/'test-results/gameplay-summary.json').read_text())
assert gameplay['status']=='PASS' and gameplay['rom_sha256']==romsha,'Gameplay feature gate is not current'
additional_remaining=json.loads((R/'docs/remaining-additional-checks.json').read_text())
assert additional_remaining['status']=='PASS' and additional_remaining['rom_sha256']==romsha,'Native subsystem additional proofs are not current'
remaining=json.loads((R/'test-results/remaining-summary.json').read_text())
assert remaining['status']=='PASS' and remaining['rom_sha256']==romsha and len(remaining['cases'])==6,'New native subsystem gate is not current'
clean=json.loads((R/'docs/dynamics-clean-rebuild.json').read_text())
assert clean['status']=='PASS' and clean['rom_sha256']==romsha,'Clean rebuild proof is not current'
extra=json.loads((R/'docs/dynamics-additional-checks.json').read_text())
assert extra['status']=='PASS' and extra['rom_sha256']==romsha,'Additional observed-state checks are not current'
extra_materials=json.loads((R/'docs/materials-additional-checks.json').read_text())
assert extra_materials['status']=='PASS' and extra_materials['rom_sha256']==romsha,'Recorded material-bank proof is not current'
extra_gameplay=json.loads((R/'docs/gameplay-additional-checks.json').read_text())
assert extra_gameplay['status']=='PASS' and extra_gameplay['rom_sha256']==romsha,'Recorded gameplay proof is not current'
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
record['policy']='Desktop retains the last saved capture of idle, countdown, throttle-autopilot, pause and restart-moving phases. Complete measured metrics and every negative-control screenshot retained.'
for result in (R/'test-results/gui').glob('*/result.json'):
    if result.parent.name.startswith('negative-'):continue
    samples=json.loads(result.read_text()).get('samples',[])
    by_phase={}
    for i,sample in enumerate(samples):
        picture=result.parent/f'capture-{i+1:03d}.png'
        if picture.exists() and sample['phase'] in {'idle','countdown','throttle-autopilot','pause','restart-moving'}:
            by_phase[sample['phase']]=picture
    keep=set(by_phase.values())
    if not keep:continue
    for p in result.parent.glob('capture-*.png'):
        if p not in keep:
            record['removed'].append({'path':str(p.relative_to(R/'test-results/gui')),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
            p.unlink()
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
# Calibration probes and static EEPROM fixtures retain final imagery plus every
# complete trace, invocation and metric; these are not claimed as moving scenes.
static_path=R/'test-results/static-screenshot-retention.json'
static_record=json.loads(static_path.read_text()) if static_path.exists() else {}
if static_record.get('rom_sha256')!=romsha:static_record={'rom_sha256':romsha,'removed':[]}
static_record['policy']='Calibration probes, journal fixtures and fresh-process save-reboot runs retain final.png. Every field trace, invocation, metric and original verdict is retained. All actual fall/pause and material/sky/stereo captures retained.'
for directory in (R/'test-results').iterdir():
    if not directory.is_dir():continue
    if not (directory.name.endswith('-probe') or '-probe-' in directory.name or 'calibration-' in directory.name or directory.name.startswith(('journal-','save-reboot-'))):continue
    for p in directory.glob('frame_*.png'):
        static_record['removed'].append({'path':str(p.relative_to(R/'test-results')),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
        p.unlink()
static_path.write_text(json.dumps(static_record,indent=2)+'\n')
# Keep a compact, auditable source bundle. All per-field traces and verdicts are
# retained; repeated controller/HUD screenshots are sampled with original hashes.
# Preserve every asserted race-banner glyph, composed-FX pixel capture and sky
# pixel proof, plus the images embedded in REPORT.html. Never sample fault cases.
extra_path=R/'test-results/gameplay-screenshot-retention.json'
ret=json.loads(extra_path.read_text()) if extra_path.exists() else {}
if ret.get('rom_sha256')!=romsha:ret={'rom_sha256':romsha,'removed':[]}
ret['policy']='Representative repeated HUD/controller captures; all per-field traces, executed pixel-verdict metrics, source-font race banners, exact composed-FX captures, sky captures and fault-control images retained. Removed PNG hashes recorded.'
plans={}
for std,hz in [('ntsc',60),('pal',50)]:
    go=100+7*hz
    plans['handling-'+std]={'frame_00180.png','frame_00580.png','frame_00800.png','final.png'}
    plans['boost-'+std]={'frame_00180.png','frame_00580.png','frame_00800.png','final.png'}
    plans['boost-events-'+std]={'frame_00180.png','frame_00800.png','frame_01200.png','final.png'}
    plans['views-'+std]={'final.png',*(c['capture'] for c in gameplay['cases']['views-'+std]['source_font_banner_captures']),*(f'frame_{go+n:05d}.png' for n in [300,450,600])}
    settings_go=600+7*hz
    plans['settings-'+std]={'frame_00520.png','frame_00680.png','frame_00800.png',f'frame_{settings_go+100:05d}.png',f'frame_{settings_go+230:05d}.png','final.png'}
    plans['view-replay-'+std]={'frame_01040.png','frame_01140.png','frame_01250.png','frame_01460.png','frame_01550.png','final.png'}
    plans['replay-'+std]={'frame_00880.png','frame_01040.png','frame_01140.png','frame_01250.png','frame_01460.png','frame_01550.png','final.png'}
    plans['menu-'+std]={'frame_00080.png','frame_00180.png','frame_00380.png','frame_00580.png','frame_00880.png','final.png'}
    plans['dynamics-drive-'+std]={'final.png',*dynamics['cases']['dynamics-drive-'+std]['exact_composed_framebuffer_captures']}
    plans['dynamics-route-'+std]={'frame_00580.png','frame_00800.png','frame_01200.png','final.png'}
    captures=hud['cases'][std]['bitmap_hud']['captures']
    keep={'frame_00180.png','frame_00280.png','final.png'}
    for field in ['speed','shield']:
        keep.add(min(captures,key=lambda c:c[field])['capture'])
        keep.add(max(captures,key=lambda c:c[field])['capture'])
    partial=[c for c in captures if 0<c['speed']<28]
    for i in [0,len(partial)//2,len(partial)-1]:
        if partial:keep.add(partial[i]['capture'])
    plans['hud-live-'+std]=keep
for name,c in fall['cases'].items():
    pause=c['controller_pause_field']
    plans[name]={'frame_00180.png','frame_00280.png',f'frame_{pause+50:05d}.png',f'frame_{pause+200:05d}.png','final.png'}
for std in ['ntsc','pal']:
    plans['remaining-menu-'+std]={'frame_00200.png','frame_00570.png','final.png'}
for name,keep in plans.items():
    directory=R/'test-results'/name
    for p in directory.glob('*.png'):
        if p.name not in keep:
            ret['removed'].append({'path':str(p.relative_to(R/'test-results')),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
            p.unlink()
extra_path.write_text(json.dumps(ret,indent=2)+'\n')
# Pixel-identical repeated menus/countdowns need only one PNG payload. Unlike
# sampling unique pictures, these aliases are fully restorable, byte-for-byte.
alias_path=R/'test-results/capture-aliases.json'
aliases=json.loads(alias_path.read_text()) if alias_path.exists() else {}
if aliases.get('rom_sha256')!=romsha:aliases={'rom_sha256':romsha,'aliases':{}}
aliases['policy']='Only byte-identical duplicate PNGs. Canonical PNG and SHA-256 retained. tools/restore_capture_duplicates.py restores aliases losslessly. Source-font/FX/sky pixel proofs, report images and fault captures remain at their original paths.'
protected=set()
for directory in (R/'test-results').iterdir():
    if directory.is_dir() and directory.name.startswith(('negative-','journal-','materials-','menu-','settings-','save-reboot-')):
        protected.update(directory.rglob('*.png'))
protected.update((R/'test-results/gui').rglob('*.png'))
for std in ['ntsc','pal']:
    protected.update(R/'test-results'/('views-'+std)/c['capture'] for c in gameplay['cases']['views-'+std]['source_font_banner_captures'])
    protected.update(R/'test-results'/('dynamics-drive-'+std)/n for n in dynamics['cases']['dynamics-drive-'+std]['exact_composed_framebuffer_captures'])
# Keep every newly asserted source-sky / actual-shadow / native-bloom pixel proof.
for name,case in remaining['cases'].items():
    directory=R/'test-results'/('remaining-'+name)
    for key in ['rolled_sky_pixel_captures','actual_bloom_pixels','actual_shadow_pixels']:
        protected.update(directory/item['capture'] for item in case.get(key,[]))
protected.update((R/'test-results/remaining-menu-ntsc').glob('*.png'))
protected.update((R/'test-results/remaining-menu-pal').glob('*.png'))
for match in __import__('re').findall(r"picture\('([^']+)'",(R/'tools/frontend_report.py').read_text()):
    protected.add(R/'test-results'/match)
groups={}
for p in (R/'test-results').rglob('*.png'):
    groups.setdefault(hashlib.sha256(p.read_bytes()).hexdigest(),[]).append(p)
for digest,files in groups.items():
    if len(files)<2:continue
    canonical=min(files,key=lambda p:(p not in protected,str(p)))
    for p in files:
        if p==canonical or p in protected:continue
        aliases['aliases'][str(p.relative_to(R/'test-results'))]={'canonical':str(canonical.relative_to(R/'test-results')),'sha256':digest}
        p.unlink()
alias_path.write_text(json.dumps(aliases,indent=2)+'\n')
skipdirs={'.git','__pycache__','.venv','node_modules','obj','.cache'}
with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(R.rglob('*')):
        if not p.is_file():continue
        rel=p.relative_to(R)
        if any(part in skipdirs for part in rel.parts):continue
        if rel.parts[0]=='vendor' and p.suffix=='.j64':continue
        if p.suffix in {'.o','.a','.d','.P','.pyc','.exe','.cof','.abs','.jag'}:continue
        if rel.as_posix() in {'tests/vjrunner/vjrun','vendor/lyxass/lyxass','vendor/HexGL/package.zip','vendor/virtualjaguar/src/m68000/build68k','vendor/virtualjaguar/src/m68000/gencpu'}:continue
        if rel.parts[:3] in [('vendor','lyxass','bin'),('vendor','jag_3d_engine','bin')]:continue
        if p.name.endswith('.log') and rel.parts[0]=='vendor':continue
        z.write(p,Path('hexgl-jaguar')/rel)
print(path, path.stat().st_size, 'bytes')
(R.parent/'HexGL-Jaguar-source-and-ROM.sha256').write_text(hashlib.sha256(path.read_bytes()).hexdigest()+'  '+path.name+'\n')
