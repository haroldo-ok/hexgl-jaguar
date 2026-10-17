#!/usr/bin/env python3
"""Convert original effect textures to bounded native CrY/alpha sprite atlases."""
from pathlib import Path
from PIL import Image
import numpy as np,struct,json,hashlib
from cry import cry
R=Path(__file__).resolve().parents[1];data=bytearray();items=[]
for name,path in [('spark','particles/spark.png'),('cloud','particles/cloud.png'),('glow','ships/feisar/booster/boostersprite.jpg')]:
 p=R/'vendor/HexGL/textures'/path;im=Image.open(p).convert('RGBA').resize((16,16),Image.Resampling.LANCZOS)
 a=np.array(im);rgb=Image.fromarray(a[:,:,:3]);alpha=a[:,:,3]
 if name=='glow':alpha=a[:,:,:3].max(axis=2)
 if name=='spark':rgb=Image.new('RGB',(16,16),(255,192,64))
 values=struct.unpack('>256H',cry(rgb))
 for v,al in zip(values,alpha.flat):data.extend(struct.pack('>I',(int(al)<<16)|v))
 items.append({'name':name,'source':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'offset':len(data)-1024})
(R/'assets/effects.bin').write_bytes(data)
(R/'assets/effects.json').write_text(json.dumps({'sprites':items,'size':[16,16],'format':'alpha8 in bits16..23, CrY16 in low bits; native perspective-resampled RGB additive/alpha-over composition','sha256':hashlib.sha256(data).hexdigest()},indent=2)+'\n')
