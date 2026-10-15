#!/usr/bin/env python3
"""ROM structure, conversion coverage, memory/size and input integrity checks."""
from pathlib import Path
import struct,hashlib,json,re
R=Path(__file__).resolve().parents[1]
rom=(R/'rom/hexgl.j64').read_bytes();payload=(R/'src/hexgl.o').read_bytes()
loader=(R/'vendor/jag_3d_engine/loader/sbl.XXX').read_bytes()
assert len(rom)==6*1024*1024
assert rom[:0x404]==loader[:0x404] and rom[0x408:len(loader)]==loader[0x408:]
assert struct.unpack_from('>I',rom,0x404)[0]==0x900000
boot=(R/'src/cart_boot.bin').read_bytes()
assert rom[0x100000:0x100000+len(boot)]==boot
assert len(loader)+len(payload)<0x100000 and len(boot)<0x1000
assert rom[len(loader):len(loader)+len(payload)]==payload
assert payload[:4]==b'BS94'
addr,size=struct.unpack('>II',payload[4:12]);assert addr==0x2000
assert len(payload)==size+12
assert addr+size<=0x110000,'Program overlaps renderer scratch space'
layout=[('collision.bin',0x200000),('height.bin',0x240000),('replay.bin',0x2c0000),('route.bin',0x2d8000),('audio.bin',0x300000),('sky.bin',0x400000)]
for i,(name,offset) in enumerate(layout):
    b=(R/'assets'/name).read_bytes();assert rom[offset:offset+len(b)]==b
    end=layout[i+1][1] if i+1<len(layout) else len(rom)
    assert offset+len(b)<=end,(name,'overlaps next asset')
m=json.loads((R/'assets/manifest.json').read_text())
for item in m['models']:
    if item.get('runtime'):
        p=R/'vendor/HexGL'/item['source']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256']
assert sum(i['triangles'] for i in m['models'] if i['runtime'])==12206
assert len((R/'src/audio.bin').read_bytes())<8192
s=(R/'src/hexgl.equ').read_text()
mods=dict(re.findall(r'(MOD(?:end|run)_\w+)\s+EQU \$([0-9a-fA-F]+)',s))
for name in ['engine','control']:
    assert int(mods['MODend_'+name],16)<0xf03f00,'GPU module overlaps stack'
report={'rom_bytes':len(rom),'sha256':hashlib.sha256(rom).hexdigest(),'load_address':hex(addr),'loaded_bytes':size,'loaded_end':hex(addr+size),'scratch_start':'0x110000','triangle_arena_end':'0x14acc8','framebuffer_start':'0x1b4800','runtime_triangles':12206,'runtime_objects':m['objects'],'status':'PASS'}
(R/'rom/verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
