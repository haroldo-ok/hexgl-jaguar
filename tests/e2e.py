#!/usr/bin/env python3
"""End-to-end tests: retail BIOS -> ROM loader -> GPU/DSP -> TOM video.
Uses Virtual Jaguar Rx's real CPU/device cores, not a mock or a web remake.
Native state is READ ONLY; all control comes through VJ's joystick input.
The halt-GPU negative control only disables emulator execution, not game code.
"""
from pathlib import Path
import argparse,json,subprocess,hashlib,time,sys,shutil
import motion_checks,hud_checks
HUD_EVIDENCE={}
R=Path(__file__).resolve().parents[1]
MAGIC=0x48455847
def hz(standard): return 60 if standard=='ntsc' else 50

def manual_input(standard):
    d=7*hz(standard)
    return f'100:a,{d+180}:a+left,{d+205}:a,{d+250}:pause,{d+265}:none,{d+400}:pause,{d+415}:a,{d+500}:option,{d+520}:a,{2*d+1000}:option,{2*d+1020}:a'

def run(name,standard,frames,input,extra=(),expect_failure=False):
    d=R/'test-results'/name;d.mkdir(parents=True,exist_ok=True)
    args=[str(R/'tests/vjrunner/vjrun'),'--symbols',str(R/'src/hexgl.equ'),'--frames',str(frames),'--'+standard,'--out',str(d),'--input',input,'--quiet','--dump-at','80,180,280,380,480,580,800,1200,2400,4800,8000,12000','--title','run',*extra,str(R/'rom/hexgl.j64')]
    if '--eeprom-dir' not in extra:shutil.rmtree(d/'eeprom',ignore_errors=True)
    for old in d.glob('frame_*.png'):old.unlink()
    (d/'run_report.json.gz').unlink(missing_ok=True)
    (d/'invocation.json').write_text(json.dumps({'args':args,'rom_sha256':hashlib.sha256((R/'rom/hexgl.j64').read_bytes()).hexdigest()},indent=2)+'\n')
    (d/'run_report.json').unlink(missing_ok=True)
    t=time.time()
    with (d/'emulator.log').open('w') as f:
        c=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=900)
    result=json.loads((d/'run_report.json').read_text())
    print(name,'exit',c.returncode,'fields',result['field_count'],'elapsed',round(time.time()-t,1),'s',flush=True)
    (d/'ram.bin').unlink(missing_ok=True)
    assert c.returncode in (0,1),'Emulator crashed or setup failed'
    if not expect_failure:assert c.returncode==0,'Emulator watchdog failed; see '+str(d/'emulator.log')
    assert result['field_count']==len(result['fields']),'Truncated trace'
    assert len(result['fields'])==frames or '--stop-on-finish' in extra,'Incomplete run'
    result['output_dir']=str(d)
    result['process_exit_code']=c.returncode
    result['boot_mode']='direct' if '--no-bios' in extra else 'bios'
    if not expect_failure:
        result['bitmap_hud']=hud_checks.verify(result)
        HUD_EVIDENCE[name]=result['bitmap_hud']
    return result

def common(result):
    s=result['fields'];assert len(s)>200
    live=[f for f in s if f['game'][0]==MAGIC]
    assert live and live[0]['f']<120,'ROM never reached native gameplay'
    assert result['worst_black_streak']<=45,'Black-screen watchdog'
    assert all(f['game'][0]==MAGIC for f in s[150:]),'Native state lost'
    assert min(f['world_lit'] for f in s[150:])>1500,'World viewport black (includes final field)'
    for start in range(150,len(s)-29,30):
        w=s[start:start+90]
        assert len({f['game'][1] for f in w})>1,f'GPU/game heartbeat stalled at field {start}'
        assert min(f['world_lit'] for f in w)>1500,f'World viewport black at {start}'
        if len(w)>=90 and all((f['game'][2]==1 or (f['game'][2]==5 and not f.get('replay',[0]*9)[8])) and not f['game'][13] and f['game'][8]>10 for f in w):
            assert any(f['world_changed']>100 for f in w),f'World framebuffer frozen at {start}'
    assert s[-1]['audio_samples']>s[120]['audio_samples']+1000,'ROM DSP PCM mixer stalled'
    assert sum(f['audio_nonzero']>100 for f in s[120:])>len(s[120:])*.8,'Audio is silent'
    return s

