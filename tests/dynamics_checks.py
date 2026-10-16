"""Independent numerical oracles for ShipControls adaptations and real GPU vertices."""
import re,math,struct
from pathlib import Path
R=Path(__file__).resolve().parents[1]
SIN=[]
for line in (R/'src/sintab.inc').read_text().splitlines():
 if 'dc.w' in line:SIN.extend(map(int,line.split('dc.w')[1].strip().split(',')))
def trig(angle):
 i=(angle&2044)//2
 return SIN[i],SIN[i+1]
def signed16(n):return (n+32768)%65536-32768

def transformed_vertex(f):
 p=f['pose'];x,y,z=(2,2,16)
 b,a=trig(p[0]);d,c=trig(p[1]);ff,e=trig(p[2])
 ac=a*c>>15;bc=b*c>>15
 matrix=[d*ff>>15,-d*e>>15,c,(ac*ff+b*e)>>15,(-ac*e+b*ff)>>15,-a*d>>15,(-bc*ff+a*e)>>15,(bc*e+a*ff)>>15,b*d>>15]
 v=[(sum(matrix[j*3+k]*[x,y,z][k] for k in range(3))+16383)>>15 for j in range(3)]
 v=[signed16(v[j]+f['mesh_positions'][j]-p[6+j]) for j in range(3)]
 co,si=trig(p[9]);x=(co*v[0]+si*v[2]+16383)>>15;z=(-si*v[0]+co*v[2]+16383)>>15;y=v[1]
 co,si=trig(f['physics'][12]>>8)
 return x,(co*y+si*z)>>15,(co*z-si*y)>>15

def verify_vertices(result):
 checked=pitched=0;seen=None
 for f in result['fields'][150:]:
  q=f['physics'];m=f['motion']
  if len(q)<30 or q[25]!=m[16] or q[25]==seen:continue
  seen=q[25]
  actual=(signed16(q[26]>>16),signed16(q[26]),signed16(q[27]>>16))
  wanted=transformed_vertex(f)
  assert actual==wanted,('GPU vertex pitch/yaw/roll mismatch',f['f'],actual,wanted,f['pose'],q[:14])
  assert q[28]==actual[2],'Projected vertex used a different depth'
  # Exact reciprocal and per-standard aspect, independent of native telemetry.
  x,y,z=actual;reciprocal=32768//max(2,z)
  xx=(abs(x)*reciprocal)>>7;yy=(abs(y)*reciprocal)>>7
  xx=xx if x>=0 else -xx;yy=-yy if y>=0 else yy
  yy=yy*(11 if f['game'][20]==60 else 12)>>4
  want=(192+xx,100+yy)
  got=(signed16(q[29]>>16),signed16(q[29]))
  assert got==want,('Actual projected vertex mismatch',f['f'],got,want)
  checked+=1;pitched+=abs(q[12])>1024
 assert checked>30 and pitched>10,'Pitch transform not exercised'
 return {'actual_vertices':checked,'pitched_vertices':pitched}

def height_q8(x,z):
 h=HEIGHT
 u=((x>>8)+12000)*131072//24000;v=((z>>8)+12000)*131072//24000
 ix=min(510,u>>8);iz=min(510,v>>8);fx=u&255;fz=v&255
 a,b,c,d=[h[i] for i in [iz*512+ix,iz*512+ix+1,(iz+1)*512+ix,(iz+1)*512+ix+1]]
 b=a if b==65535 else b;c=a if c==65535 else c;d=a if d==65535 else d
 top=a*256+(b-a)*fx;bottom=c*256+(d-c)*fx
 return top+(bottom-top)*fz//256
HEIGHT=struct.unpack('>262144H',(R/'assets/height.bin').read_bytes())

