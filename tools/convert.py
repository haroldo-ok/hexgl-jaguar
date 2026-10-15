#!/usr/bin/env python3
"""Convert real HexGL JSON geometry to 42Bastian's triangle/normal/UV format.
No replacement meshes: quads are triangulated, all triangles retained.
Cityscape is partitioned into bounded objects for the engine's culling.
"""
import json, math, re, hashlib, pathlib, struct
import numpy as np
from PIL import Image
ROOT=pathlib.Path(__file__).resolve().parents[1]
UP=ROOT/'vendor/HexGL'
OUT=ROOT/'assets'; OUT.mkdir(exist_ok=True)
SCALE=4

def faces(d):
    f=d['faces']; i=0; out=[]
    layers=[x for x in d.get('uvs',[]) if x]
    while i<len(f):
        t=f[i]; i+=1; n=4 if t&1 else 3
        vs=f[i:i+n]; i+=n
        if t&2:i+=1
        uv=[(0,0)]*n
        if t&4:i+=len(layers)
        if t&8:
            for j,l in enumerate(layers):
                inds=f[i:i+n];i+=n
                if j==0:uv=[(l[2*k],l[2*k+1]) for k in inds]
        if t&16:i+=1
        if t&32:i+=n
        if t&64:i+=1
        if t&128:i+=n
        for ix in ([(0,1,2)] if n==3 else [(0,1,3),(1,2,3)]):
            out.append(([vs[k] for k in ix],[uv[k] for k in ix]))
    assert i==len(f)
    return out

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