def rendered_hud(result,finished=False):
    """Match real glyph pixels, not just strings/telemetry, in TOM screenshots."""
    import numpy as np
    from PIL import Image
    font=(R/'vendor/new_bjl/font/light8x8.fnt').read_bytes()
    def glyphs(text):
        return np.concatenate([np.unpackbits(np.frombuffer(font[8+ord(c)*8:8+(ord(c)+1)*8],dtype=np.uint8)).reshape(8,8) for c in text],axis=1).astype(bool)
    directory=Path(result['output_dir'])
    image=np.asarray(Image.open(directory/('final.png' if finished else 'frame_00180.png')).convert('RGB'))
    mask=image.max(axis=2)>150
    text='FINISH' if finished else 'GET READY';expected=glyphs(text);location=None
    for y in range(190,mask.shape[0]-31):
        for x in range(50):
            crop=mask[y:y+8,x:x+expected.shape[1]]
            if crop.shape==expected.shape and np.array_equal(crop,expected):location=(x,y);break
        if location:break
    assert location,'Countdown/finish message not visibly rendered in the captured HUD'
    x,y=location
    if finished:
        strings=result['fields'][-1]['times']
        for value,(col,row) in zip(strings,[(5,2),(19,2),(34,2),(3,3),(18,3),(33,3)]):
            expected=glyphs(value);crop=mask[y+row*8:y+row*8+8,x+col*8:x+col*8+expected.shape[1]]
            assert crop.shape==expected.shape and np.array_equal(crop,expected),'Lap/result digits missing, clipped or different in actual framebuffer'
    else:
        second=np.asarray(Image.open(directory/'frame_00280.png').convert('RGB')).max(axis=2)>150
        expected=glyphs('3')
        assert np.array_equal(second[y:y+8,x:x+8],expected),'Countdown 3 not actually visible'

def countdown(result,check_pause=False):
    s=common(result);h=hz(result['video'].lower());d=7*h
    assert {f['game'][20] for f in s[150:]}=={h},'Wrong video clock rate'
    cd=[f for f in s if f['game'][2]==4]
    assert cd,'Countdown was skipped'
    # Restrict to first countdown (manual tests contain subsequent restarts).
    go=next(f['f'] for f in s if f['game'][2]==1)
    first=[f for f in cd if f['f']<go]
    assert all(f['game'][16]==0 and f['game'][8]==0 for f in first),'Countdown allowed timer/throttle'
    assert len({tuple(f['game'][4:8]) for f in first})==1,'Ship moved/steered before GO'
    stages=[f['message'].strip() for f in first]
    for label in ['GET READY','3','2','1']:assert label in stages,'Missing countdown display '+label
    observed=[]
    for m in stages:
        if m in ['GET READY','3','2','1'] and (not observed or m!=observed[-1]):observed.append(m)
    assert observed==['GET READY','3','2','1'],'Wrong countdown order'
    for label,lo,hi in [('3',2.5,4),('2',4,5.5),('1',5.5,7)]:
        t=next(f['game'][3] for f in first if f['message'].strip()==label)
        assert lo*h<=t<=lo*h+10,('Bad countdown transition',label,t)
    assert 'GO' in [f['message'].strip() for f in s[go:go+h]],'GO message missing'
    expected=d+(200 if check_pause else 0)
    assert abs(go-first[0]['f']-expected)<=10,'Countdown duration differs from original 7 seconds'
    if check_pause:
        w=s[180:320]
        assert all(f['game'][13]==1 and f['game'][2]==4 for f in w)
        assert len({f['game'][3] for f in w})==1,'Countdown advanced while paused'
        assert all(f['message'].strip().startswith('PAUSED') for f in w)
    return go

def milliseconds(text):
    import re
    assert re.fullmatch(r'\d{2}:\d{2}\.\d{3}',text),('Malformed displayed time',text)
    return int(text[:2])*60000+int(text[3:5])*1000+int(text[6:])

def timing(result):
    s=result['fields'];h=hz(result['video'].lower())
    for f in s[160:]:
        g=f['game']
        if g[2] not in (1,3):continue
        shown=milliseconds(f['times'][0]);expected=g[16]*1000//h
        # Capture can occur in the middle of HUD drawing; at most one native
        # update of display latency is allowed, never a cumulative clock drift.
        assert -1<=expected-shown<=250,('HUD elapsed time mismatch',f['f'],expected,shown)
    # Raw VBL delta, not capped physics dt or number of rendered frames.
    for a,b in zip(s[160:],s[161:]):
        ga,gb=a['game'],b['game']
        if ga[2]==gb[2]==1 and not ga[13] and not gb[13] and gb[1]!=ga[1]:
            assert gb[16]-ga[16]==gb[18]-ga[18],'Race timer drifts from video clock'

