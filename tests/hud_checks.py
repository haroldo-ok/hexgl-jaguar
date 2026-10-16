"""Framebuffer oracle from original PNGs and HUD.js geometry, not native records.
Checks actual TOM pixels; only recent controller-driven states may match a capture.
The completed back buffer normally appears a few fields after GAME is updated.
"""
from pathlib import Path
from functools import lru_cache
import sys,re
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'tools'))
from cry import cry

@lru_cache(None)
def palette():
    text=(R/'vendor/virtualjaguar/src/cry2rgb.h').read_text();channels=[]
    for name in ('redcv','greencv','bluecv'):
        part=text.split(name+'[16][16] = {')[1].split('};')[0]
        channels.append([int(x) for x in re.findall(r'\d+',re.sub(r'//[^\n]*','',part))])
    return np.array(channels).T

@lru_cache(None)
def layers():
    dac=palette()
    # Independent bit-interleaved Bayer rank, equivalent to the coverage matrix.
    ranks=np.zeros((50,384),int)
    for y in range(50):
        for x in range(384):
            ranks[y,x]=sum((2*(((x>>i)&1)^((y>>i)&1))+((y>>i)&1))<<(2*(2-i)) for i in range(3))
    result=[]
    for name in ['hud-bg','hud-fg-speed','hud-fg-shield']:
        im=Image.open(R/'vendor/HexGL/textures/hud'/f'{name}.png').convert('RGBA').resize((384,50),Image.Resampling.LANCZOS)
        c=np.frombuffer(cry(im),dtype='>u2').reshape(50,384).astype(int)
        rgb=(dac[c>>8]*(c&255)[:,:,None])>>8
        coverage=np.asarray(im)[:,:,3]>(ranks+.5)*255/64
        result.append((rgb.astype(np.uint8),coverage))
    return result

@lru_cache(None)
def expected(speed,shield):
    yy,xx=np.mgrid[:50,:384];x=xx+.5;y=yy+.5
    masks=[np.ones((50,384),bool), abs(x-192)<=384/2.91*(speed/28)+50-y,
           (abs(x-192)<=384/18.3)&(y>=384/34+384/14.3*(1-shield/100))&(y<384/34+384/14.3)]
    image=np.zeros((50,384,3),np.uint8);mask=np.zeros((50,384),bool)
    for (rgb,coverage),clip in zip(layers(),masks):
        m=coverage&clip;image[m]=rgb[m];mask|=m
    font=(R/'vendor/new_bjl/font/light8x8.fnt').read_bytes()
    for value,row in [(speed*10,14),(shield,25)]:
        text=f'{value:03d}'
        for i,c in enumerate(text):
            bits=np.unpackbits(np.frombuffer(font[8+ord(c)*8:8+(ord(c)+1)*8],np.uint8)).reshape(8,8)
            image[row:row+8,180+i*8:188+i*8]=bits[:,:,None]*((palette()[0x88]*255)>>8)
            mask[row:row+8,180+i*8:188+i*8]=True
    return image,mask

def check_pixels(image,speed,shield,standard):
    expected_rgb,mask=expected(speed,shield)
    y,x=np.where(mask);dx,dy=(17,8) if standard=='ntsc' else (18,-4)
    assert np.all(y+dy>=0),'Artwork clipped by video standard'
    observed=np.asarray(image.convert('RGB'))[y+dy,x+dx]
    matches=np.all(observed==expected_rgb[y,x],axis=1)
    assert matches.all(),f'HUD pixel mismatch at speed {speed}, shield {shield}: {int((~matches).sum())}/{len(matches)}'
    return len(matches)

def verify(result):
    d=Path(result['output_dir']);s=result['fields'];standard=result['video'].lower();matches=[]
    captures=sorted(d.glob('frame_*.png'))+[d/'final.png']
    for path in captures:
        n=len(s)-1 if path.name=='final.png' else int(path.stem.split('_')[1])
        if n<150:continue
        candidates={(f['game'][8],f['game'][9]) for f in s[max(0,n-12):n+1]}
        im=Image.open(path);failures=[]
        for speed,shield in candidates:
            try:count=check_pixels(im,speed,shield,standard)
            except AssertionError as e:failures.append(str(e));continue
            matches.append({'capture':path.name,'speed':speed,'shield':shield,'pixels':count});break
        else:raise AssertionError(path.name+': no recently committed state matches original-art oracle; '+str(failures))
    assert len(matches)>=3,'Not enough actual captures checked'
    return {'checks':['original three PNG layers in actual TOM output','HUD.js speed trapezoid and shield rectangle','native speed/shield digits','recent live game state'], 'captures':matches}