def verify_dynamics(result):
 vertices=verify_vertices(result);s=result['fields'];last=None;hover=drift=repulse=fall=0
 for f in s[150:]:
  g,q=f['game'],f['physics'];m=f['motion']
  if q[11]!=m[16] or m[16]==last:continue
  last=m[16]
  assert abs(q[1])<=26,'Lateral drift escaped ratio bounds'
  assert abs(q[6])<=40000 and 0<=q[12]<=40000,'Pitch escaped slope envelope'
  if g[2]!=1 or g[13] or q[10]==0:continue
  if q[4]:
   fall+=1
  elif not q[9]:
   expected=height_q8(g[4],g[6])
   assert q[8]==expected,('Bilinear source height mismatch',f['f'],q[8],expected)
   dy=q[8]-q[20]
   assert q[21]==dy
   alpha=round(256*(1-.6**(q[10]*60/g[20])))
   assert q[16]==alpha
   target=q[20]+(dy if dy>=0 else dy*alpha//256)
   assert g[5]==target,('Hover response mismatch',f['f'],g[5],target)
   hover+=1
  drift+=abs(q[1])>2;repulse+=bool(q[2] or q[3])
 assert hover>10,'No actual height-follow updates'
 return {**vertices,'hover_updates':hover,'drifting_updates':drift,'repulsion_updates':repulse,'fall_updates':fall}

def verify_particles(result):
 previous=None;updates=spawns=0;drawn=0
 for f in result['fields'][150:]:
  fx=f['effects'];g=f['game'];pool=f.get('particles')
  if pool is None:continue
  if previous and fx[12]==previous['effects'][12]:continue
  particles=[pool[i:i+8] for i in range(0,128,8)]
  assert all(0<=p[6]<=15360 and p[7] in (0,1) for p in particles),'Pool corruption'
  if g[2]==1:
   assert 0<=fx[2]<=16 and 0<=fx[3]<=17 and fx[4]<=17*256
   drawn+=fx[4]>0
   if previous and fx[12]==previous['effects'][12]+1 and previous['game'][2]==1 and previous['game'][13]==g[13]:
    old=[previous['particles'][i:i+8] for i in range(0,128,8)]
    frozen=g[13] or (g[2]==5 and f['replay'][8])
    if frozen:
     assert pool==previous['particles'],'Pause advanced particle pool'
    else:
     dt=fx[14]
     assert 256<=dt<=1844
     for a,b in zip(old,particles):
      if b[6]>a[6] or a[3:6]!=b[3:6]:spawns+=1;continue
      if not a[6]:continue
      assert b[6]==max(0,a[6]-dt),('Particle lifetime differs',f['f'])
      assert b[:3]==[a[i]+(a[i+3]*dt>>8) for i in range(3)],('Particle integration differs',f['f'])
      updates+=1
  previous=f
 assert updates>20 and spawns>3 and drawn>20,'Real particle simulation not exercised'
 return {'particle_integrations':updates,'observed_spawns':spawns,'drawn_frames':drawn,'maximum_pool':max(f['effects'][2] for f in result['fields'][150:])}

def source_sprite_pixels(result):
 """Actual output must contain original sprite chroma/intensity pixels, not just counters."""
 import numpy as np
 from PIL import Image
 from hud_checks import palette
 from frontend_checks import cry
 paths=['particles/spark.png','particles/cloud.png','ships/feisar/booster/boostersprite.jpg']
 colors=[]
 for i,p in enumerate(paths):
  image=Image.open(R/'vendor/HexGL/textures'/p).convert('RGBA').resize((16,16),Image.Resampling.LANCZOS)
  arr=np.array(image);mask=arr[:,:,3]>150 if i<2 else arr[:,:,:3].max(axis=2)>150
  rgb=Image.new('RGB',(16,16),(255,192,64)) if i==0 else image.convert('RGB')
  codes=np.frombuffer(cry(rgb),dtype='>u2').reshape(16,16)[mask]
  colors.append({tuple((palette()[int(c)>>8]*(int(c)&255))>>8) for c in codes})
 counts=[0,0,0]
 for p in Path(result['output_dir']).glob('frame_*.png'):
  image=np.array(Image.open(p).convert('RGB'))
  # Exclude the source-art HUD and footer, where unrelated text can match white.
  view=image[65:190,:,:].reshape(-1,3)
  unique,n=np.unique(view,axis=0,return_counts=True)
  for i,c in enumerate(colors):counts[i]=max(counts[i],sum(int(k) for v,k in zip(unique,n) if tuple(v) in c))
 assert counts[0]>8,('Source spark pixels missing',counts)
 # Stronger glow proof: reproduce position, alpha stencil and every source color
 # from a recently completed native pose, not just global color frequencies.
 im=Image.open(R/'vendor/HexGL/textures'/paths[2]).convert('RGBA').resize((16,16),Image.Resampling.LANCZOS)
 aa=np.array(im)[:,:,:3].max(axis=2)
 codes=np.frombuffer(cry(im),dtype='>u2').reshape(16,16)
 rgb=(palette()[codes>>8]*(codes&255)[:,:,None])>>8
 yy,xx=np.indices((16,16));threshold=(((yy&3)<<2)^(xx&3))*16
 verified=0
 for path in Path(result['output_dir']).glob('frame_*.png'):
  n=int(path.stem.split('_')[1]);image=np.array(Image.open(path).convert('RGB'))
  for f in result['fields'][max(150,n-20):n+1]:
   g,q,p=f['game'],f['physics'],f['pose']
   if g[2]!=1:continue
   co,si=trig(g[7])
   world=[(g[4]+(si*18>>7))>>8,g[5]>>8,(g[6]-(co*18>>7))>>8]
   x,y,z=[world[j]-p[6+j] for j in range(3)]
   co,si=trig(p[9]);x,z=(co*x+si*z)>>15,(-si*x+co*z)>>15
   co,si=trig(q[12]>>8);y,z=(co*y+si*z)>>15,(co*z-si*y)>>15
   if z<10:continue
   rec=32768//z;sx=(abs(x)*rec)>>7;sy=(abs(y)*rec)>>7
   if x<0:sx=-sx
   if y>=0:sy=-sy
   sx+=184;sy=(sy*(11 if g[20]==60 else 12)>>4)+92
   dx,dy=(17,8) if g[20]==60 else (18,-4)
   opacity=255 if g[12] else 96+g[8]*4
   alpha=aa.astype(int)*opacity>>8;mask=(alpha>0)&(alpha>=threshold)
   if not (0<=sx<=368 and 50<=sy<184):continue
   crop=image[sy+dy:sy+dy+16,sx+dx:sx+dx+16]
   if crop.shape==rgb.shape and np.all(crop[mask]==rgb[mask]):verified=max(verified,int(mask.sum()))
 assert verified>8,('Original glow stencil/position not visible',verified)
 return {'source_sprite_matching_pixels':counts,'exact_glow_pixels':verified}

def verify_fall(result):
 previous=None;checked=held=0;terminal=None
 for f in result['fields'][150:]:
  g,q,m=f['game'],f['physics'],f['motion']
  if q[11]!=m[16]:continue
  if previous and previous['motion'][16]==m[16]:continue
  if previous and previous['physics'][4] and q[4] and m[16]==previous['motion'][16]+1:
   old=previous['physics'];og=previous['game']
   if g[13] and og[13]:
    assert q[5]==old[5] and g[5]==og[5],'Pause advanced falling'
    held+=1
   elif q[5]>old[5]:
    elapsed=g[18]-og[18]
    assert q[5]-old[5]==elapsed,'Fall clock ignored actual video fields'
    delta=80*256*max(1,min(6,elapsed))*60//g[20]
    assert og[5]-g[5]==delta,('Native fall displacement differs',f['f'])
    checked+=1
  if g[2]==2 and q[4]:
   assert 3*g[20]//2<=q[5]<3*g[20]//2+7,'Fall did not end at 1.5 active seconds'
   assert g[9]==0
   terminal=q[5]
  previous=f
 assert checked>10 and terminal is not None
 return {'fall_integration_updates':checked,'paused_fall_updates':held,'terminal_fall_fields':terminal}