models=[
('ship','ships/feisar/feisar.js','ships/feisar/diffuse.jpg',0),
('booster','booster/booster.js','ships/feisar/booster/booster.png',0),
('track','tracks/cityscape/track.js','tracks/cityscape/diffuse.jpg',-5),
('base','bonus/base/base.js','bonus/base/diffuse.jpg',-5),
('speed','tracks/cityscape/bonus/speed.js','bonus/base/diffuse.jpg',-5),
('scrapers1','tracks/cityscape/scrapers1.js','tracks/cityscape/scrapers1/diffuse.jpg',0),
('scrapers2','tracks/cityscape/scrapers2.js','tracks/cityscape/scrapers2/diffuse.jpg',0),
('start','tracks/cityscape/start.js','tracks/cityscape/start/diffuse.jpg',-5),
('banner','tracks/cityscape/startbanner.js','tracks/cityscape/start/start.jpg',-5),
]
lines=[]; names=[]; manifest=[]; maxv=0;maxf=0
for ti,(name,path,tex,yoff) in enumerate(models):
    p=UP/'geometries'/path; d=json.loads(p.read_text())
    verts=np.array(d['vertices']).reshape(-1,3); verts[:,1]+=yoff
    if name=='booster':verts+=np.array([0,.665,-3.8])
    verts=np.rint(verts*SCALE).astype(int); fs=faces(d)
    groups={}
    for f,uv in fs:
        center=verts[f].mean(axis=0)
        key=(int(center[0]//1024),int(center[2]//1024)) if name not in ('ship','booster') else (0,0)
        groups.setdefault(key,[]).append((f,uv))
    img=Image.open(UP/'textures'/tex).resize((64,64),Image.Resampling.LANCZOS)
    (OUT/(name+'.cry')).write_bytes(cry(img))
    for gi,(key,group) in enumerate(groups.items()):
        label=name if name in ('ship','booster') else f'{name}_{gi}'
        names.append(label)
        used=sorted({v for f,uv in group for v in f}); remap={v:i for i,v in enumerate(used)}
        center=np.zeros(3,dtype=int) if name in ('ship','booster') else np.rint(verts[used].mean(axis=0)).astype(int)
        loc=verts[used]-center
        maxv=max(maxv,len(loc)); maxf=max(maxf,len(group))
        lines+=['\talign 8',f'obj_{label}:','\tdc.w 0', '\tdc.w '+','.join(map(str,center)), '\tdc.w 0,0,0,0',f'\tdc.l {label}_points,{label}_faces,{label}_normals,0', '\tdc.l scratch_rotated,scratch_normals_rotated,0,scratch_projected,scratch_visible',f'{label}_points:',f'\tdc.l {len(loc)}']
        lines+=['\t_PT '+','.join(map(str,v)) for v in loc]
        lines+=[f'{label}_faces:',f'\tdc.l {len(group)}']
        for fi,(f,uv) in enumerate(group):
            lines+=['\tdc.w '+','.join(str(remap[x]) for x in f)+',128',f'\tdc.l {label}_uv+{fi*16}']
        lines+=[f'{label}_normals:',f'\tdc.l {len(group)}']
        for f,uv in group:
            a,b,c=verts[f]; n=-np.cross(b-a,c-a).astype(float); size=np.linalg.norm(n)
            if size:n=np.rint(n*256/size).astype(int)
            else:n=np.array([0,-256,0])
            lines+=['\tNT '+','.join(map(str,n.astype(int)))]
        lines+=[f'{label}_uv:']
        for f,uv in group:
            vals=[]
            for u,v in uv: vals.extend([round(max(0,min(1,u))*63*256),round((1-max(0,min(1,v)))*63*256)])
            lines+=['\tdc.w '+','.join(map(str,[ti,0]+vals))]
    manifest.append(dict(name=name,source=str(p.relative_to(UP)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),vertices=len(verts),triangles=len(fs),objects=len(groups),runtime=True))
parts=[]
for i in range(0,len(lines),10000):
    name=f'models_{i//10000:02d}.inc';(OUT/name).write_text('\n'.join(lines[i:i+10000])+'\n');parts.append(name)
(OUT/'models.inc').write_text('\n'.join('\tinclude \"../assets/'+n+'\"' for n in parts)+'\n')
(OUT/'model_list.inc').write_text('\n'.join('\tdc.l obj_'+n for n in names)+'\n\tdc.l 0\n')
(OUT/'limits.inc').write_text(f'MAX_VERTICES equ {maxv}\nMAX_FACES equ {maxf}\nNUM_OBJECTS equ {len(names)}\n')
(OUT/'textures.inc').write_text('\n'.join(f'\tincbin "../assets/{name}.cry"' for name,*_ in models)+'\n')
# Original packed height is base 255, as in ImageData.getPixelF.
h=np.array(Image.open(UP/'textures/tracks/cityscape/height.png').convert('RGB').resize((512,512),Image.Resampling.NEAREST),dtype=np.int32)
height=np.rint((h[:,:,0]+255*h[:,:,1]+65025*h[:,:,2])/10*SCALE+4*SCALE).clip(0,65535).astype('>u2')
(OUT/'height.bin').write_bytes(height.tobytes())
c=np.array(Image.open(UP/'textures/tracks/cityscape/collision.png').convert('RGB').resize((512,512),Image.Resampling.NEAREST))
# 0 off track, 1 road, 2 boost, 3/4/5 sequential checkpoints
m=np.where(c[:,:,0]>=240,1,0).astype(np.uint8)
m[(c[:,:,0]==255)&(c[:,:,1]<127)&(c[:,:,2]<127)]=2
for cp in range(3):m[(c[:,:,0]==255)&(c[:,:,1]==255)&(c[:,:,2]==cp)]=3+cp
(OUT/'collision.bin').write_bytes(m.tobytes())
# Keep an exact native conversion of the unused Edge mesh too, separate from the Cityscape runtime.
d=json.loads((UP/'geometries/tracks/edge/track.js').read_text());ef=faces(d)
with (OUT/'edge.mesh').open('wb') as f:
    f.write(struct.pack('>II',len(d['vertices'])//3,len(ef)))
    for v in np.array(d['vertices']).reshape(-1,3):f.write(struct.pack('>hhh',*[round(x*4) for x in v]))
    for vs,uv in ef:f.write(struct.pack('>HHH',*vs))
manifest.append(dict(name='edge',vertices=len(d['vertices'])//3,triangles=len(ef),runtime=False,reason='Not loaded by upstream Cityscape'))
(OUT/'manifest.json').write_text(json.dumps(dict(models=manifest,max_vertices=maxv,max_faces=maxf,objects=len(names),scale=SCALE),indent=2))
print('Converted',len(names),'objects; scratch maxima',maxv,maxf,'triangles',sum(x['triangles'] for x in manifest))