def manual(result):
    s=common(result);d=7*hz(result['video'].lower());countdown(result);timing(result);rendered_hud(result);motion_checks.verify_motion(result)
    assert len({tuple(f['game'][4:7]) for f in s[d+110:d+175]})>8,'Throttle did not move ship'
    assert max(f['game'][8] for f in s[d+110:d+175])>=20,'Throttle did not accelerate'
    assert len({f['game'][7] for f in s[d+180:d+240]})>=3,'Steering did not change heading'
    assert len({tuple(f['game'][4:8]) for f in s[d+280:d+380]})==1,'Pause did not hold position'
    assert len({f['game'][16] for f in s[d+280:d+380]})==1,'Pause did not hold race timer'
    assert all(f['game'][13]==1 for f in s[d+280:d+380]),'Pause input not recognized'
    assert any(f['game'][9]<100 for f in s[d+220:d+250]),'Collision did not damage shield'
    assert any(f['game'][2]==2 for f in s[2*d+750:2*d+990]),'Destruction state not reached'
    assert s[2*d+1010]['game'][9]==100 and s[2*d+1010]['game'][2]==0,'Restart failed'
    assert all(x==0 for x in s[2*d+1010]['game'][21:26]),'Restart retained lap results'
    assert sum(f['world_changed']>100 for f in s[d+110:d+240])>=15,'Only HUD animated'
    return dict(checks=['direct cartridge boot' if result.get('boot_mode')=='direct' else 'BIOS boot','seven-second countdown','3/2/1/GO display','throttle locked until GO','wall-clock timing','formatted timer','nonblack world','heartbeat','audio','throttle','steering','pause/resume','collision','destruction','restart'],fields=len(s),updates=s[-1]['game'][1],audio_samples=s[-1]['audio_samples'])

