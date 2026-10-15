#!/usr/bin/env python3
"""Preserve the provided replay as native fixed-point records (not a moving demo)."""
from pathlib import Path
import json,math,struct
R=Path(__file__).resolve().parents[1]
p=json.loads((R/'vendor/HexGL/replays/cityscape-casual/bkcore.replay.json').read_text())
b=bytearray()
for t,x,y,z,qx,qy,qz,qw in p:
    yaw=math.atan2(2*(qw*qy+qx*qz),1-2*(qy*qy+qz*qz))
    angle=round(-yaw*512/(2*math.pi))%512*4
    b+=struct.pack('>iiii',round(x*4*256),round(y*4*256),round(z*4*256),angle)
(R/'assets/replay.bin').write_bytes(b)
print(len(p),'replay records;',len({tuple(x[1:4]) for x in p}),'unique positions')
