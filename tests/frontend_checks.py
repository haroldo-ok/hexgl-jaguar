"""Independent source-font, cartridge-journal and native replay oracles."""
from pathlib import Path
from functools import lru_cache
import json,struct,sys,zlib
import numpy as np
from PIL import Image,ImageFont,ImageDraw
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'tools'))
from cry import cry
from hud_checks import palette

@lru_cache(None)
def glyph(c):
    font=ImageFont.truetype(str(R/'vendor/HexGL/css/BebasNeue-webfont.ttf'),18)
    im=Image.new('L',(16,24));ImageDraw.Draw(im).text((0,0),c,font=font,fill=255)
    return np.array(im)>=128,max(1,min(16,round(font.getlength(c))))

def text_pixels(path,text,x,y,standard='ntsc',color='#4190bb'):
    image=np.array(Image.open(path).convert('RGB'));dx,dy=(17,8) if standard=='ntsc' else (18,-4)
    code=int.from_bytes(cry(Image.new('RGB',(1,1),color)),'big');rgb=(palette()[code>>8]*(code&255))>>8
    count=0
    for c in text:
        mask,advance=glyph(c);yy,xx=np.where(mask)
        assert np.all(image[yy+y+dy,xx+x+dx]==rgb),f'Original font pixels missing: {path}: {text}'
        count+=len(xx);x+=advance
    assert count>20
    return count

def decode_slot(data,index):
    words=struct.unpack_from('>8H',data,index*2)
    magic,gen,hi,lo,lhi,llo,version,check=words
    total=(hi<<16)|lo;lap=(lhi<<16)|llo;c=0xa5c3
    for w in words[1:7]:c^=w
    if magic!=0x4847 or version!=1 or c!=check or not 0<lap<=total<6000000:return None
    return {'generation':gen,'total_ms':total,'lap_ms':lap,'slot':index}

def choose(data,base):
    a,b=decode_slot(data,base),decode_slot(data,base+8)
    if a is None:return b
    if b is None:return a
    return a if ((a['generation']-b['generation'])&65535)<32768 else b

def encode(gen,total,lap):
    w=[0x4847,gen,total>>16,total&65535,lap>>16,lap&65535,1,0xa5c3]
    for v in w[1:7]:w[-1]^=v
    return struct.pack('>8H',*w)

def filename():return f'{zlib.crc32((R/"rom/hexgl.j64").read_bytes()):08X}.eeprom'

def recordings(result):
    data=(Path(result['output_dir'])/'recording.bin').read_bytes()
    assert len(data)%64==0 and len(data)<=6144*64
    return list(struct.iter_unpack('>16i',data))

def replay(result):
    samples=recordings(result);assert len(samples)>50
    extra=list(struct.iter_unpack('>6i',(Path(result['output_dir'])/'recording-view.bin').read_bytes()))
    assert len(extra)==len(samples)
    angles=list(struct.iter_unpack('>bb',(Path(result['output_dir'])/'recording-angles.bin').read_bytes()))
    assert len(angles)==len(samples)
    assert all(b[7]>a[7] for a,b in zip(samples,samples[1:])),'Duplicate/reversed recording clock'
    # Compare stored records against observed native gameplay, not imported routes.
    observed=set();observed_angles=set();observed_views=set()
    for f in result['fields']:
        g,m=f['game'],f['motion']
        if g[2] not in (1,2,3):continue
        sample=tuple(g[4:8]+m[:3]+[g[16]]+g[8:11]+[g[12],g[17],g[2],g[21],g[25]])
        observed.add(sample)
        observed_views.add((sample,tuple(f['view'][8:11]+[f['view'][4],f['view'][5],f['handling'][16]])))
        observed_angles.add((sample,(f['physics'][6]>>10,f['physics'][12]>>10)))
    assert all(s in observed for s in samples),'Stored sample was not an observed native game state'
    assert all((s,a) in observed_angles for s,a in zip(samples,angles)),'Recorded pitch was not an observed native angle'
    assert all((s,v) in observed_views for s,v in zip(samples,extra)),'Actual-camera/bank sample not observed in native gameplay'
    checked=partial=0;last=None
    for f in result['fields']:
        g,m,p,r=f['game'],f['motion'],f['pose'],f['replay']
        if g[2]!=5 or m[16]!=r[15] or m[16]==last or f['view'][12]!=m[16]:continue
        last=m[16];i=r[3];a=samples[i];b=samples[min(i+1,len(samples)-1)]
        alpha=0 if a[7]==b[7] else (r[4]-a[7])*256//(b[7]-a[7])
        assert r[11]==alpha and 0<=alpha<256
        want=[]
        for j in range(7):
            delta=b[j]-a[j]
            if j==3:delta=(delta+1024)%2048-1024
            v=a[j]+delta*alpha//256
            if j==3:v&=2044
            want.append(v)
        assert g[4:8]+m[:3]==want,('Replay interpolation differs',f['f'],i,alpha)
        assert g[8:11]+[g[12],g[17],r[16],g[21],g[25]]==list(a[8:16])
        assert g[16]==r[4]
        assert f['mesh_positions'][:3]==[v>>8 for v in want[:3]]
        assert f['mesh_positions'][3:]==f['mesh_positions'][:3]
        ap=[angles[i][j]*1024+(angles[min(i+1,len(angles)-1)][j]-angles[i][j])*1024*alpha//256 for j in range(2)]
        assert f['physics'][6]==ap[0] and f['physics'][12]==ap[1],'Replay lost recorded pitch'
        assert p[0]==p[3]==(ap[0]>>8)&2044
        assert p[1]==p[4]==(-want[3])&2044
        ext=[]
        for j,(v,w) in enumerate(zip(extra[i],extra[min(i+1,len(extra)-1)])):
            delta=w-v
            if j==3:delta=(delta+1024)%2048-1024
            value=v+delta*alpha//256
            ext.append(value&2044 if j==3 else value)
        assert p[2]==p[5]==(ext[5]>>8)&2044,'Replay lost cross-slope mesh bank'
        assert p[6:9]==m[12:15]==ext[:3] and p[9]==ext[3],'Actual-camera replay interpolation differs'
        assert f['view'][5]==ext[4] and f['handling'][16]==ext[5]
        checked+=1;partial+=0<alpha<256
    assert checked>30 and partial>10,'Interpolation not exercised'
    paused=[f for f in result['fields'][1100:1140] if f['game'][2]==5]
    assert len({tuple(f['game'][4:8]+f['motion'][:3]) for f in paused})==1,'Replay moves during pause'
    assert all(f['game'][13] for f in paused)
    ended=[f for f in result['fields'] if f['replay'][8] and f['game'][2]==5]
    assert len(ended)>30 and len({f['replay'][4] for f in ended})==1
    assert ended[-1]['replay'][4]==samples[-1][7]
    assert result['fields'][-1]['game'][2]==0 and result['fields'][-1]['front'][1:3]==[0,0],'Option did not exit to Start'
    assert all(f['front'][16]==0 for f in result['fields'][80:]),'Replay/menu wrote scores'
    return {'recorded_pitch_pairs_verified':len(angles),'samples':len(samples),'interpolated_commits':checked,'fractional_commits':partial,'record_ticks':samples[-1][7],'checks':['real run samples','time interpolation','mesh positions and camera','wrapped heading','pause/resume','stable end','Option exit','no replay score writes']}
