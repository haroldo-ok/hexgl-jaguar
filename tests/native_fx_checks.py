"""Read-only RGB/sprite/depth arithmetic proofs against actual GPU execution."""
from pathlib import Path
from functools import lru_cache
import struct
R=Path(__file__).resolve().parents[1]

@lru_cache(None)
def tables():
 from hud_checks import palette
 return palette().tolist(),struct.unpack('>32768H',(R/'assets/color-encode.bin').read_bytes()),struct.unpack('>768I',(R/'assets/effects.bin').read_bytes())

def rgb(cry):
 palette,_,_=tables()
 return tuple(c*(cry&255)//256 for c in palette[(cry>>8)&255])

def blend(src,dst,alpha,mode):
 _,encode,_=tables();s=rgb(src);d=rgb(dst)
 if mode:color=[min(255,b+a*alpha//256) for a,b in zip(s,d)]
 else:color=[(a*alpha+b*(256-alpha))//256 for a,b in zip(s,d)]
 return encode[((color[0]>>3)<<10)|((color[1]>>3)<<5)|(color[2]>>3)]

def pixel(a):
 if not a[15] or a[15]&1:return False
 _,_,atlas=tables();z=a[14];size,opacity,kind=a[25:28];col,row=a[30:32]
 assert 0<=kind<=2 and 0<=opacity<=256 and z>=10
 assert size==max(2,min(32,([8,24,16][kind]*(32768//z))>>7)),'Perspective sprite size differs'
 assert 0<=col<size and 0<=row<size
 index=(row*16//size)*16+col*16//size
 if 0x9f2000<=a[22]<0x9fa000:
  assert (a[22]-0x9f2000)%1024==0 and (a[22]-0x9f2000)//16384==kind,'Wrong per-particle source color bank'
  colors=struct.unpack('>8192I',(R/'assets/particle-colors.bin').read_bytes())
  raw=colors[(a[22]-0x9f2000)//4+index]
 else:raw=atlas[kind*256+index]
 expected=raw if kind==2 else (raw&0xffffff00)|((raw&255)*opacity//256)
 assert a[16]==expected,'Original source color2/life/sprite resampling differs'
 alpha=(raw>>16)*opacity//256 if kind==2 else raw>>16
 if kind==1:alpha=alpha*204//256
 assert a[18]==alpha and a[19]==int(kind!=1),'Source alpha/blend mode differs'
 assert a[20]==blend(a[16],a[17],alpha,a[19]),'GPU RGB composite differs (including packed-alpha masking)'
 x,y=a[28]+col,a[29]+row
 assert 0<=x<384 and 50<=y<200,'Sprite clipped pixel outside viewport'
 address=y*1536+(x//4)*16+(x%4)*2
 assert a[21]-address in (0x1b4800,0x1b4808),'Pixel not written into interleaved native framebuffer'
 return True

def signed16(n):return (n&65535)-65536 if n&32768 else n&65535

def depth(d):
 if len(d)<32 or not d[31] or d[31]&1:return False
 px,py,z,triangle=d[16:20]
 v=[(signed16(n>>16)-px,signed16(n)-py) for n in d[20:23]]
 cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
 w=[cross(v[1],v[2]),cross(v[2],v[0]),cross(v[0],v[1])];area=sum(w)
 if area<0:w=[-n for n in w];area=-area
 assert area>0 and min(w)>=0,'Depth proof point outside actual triangle'
 while area>=16384:w=[n//2 for n in w];area//=2
 assert d[26:30]==w+[area],'Native barycentric weights differ'
 assert min(d[23:26])>10,'Native tested a near-plane triangle'
 reciprocal=sum(weight*(32768//depth) for weight,depth in zip(w,d[23:26]))//area
 assert reciprocal>0 and triangle==32768//reciprocal,'Actual submitted-vertex reciprocal depth differs'
 return True

def verify(result):
 from PIL import Image
 valid=[];depths=0;kinds=set();sizes=set()
 for f in result['fields'][150:]:
  a=f['fx_aux']
  if pixel(a):valid.append(f);kinds.add(a[27]);sizes.add(a[25])
  depths+=depth(f['fx_depth'])
 assert len(valid)>100 and kinds=={0,1,2},('All native source sprite kinds not exercised',len(valid),kinds)
 assert len(sizes)>3 and max(f['effects'][4] for f in result['fields'])>256,'Only fixed-size or one-texel sprites rendered'
 assert depths>20,'Actual inside-triangle depth arithmetic not exercised'
 dx,dy=(17,8) if result['video'].lower()=='ntsc' else (18,-4)
 matches=[]
 for path in sorted(Path(result['output_dir']).glob('frame_*.png')):
  n=int(path.stem.split('_')[1]);image=Image.open(path).convert('RGB');found=False
  for f in result['fields'][max(150,n-28):n+1]:
   a=f['fx_aux']
   if not a[15] or a[15]&1:continue
   x,y=a[28]+a[30],a[29]+a[31]
   if a[20]==a[17] or not (0<=x<384 and 50<=y<200):continue
   if image.getpixel((x+dx,y+dy))==rgb(a[20]):found=True;break
  if found:matches.append(path.name)
 assert len(matches)>=2,('Native composed sprite pixels not present in TOM output',matches)
 return {'rgb_composites_and_source_texels_checked':len(valid),'source_sprite_kinds':sorted(kinds),'perspective_pixel_sizes':sorted(sizes),'actual_triangle_depth_checks':depths,'observed_depth_occlusions':max(f['fx_depth'][13] for f in result['fields']),'exact_composed_framebuffer_captures':matches}
