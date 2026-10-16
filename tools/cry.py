"""Shared Jaguar CrY conversion using the emulator chroma DAC tables."""
import pathlib,re
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
# CrY conversion uses the actual VJ chroma DAC table, not an RGB565 assumption.
txt=(ROOT/'vendor/virtualjaguar/src/cry2rgb.h').read_text()
ch=[]
for name in ('redcv','greencv','bluecv'):
    part=txt.split(name+'[16][16] = {')[1].split('};')[0]
    part=re.sub(r'//[^\n]*','',part)
    ch.append(np.array([int(x) for x in re.findall(r'\d+',part)],dtype=np.float32))
ch=np.stack(ch,axis=1)/255

def cry(a):
    rgb=np.asarray(a.convert('RGB'),dtype=np.float32).reshape(-1,3)
    ans=[]
    for block in np.array_split(rgb,max(1,len(rgb)//1024)):
        y=np.clip(block@ch.T/(ch*ch).sum(axis=1),0,255)
        err=((block[:,None,:]-y[:,:,None]*ch[None,:,:])**2).sum(axis=2)
        k=err.argmin(axis=1); val=np.rint(y[np.arange(len(k)),k]).astype(np.uint16)
        ans.append((k.astype(np.uint16)<<8)|val)
    return np.concatenate(ans).astype('>u2').tobytes()

