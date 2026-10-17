#!/usr/bin/env python3
"""Native material lookup and static sun visibility, from pinned source assets.
Eight view directions, 64-square CrY textures; not a per-fragment WebGL shader.
Static shadows use actual scene triangles, not painted replacement artwork.
"""
import hashlib,json,math
from pathlib import Path
import numpy as np
from PIL import Image
from convert import ROOT,UP,OUT,models,faces,SCALE
from cry import cry
BANKS=8
ROM_OFFSET=0x102000
sources={}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def image(p):
    sources[str(p.relative_to(ROOT))]=digest(p)
    return np.asarray(Image.open(p).convert('RGBA').resize((64,64),Image.Resampling.LANCZOS),dtype=np.float64)/255

def cube_sample(v,cube):
    axis=np.abs(v).argmax(axis=-1);out=np.zeros(v.shape)
    x,y,z=v[...,0],v[...,1],v[...,2]
    for ax,pos,neg in [(0,'px','nx'),(1,'py','ny'),(2,'pz','nz')]:
        for sign,face in [(1,pos),(-1,neg)]:
            mask=(axis==ax)&(v[...,ax]*sign>=0)
            if ax==0:u=-sign*z;vv=-y
            elif ax==1:u=x;vv=sign*z
            else:u=sign*x;vv=-y
            major=np.maximum(np.abs(v[...,ax]),1e-6)
            ix=np.clip(((u/major+1)*31.5).astype(int),0,63)
            iy=np.clip(((vv/major+1)*31.5).astype(int),0,63)
            out[mask]=cube[face][iy[mask],ix[mask],:3]
    return out

def atlas():
    cube={n:image(UP/'textures/skybox/dawnclouds'/f'{n}.jpg') for n in ('px','nx','py','ny','pz','nz')}
    data=[];entries=[]
    for bank in range(BANKS):
        theta=bank*2*math.pi/BANKS
        # Tangent-space hemisphere approximation. Full per-face TBN is not implied.
        view=np.array([math.sin(theta)*.8,math.cos(theta)*.6,1.0]);view/=np.linalg.norm(view)
        light=np.array([-4000.,1800.,1200.]);light/=np.linalg.norm(light)
        half=light+view;half/=np.linalg.norm(half)
        for name,geo,tex,yoff in models:
            rgba=image(UP/'textures'/tex);rgb=rgba[:,:,:3]
            root=(UP/'textures'/tex).parent
            npth=root/'normal.jpg';spth=root/'specular.jpg'
            mapped=name not in ('booster','speed','banner')
            if mapped:
                normal=image(npth)[:,:,:3]*2-1
                if name=='base':normal[:,:,:2]*=3
                normal/=np.maximum(np.linalg.norm(normal,axis=-1,keepdims=True),1e-6)
                spec=image(spth)[:,:,:3]
                diffuse=np.maximum(0,normal@light)
                specular=np.maximum(0,normal@half)**42
                rgb=rgb*(.85+.15*diffuse[:,:,None])+spec*specular[:,:,None]*(rgb if name in ('ship','track') else 1)
                if name.startswith('scrapers'):
                    reflection=2*(normal@view)[:,:,None]*normal-view
                    environment=cube_sample(reflection[...,[0,2,1]],cube)
                    weight=.8*spec
                    rgb=rgb*(1-weight)+environment*weight
            if name=='speed':rgb=np.broadcast_to(np.array([0,150,255])/255,(64,64,3))
            native=np.frombuffer(cry(Image.fromarray(np.uint8(np.clip(rgb*255,0,255)))),dtype='>u2').copy().reshape(64,64)
            native[native==0]=1 # opaque black must not match transparency key
            if name=='booster':
                yy,xx=np.indices((64,64));threshold=((yy&3)*4+(xx&3)^((yy&1)*3))*16+8
                native[rgba[:,:,3]*255<threshold]=0
            blob=native.astype('>u2').tobytes();data.append(blob)
            entries.append({'bank':bank,'material':name,'offset':len(data[:-1])*8192,'sha256':hashlib.sha256(blob).hexdigest(),'transparent_texels':int((native==0).sum())})
    blob=b''.join(data);(OUT/'materials.bin').write_bytes(blob)
    return {'banks':BANKS,'materials':9,'size':[64,64],'rom_offset':hex(ROM_OFFSET),'bytes':len(blob),'sha256':hashlib.sha256(blob).hexdigest(),'entries':entries,'adaptations':['eight yaw-dependent tangent-space lookup banks; no per-face TBN or shader interpolation','original normal/specular maps, exponent 42, base normal scale 3','original sky cubemap reflections modulated by scraper specular maps','ordered-alpha zero-key booster; opaque source-blue speed pads','static centroid sun visibility baked into native face luminance; no moving ship shadow']}

def shadows():
    triangles=[];receivers=[];labels=[];geo_sources={};counts={}
    for name,path,tex,yoff in models:
        p=UP/'geometries'/path;geo_sources[str(p.relative_to(ROOT))]=digest(p)
        d=json.loads(p.read_text());verts=np.array(d['vertices'],dtype=float).reshape(-1,3);verts[:,1]+=yoff
        if name=='booster':verts+=np.array([0,.665,-3.8])
        verts=np.rint(verts*SCALE);fs=faces(d);groups={}
        for ids,uv in fs:
            tri=verts[ids];c=tri.mean(axis=0)
            key=(int(c[0]//1024),int(c[2]//1024)) if name not in ('ship','booster') else (0,0)
            groups.setdefault(key,[]).append(tri)
        for gi,group in enumerate(groups.values()):
            label=name if name in ('ship','booster') else f'{name}_{gi}'
            counts[label]=len(group)
            if name not in ('ship','booster'):
                triangles.extend(group)
                if name!='speed':
                    receivers.extend(np.mean(group,axis=1));labels.extend((label,i) for i in range(len(group)))
    tri=np.asarray(triangles);origins=np.asarray(receivers)
    direction=np.array([-4000.,1200.,1800.]);direction/=np.linalg.norm(direction)
    a=tri[:,0];e1=tri[:,1]-a;e2=tri[:,2]-a
    h=np.cross(direction,e2);det=np.einsum('ij,ij->i',e1,h)
    valid=np.abs(det)>1e-8;inv=np.divide(1,det,out=np.zeros_like(det),where=valid)
    blocked=[]
    for start in range(0,len(origins),32):
        s=origins[start:start+32,None,:]-a
        u=np.einsum('bti,ti->bt',s,h)*inv
        q=np.cross(s,e1)
        v=np.einsum('bti,i->bt',q,direction)*inv
        t=np.einsum('bti,ti->bt',q,e2)*inv
        blocked.extend(np.any(valid & (u>=-1e-7)&(v>=-1e-7)&(u+v<=1+1e-7)&(t>1),axis=1).tolist())
    lum={label:[160]*count for label,count in counts.items()}
    for (label,i),shadow in zip(labels,blocked):
        if shadow:lum[label][i]=128
    result={'sources':geo_sources,'faces':lum,'direction':direction.tolist(),'receiver_faces':len(origins),'occluded_faces':sum(blocked),'method':'double-sided triangle ray test at each static receiver centroid, self-hit epsilon 1 native unit'}
    (OUT/'shadow-faces.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
    print('Static sun visibility:',sum(blocked),'/',len(origins),'receiver centroids occluded',flush=True)
    return {k:v for k,v in result.items() if k!='faces'}

def main():
    report=atlas();report['shadows']=shadows();report['sources']=sources
    (OUT/'materials.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Material banks:',report['bytes'],'bytes,',len(sources),'source maps',flush=True)
if __name__=='__main__':main()
