#!/usr/bin/env python3
"""Convert the three actual HUD.png layers and HUD.js clipping to native CrY.
Transparency is deterministic 8x8 ordered coverage, not a replacement bitmap.
Records: big-endian (threshold<<24 | PITCH2 byte offset), CrY word in longword.
"""
from pathlib import Path
import hashlib,json,math,struct
import numpy as np
from PIL import Image
from cry import cry
R=Path(__file__).resolve().parents[1]
W,H=384,50

def offset(x,y): return y*W*4+(x//4)*16+(x%4)*2

def threshold(layer,x,y):
    x+=.5;y+=.5
    if layer=='bg':return 0
    if layer=='speed':return max(0,math.ceil((abs(x-W/2)-(H-y))/(W/2.91)*28))
    if abs(x-W/2)>W/18.3 or y>=W/34+W/14.3:return 255
    return max(0,math.ceil((W/34+W/14.3-y)/(W/14.3)*100))

def coverage():
    b=np.array([[0,2],[3,1]])
    for _ in range(2):b=np.block([[4*b,4*b+2],[4*b+3,4*b+1]])
    return (b+.5)*255/64

def main():
    source_js=R/'vendor/HexGL/bkcore/hexgl/HUD.js'
    manifest={'clip_source':str(source_js.relative_to(R)),'clip_source_sha256':hashlib.sha256(source_js.read_bytes()).hexdigest(),'dimensions':[W,H],'placement':[0,0],'alpha':'8x8 ordered coverage','layers':[]}
    inc=['; Generated from the original three HexGL HUD PNGs.']
    b=coverage()
    for layer,filename in [('bg','hud-bg.png'),('speed','hud-fg-speed.png'),('shield','hud-fg-shield.png')]:
        source=R/'vendor/HexGL/textures/hud'/filename
        im=Image.open(source).convert('RGBA').resize((W,H),Image.Resampling.LANCZOS)
        colors=np.frombuffer(cry(im),dtype='>u2').reshape(H,W)
        alpha=np.asarray(im)[:,:,3]
        records=[]
        for y in range(H):
            for x in range(W):
                if alpha[y,x]>b[y%8,x%8]:
                    t=min(255,threshold(layer,x,y))
                    records.append(struct.pack('>II',t<<24|offset(x,y),int(colors[y,x])))
        data=b''.join(records);dest=R/'assets'/f'hud-{layer}.bin';dest.write_bytes(data)
        inc += [f'HUD_{layer.upper()}_COUNT equ {len(records)}', '\talign 8',f'hud_{layer}_data:',f'\tincbin "../assets/hud-{layer}.bin"']
        manifest['layers'].append({'layer':layer,'source':str(source.relative_to(R)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'native_file':str(dest.relative_to(R)),'native_sha256':hashlib.sha256(data).hexdigest(),'records':len(records),'bytes':len(data)})
    (R/'assets/hud.inc').write_text('\n'.join(inc)+'\n')
    (R/'assets/hud.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Original HUD:',sum(l['bytes'] for l in manifest['layers']),'bytes')
if __name__=='__main__':main()
