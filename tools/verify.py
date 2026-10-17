#!/usr/bin/env python3
"""ROM structure, conversion coverage, memory/size and input integrity checks."""
from pathlib import Path
import struct,hashlib,json,re
R=Path(__file__).resolve().parents[1]
rom=(R/'rom/hexgl.j64').read_bytes();payload=(R/'src/hexgl.o').read_bytes()
loader=(R/'vendor/jag_3d_engine/loader/sbl.XXX').read_bytes()
# Object-list adaptation must change ONLY the text bitmap's vertical position.
for name in ['obl0_50.bin','obl1_50.bin','obl0_60.bin','obl1_60.bin']:
    original=(R/'vendor/jag_3d_engine'/name).read_bytes()
    adjusted=(R/'src'/name).read_bytes()
    assert original[:0x50]==adjusted[:0x50] and original[0x58:]==adjusted[0x58:]
    a=int.from_bytes(original[0x50:0x58],'big');b=int.from_bytes(adjusted[0x50:0x58],'big')
    mask=0x7ff<<3
    assert a&~mask==b&~mask and ((a>>3)&0x7ff)-((b>>3)&0x7ff)==4
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
assert addr+size<0xb8000,'Program overlaps extended actual-camera replay records'
assert 0xb8000+6144*24==0xdc000<0xe0000
assert 0xe0000+8192*12==0xf8000
# addobj preserves one candidate before its capacity rejection; reserve its guard.
assert 0xf8000+12<0xf9000
assert 0xf9000+4800<0xfa400 and 0xfa400+4800<0xfb800
assert 0xfb800+4800<0x110000
assert 0x1fc0+64==0x2000
layout=[('materials.bin',0x102000),('front-main.cry',0x192000),('front-bg.cry',0x1b7800),('blue-materials.bin',0x1e0000),('particle-colors.bin',0x1f2000),('ship-shadow.bin',0x1fa000),('collision.bin',0x200000),('height.bin',0x240000),('replay.bin',0x2c0000),('route.bin',0x2d8000),('audio.bin',0x300000),('sky.bin',0x400000)]
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
# Camera smoothing splits signed Q8 deltas before 16-bit IMULT. Establish its
# high-part range for every driveable height-map pixel, not just tested paths.
road=(R/'assets/collision.bin').read_bytes()
heights=[h[0] for i,h in enumerate(struct.iter_unpack('>H',(R/'assets/height.bin').read_bytes())) if road[i]]
assert max(heights)-min(heights)+80<32768,'Camera height delta exceeds signed multiply range'
s=(R/'src/hexgl.equ').read_text()
mods=dict(re.findall(r'(MOD(?:end|run)_\w+)\s+EQU \$([0-9a-fA-F]+)',s))
for name in ['engine','control','bitmap_hud','frontend','frontdraw','recording','pose','effects','handling','view','presentation','skybank','postfx','bloom']:
    assert int(mods['MODend_'+name],16)<0xf03f00,'GPU module overlaps stack'
remaining=json.loads((R/'assets/remaining.json').read_text())
assert remaining['shadow_faces']==1676
assert hashlib.sha256((R/remaining['ship_source']).read_bytes()).hexdigest()==remaining['ship_source_sha256']
for name,item in remaining['outputs'].items():
    data=(R/'assets'/name).read_bytes()
    assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']
# Original HUD assets are present in the loaded program, not merely archived.
hud=json.loads((R/'assets/hud.json').read_text())
assert hashlib.sha256((R/hud['clip_source']).read_bytes()).hexdigest()==hud['clip_source_sha256']
for layer in hud['layers']:
    assert hashlib.sha256((R/layer['source']).read_bytes()).hexdigest()==layer['source_sha256']
    data=(R/layer['native_file']).read_bytes()
    assert hashlib.sha256(data).hexdigest()==layer['native_sha256']
    assert payload[12:].count(data)==1,'HUD data absent or duplicated in native payload'
    for record,color in struct.iter_unpack('>II',data):
        off=record&0xffffff
        assert off<384*50*4 and off%16<8 and off%2==0 and color<=65535
front=json.loads((R/'assets/frontend.json').read_text())
for path,digest in front['sources'].items():
    assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest
for path,digest in front['outputs'].items():
    assert hashlib.sha256((R/'assets'/path).read_bytes()).hexdigest()==digest
assert 0x14acc8<0x150000 and 0x150000+6144*64==0x1b0000<0x1b4800
# New runtime effects are original-source conversions referenced by the program.
fx=json.loads((R/'assets/effects.json').read_text())
for sprite in fx['sprites']:
    assert hashlib.sha256((R/sprite['source']).read_bytes()).hexdigest()==sprite['sha256']
data=(R/'assets/effects.bin').read_bytes()
assert hashlib.sha256(data).hexdigest()==fx['sha256'] and len(data)==3*16*16*4
assert payload[12:].count(data)==1,'Native effect atlas missing/duplicated'
assert 0x1b0000+6144*2==0x1b3000<0x1b4800
assert 0x1800+16*32==0x1a00<0x2000
# Material lookup is actually in the ROM used by renderer native texture pointers.
mat=json.loads((R/'assets/materials.json').read_text())
data=(R/'assets/materials.bin').read_bytes()
assert len(data)==8*9*8192 and hashlib.sha256(data).hexdigest()==mat['sha256']
for p,digest in mat['sources'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==digest
for p,digest in mat['shadows']['sources'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==digest
assert len((R/'assets/sky.bin').read_bytes())==2048*512*2
assert 0x1a40+12*4<0x2000 and 0x1a00+6*4<=0x1a40
report={'material_banks':8,'material_rom_offset':'0x102000','sky_dimensions':[2048,512],'effect_pool':16,'replay_angles_end':'0x1b3000','recording_capacity':6144,'recording_end':'0x1b0000','hud_records':{l['layer']:l['records'] for l in hud['layers']},'rom_bytes':len(rom),'sha256':hashlib.sha256(rom).hexdigest(),'load_address':hex(addr),'loaded_bytes':size,'loaded_end':hex(addr+size),'scratch_start':'0x110000','triangle_arena_end':'0x14acc8','framebuffer_start':'0x1b4800','runtime_triangles':12206,'runtime_objects':m['objects'],'status':'PASS'}
(R/'rom/verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
