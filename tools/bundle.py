#!/usr/bin/env python3
"""Create a source + ROM + evidence archive, excluding host build products."""
from pathlib import Path
import zipfile,hashlib,json
R=Path(__file__).resolve().parents[1]
path=R.parent/'HexGL-Jaguar-source-and-ROM.zip'
summary=json.loads((R/'test-results/summary.json').read_text())
romsha=hashlib.sha256((R/'rom/hexgl.j64').read_bytes()).hexdigest()
assert summary['status']=='PASS' and summary['rom_sha256']==romsha
gui=json.loads((R/'test-results/gui/summary.json').read_text())
assert gui['status']=='PASS' and gui['rom_sha256']==romsha,'Stock GUI regression gate has not passed for this ROM'
skipdirs={'.git','__pycache__','.venv','node_modules','obj','.cache'}
with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(R.rglob('*')):
        if not p.is_file():continue
        rel=p.relative_to(R)
        if any(part in skipdirs for part in rel.parts):continue
        if p.suffix in {'.o','.a','.d','.P','.pyc','.exe','.cof','.abs','.jag'}:continue
        if rel.as_posix() in {'tests/vjrunner/vjrun','vendor/lyxass/lyxass','vendor/HexGL/package.zip'}:continue
        if rel.parts[:3] in [('vendor','lyxass','bin'),('vendor','jag_3d_engine','bin')]:continue
        if p.name.endswith('.log') and rel.parts[0]=='vendor':continue
        z.write(p,Path('hexgl-jaguar')/rel)
print(path, path.stat().st_size, 'bytes')
(R.parent/'HexGL-Jaguar-source-and-ROM.sha256').write_text(hashlib.sha256(path.read_bytes()).hexdigest()+'  '+path.name+'\n')