def race(result):
    s=common(result);go=countdown(result);timing(result)
    motion=motion_checks.verify_motion(result)
    assert motion['height_filtered_updates']>500,'Track height filtering was not exercised'
    assert motion['left_bank_seen'] and motion['right_bank_seen'],'Autopilot did not bank both ways'
    for start in range(go+60,len(s)-90,90):
        w=s[start:start+90]
        if not all(f['game'][2]==1 for f in w):continue
        assert len({tuple(f['game'][4:7]) for f in w})>1,f'Autopilot did not move at {start}'
        assert any(f['world_changed']>100 for f in w),f'World framebuffer frozen at {start}'
    assert {0,1,2}.issubset({f['game'][11] for f in s[120:]}),'Missing checkpoint'
    assert {1,2,3}.issubset({f['game'][10] for f in s[120:]}),'Missing laps'
    assert any(f['game'][12]>0 for f in s),'Boost pads not detected'
    assert s[-1]['game'][2]==3 and s[-1]['game'][10]==4,'Three-lap finish missing'
    assert all(f['game'][9]==100 for f in s[120:]),'Autopilot left road'
    rendered_hud(result,finished=True)
    tail=s[-120:];g=tail[-1]['game'];splits=g[22:25]
    assert all(x>0 for x in splits) and sum(splits)==g[16],'Lap splits do not sum to finish time'
    assert g[25]==min(splits),'Best lap is wrong'
    assert len({f['game'][16] for f in tail})==1,'Finish clock did not stop'
    assert len({tuple(f['game'][4:8]) for f in tail})==1,'Ship moved after finish'
    assert len({tuple(f['times']) for f in tail})==1,'Result display not stable'
    assert all(f['message'].strip().startswith('FINISH') for f in tail),'Result message missing'
    assert 'FINAL LAP' in {f['message'].strip() for f in s},'Final-lap notification missing'
    for i,value in enumerate(splits):assert milliseconds(tail[-1]['times'][3+i])==value*1000//g[20],'Displayed split mismatch'
    assert milliseconds(tail[-1]['times'][2])==min(splits)*1000//g[20],'Displayed best lap mismatch'
    return dict(checks=['BIOS boot','countdown','nonblack world','heartbeat','audio','continuous world animation','checkpoints','boost','three laps','lap splits','best lap','frozen finish clock','finish results','bank filter','speed camera','terrain-height filtering','renderer pose'],motion_checks=motion,fields=len(s),updates=g[1],race_ticks=g[16],lap_ticks=splits,audio_samples=s[-1]['audio_samples'])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--quick',action='store_true');a=ap.parse_args()
    result={'rom_sha256':hashlib.sha256((R/'rom/hexgl.j64').read_bytes()).hexdigest(),'emulator':'Virtual Jaguar Rx 2.1.3 headless core harness','cases':{},'bitmap_hud':HUD_EVIDENCE,'status':'FAIL'}
    out=R/'test-results';out.mkdir(exist_ok=True)
    try:
        for standard in ['ntsc','pal']:
            for boot in ['bios','direct']:
                name='manual-'+standard+('-direct' if boot=='direct' else '')
                extra=['--no-bios'] if boot=='direct' else []
                result['cases'][name]=manual(run(name,standard,1200+14*hz(standard),manual_input(standard),extra))
            if not a.quick:
                name='race-'+standard
                result['cases'][name]=race(run(name,standard,18000,'100:a+c,120:a', ['--stop-on-finish']))
        for standard in ['ntsc','pal']:
            h=hz(standard)
            inputs,fields,t=motion_checks.bank_script(h)
            frames={k:t+offset*h-8 for k,offset in [('left',1),('right',3),('airbrake',5),('paused',8)]}
            trace=run('bank-'+standard,standard,fields,inputs,['--no-bios','--dump-max','20','--dump-at',','.join(map(str,frames.values()))])
            common(trace)
            case=motion_checks.bank_case(trace,t,h);case['capture_fields']=frames
            result['cases']['bank-'+standard]=case
            inputs,fields,go=motion_checks.speed_script(h)
            captures=[180,280,*range(go+h,go+h+32,2),go+2*h-4,go+2*h+12,go+3*h+20]
            trace=run('camera-speed-'+standard,standard,fields,inputs,['--no-bios','--dump-max','32','--dump-at',','.join(map(str,captures))])
            speeds={c['speed'] for c in trace['bitmap_hud']['captures']}
            assert {0,28}.issubset(speeds) and any(0<x<28 for x in speeds),'HUD did not visibly exercise empty, partial and full speed'
            common(trace)
            result['cases']['camera-speed-'+standard]=motion_checks.speed_case(trace,go,h)
        left=[result['cases']['bank-'+s]['half_second_left_roll_q8'] for s in ['ntsc','pal']]
        assert abs(left[0]-left[1])<2048,'Bank response differs excessively between PAL and NTSC'
        for standard in ['ntsc','pal']:
            name='countdown-pause-'+standard
            trace=run(name,standard,1200,'100:a+c,150:pause,170:none,350:pause,370:a',['--no-bios'])
            countdown(trace,check_pause=True);timing(trace)
            result['cases'][name]={'checks':['countdown pause/resume','seven-second active countdown','no premature movement','correct GO','timer formatting'],'fields':1200}
        for seed in [7,42]:
            name='cold-boot-seed-'+str(seed)
            trace=run(name,'ntsc',1100,'100:a+c,120:a',['--no-bios','--seed',str(seed)])
            common(trace)
            result['cases'][name]={'checks':['randomized power-on RAM','direct entry','nonblack world','heartbeat','world animation'],'fields':1100}
        for name,flag,expected in [('negative-frozen-gpu','--halt-gpu-at','black'),('negative-black-video','--blank-video-at','black'),('negative-frozen-video','--freeze-video-at','frozen')]:
            negative=run(name,'ntsc',1150,'100:a+c,120:a',[flag,'800'],expect_failure=True)
            try:common(negative)
            except AssertionError as e:
                assert expected in str(e).lower(),str(e)
                tail=negative['fields'][850:]
                if flag=='--halt-gpu-at':
                    assert len({f['game'][1] for f in tail})==1
                else:
                    assert len({f['game'][1] for f in tail})>10,'Video-only fault unexpectedly halted native gameplay'
                result['cases'][name]={'expected_failure_detected':str(e),'process_exit_code':negative['process_exit_code'],'native_heartbeat_stopped':flag=='--halt-gpu-at'}
            else:raise AssertionError('Watchdog falsely accepted '+name)
        result['status']='PASS_QUICK' if a.quick else 'PASS'
    except Exception as e:
        result['error']=str(e);raise
    finally:
        (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
