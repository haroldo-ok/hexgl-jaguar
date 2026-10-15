#!/usr/bin/env python3
"""Resample all five original Ogg files, in full, to Jaguar signed 8-bit PCM."""
from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[1]
offset=0xb00000
manifest=[];equ=[];blob=bytearray()
for name in ['bg','wind','boost','crash','destroyed']:
    p=R/'assets'/f'{name}.s8'
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(R/'vendor/HexGL/audio'/f'{name}.ogg'),'-ac','1','-ar','7990','-f','s8',str(p)],check=True)
    data=p.read_bytes()
    equ.extend([f'{name}_start equ ${offset:x}',f'{name}_end equ ${offset+len(data):x}'])
    manifest.append(dict(name=name,bytes=len(data),rom_address=hex(offset),sample_rate=7990,format='signed PCM8 mono',truncated=False))
    blob+=data;offset+=len(data)
(R/'assets/audio.bin').write_bytes(blob)
(R/'assets/audio.inc').write_text('\n'.join(equ)+'\n')
(R/'assets/audio.json').write_text(json.dumps(manifest,indent=2))
print('Audio:',len(blob),'bytes, end',hex(offset))
