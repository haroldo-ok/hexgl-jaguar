#!/usr/bin/env python3
"""Derive optional demo/autopilot waypoints from the real Cityscape road mask.
Upstream's supplied replay contains only one distinct position; it is preserved
as replay.bin, but is NOT presented as an animated race or used to pass tests.
"""
from pathlib import Path
import numpy as np,struct,math
from PIL import Image
from skimage.morphology import skeletonize
R=Path(__file__).resolve().parents[1]
im=np.array(Image.open(R/'vendor/HexGL/textures/tracks/cityscape/collision.png').resize((512,512),Image.Resampling.NEAREST))
y,x=np.where(skeletonize(im[:,:,0]>200));pts=set(zip(x,y))
adj={p:[(p[0]+i,p[1]+j) for i in [-1,0,1] for j in [-1,0,1] if (i or j) and (p[0]+i,p[1]+j) in pts] for p in pts}
assert all(len(v)==2 for v in adj.values()),'Expected a single closed road loop'
start=min(pts,key=lambda p:(p[0]-(256-2268*512/6000))**2+(p[1]-(256-886*512/6000))**2)
path=[start];prev=start;cur=max(adj[start],key=lambda p:p[1])
while cur!=start:
    path.append(cur);nextp=next(p for p in adj[cur] if p!=prev);prev,cur=cur,nextp
assert len(path)==len(pts)
# Keep every second skeleton sample, plus every boost/checkpoint pixel.
route=[]
for i,p in enumerate(path):
    color=im[p[1],p[0],:3]
    if i%2==0 or (color[0]==255 and (color[1]<127 or color[2]<250)):route.append((i,p))
h=np.frombuffer((R/'assets/height.bin').read_bytes(),dtype='>u2').reshape(512,512)
blob=bytearray()
for i,(ix,p) in enumerate(route):
    back=path[(ix-5)%len(path)];front=path[(ix+5)%len(path)]
    angle=round(math.atan2(-(front[0]-back[0]),front[1]-back[1])*512/(2*math.pi))%512*4
    # Coordinate rounding as in ShipControls.boosterCheck.
    wx=(p[0]+.5-256)*24000/512;wz=(p[1]+.5-256)*24000/512
    blob+=struct.pack('>iiii',round(wx*256),int(h[p[1],p[0]])*256,round(wz*256),angle)
(R/'assets/route.bin').write_bytes(blob)
(R/'assets/route.inc').write_text(f'route_count equ {len(route)}\nroute_data equ $ad8000\n')
print('Autopilot:',len(route),'waypoints derived from the collision image')
