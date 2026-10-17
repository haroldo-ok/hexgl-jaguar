#!/usr/bin/env python3
import pathlib, struct,hashlib
R=pathlib.Path(__file__).resolve().parents[1]
program=(R/'src/hexgl.o').read_bytes()
assert program[:4]==b'BS94'
addr,size=struct.unpack('>II',program[4:12]); assert addr+size<0x110000
rom=bytearray(b'\xff'*(6*1024*1024))
loader=(R/'vendor/jag_3d_engine/loader/sbl.XXX').read_bytes()
rom[:len(loader)]=loader
rom[len(loader):len(loader)+len(program)]=program
for name,offset in [('materials.bin',0x102000),('front-main.cry',0x192000),('front-bg.cry',0x1b7800),('collision.bin',0x200000),('height.bin',0x240000),('replay.bin',0x2c0000),('route.bin',0x2d8000),('audio.bin',0x300000),('sky.bin',0x400000),('blue-materials.bin',0x1e0000),('particle-colors.bin',0x1f2000),('ship-shadow.bin',0x1fa000)]:
 b=(R/'assets'/name).read_bytes();rom[offset:offset+len(b)]=b
boot=(R/'src/cart_boot.bin').read_bytes()
assert len(loader)+len(program)<0x100000 and len(boot)<0x1000
rom[0x100000:0x100000+len(boot)]=boot
struct.pack_into('>I',rom,0x404,0x900000)
p=R/'rom/hexgl.j64';p.parent.mkdir(exist_ok=True);p.write_bytes(rom)
print(p, len(rom),'bytes',hashlib.sha256(rom).hexdigest())
