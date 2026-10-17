#!/usr/bin/env python3
"""Bake all six original sky cubemap faces into a rotating CrY panorama."""
from convert import ROOT,OUT,UP,cry
import numpy as np
from PIL import Image
# Build 2048 by 200, native wrap is split into two blits.
w,h=2048,512
xs=(np.arange(w)-192)*2*np.pi/w
ys=np.arctan((256-np.arange(h))/176)
x=np.cos(ys[:,None])*np.sin(xs[None,:]); y=np.broadcast_to(np.sin(ys[:,None]),x.shape);z=np.cos(ys[:,None])*np.cos(xs[None,:])
v=np.stack([x,y,z],axis=-1);axis=np.abs(v).argmax(axis=-1)
rgb=np.zeros((h,w,3),dtype=np.uint8)
for ax,pos,neg in [(0,'px','nx'),(1,'py','ny'),(2,'pz','nz')]:
    for sign,face in [(1,pos),(-1,neg)]:
        mask=(axis==ax)&(v[:,:,ax]*sign>=0)
        if ax==0: u=-sign*z; vv=-y
        elif ax==1:u=x;vv=sign*z
        else:u=sign*x;vv=-y
        major=np.maximum(np.abs(v[:,:,ax]),1e-6)
        im=np.array(Image.open(UP/'textures/skybox/dawnclouds'/f'{face}.jpg').convert('RGB'))
        ix=np.clip(((u/major+1)/2*(im.shape[1]-1)).astype(int),0,im.shape[1]-1)
        iy=np.clip(((vv/major+1)/2*(im.shape[0]-1)).astype(int),0,im.shape[0]-1)
        rgb[mask]=im[iy[mask],ix[mask]]
b=np.frombuffer(cry(Image.fromarray(rgb)),dtype='>u2').reshape(h,w)
(OUT/'sky.bin').write_bytes(b.astype('>u2').tobytes())
print('Sky:',(OUT/'sky.bin').stat().st_size,'bytes; six source faces used')
