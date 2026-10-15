#!/usr/bin/env python3
"""End-to-end tests: retail BIOS -> ROM loader -> GPU/DSP -> TOM video.
Uses Virtual Jaguar Rx's real CPU/device cores, not a mock or a web remake.
Native state is READ ONLY; all control comes through VJ's joystick input.
The halt-GPU negative control only disables emulator execution, not game code.
"""
from pathlib import Path
import argparse,json,subprocess,hashlib,time,sys
R=Path(__file__).resolve().parents[1]
MAGIC=0x48455847
INPUT='100:a,180:a+left,205:a,250:pause,265:none,400:pause,415:a,500:option,520:a,1000:option,1020:a'

def run(name,standard,frames,input,extra=(),expect_failure=False):
    d=R/'test-results'/name;d.mkdir(parents=True,exist_ok=True)
    args=[str(R/'tests/vjrunner/vjrun'),'--frames',str(frames),'--'+standard,'--out',str(d),'--input',input,'--quiet','--dump-at','80,175,350,600,1200,2400,3600,4800,6000,8000,10000,12000','--title','run',*extra,str(R/'rom/hexgl.j64')]
    (d/'run_report.json').unlink(missing_ok=True)
    (d/'invocation.json').write_text(json.dumps({'args':args,'rom_sha256':hashlib.sha256((R/'rom/hexgl.j64').read_bytes()).hexdigest()},indent=2)+'\n')
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
    result['process_exit_code']=c.returncode
    result['boot_mode']='direct' if '--no-bios' in extra else 'bios'
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
        if len(w)>=90 and all(f['game'][2]==1 and not f['game'][13] and f['game'][8]>10 for f in w):
            assert any(f['world_changed']>100 for f in w),f'World framebuffer frozen at {start}'
    assert s[-1]['audio_samples']>s[120]['audio_samples']+1000,'ROM DSP PCM mixer stalled'
    assert sum(f['audio_nonzero']>100 for f in s[120:])>len(s[120:])*.8,'Audio is silent'
    return s

def manual(result):
    s=common(result)
    assert len({tuple(f['game'][4:7]) for f in s[110:175]})>8,'Throttle did not move ship'
    assert max(f['game'][8] for f in s[110:175])>=20,'Throttle did not accelerate'
    assert len({f['game'][7] for f in s[180:240]})>=3,'Steering did not change heading'
    assert len({tuple(f['game'][4:8]) for f in s[280:380]})==1,'Pause did not hold position'
    assert len({f['game'][16] for f in s[280:380]})==1,'Pause did not hold race timer'
    assert all(f['game'][13]==1 for f in s[280:380]),'Pause input not recognized'
    assert any(f['game'][9]<100 for f in s[220:250]),'Collision did not damage shield'
    assert any(f['game'][2]==2 for f in s[750:990]),'Destruction state not reached'
    assert s[1010]['game'][9]==100 and s[1010]['game'][2]==0,'Restart failed'
    assert sum(f['world_changed']>100 for f in s[110:240])>=15,'Only HUD animated'
    return dict(checks=['direct cartridge boot' if result.get('boot_mode')=='direct' else 'BIOS boot','native entry','nonblack world','GPU heartbeat','DSP sample clock','audible PCM','throttle','steering','pause/resume','collision damage','destruction','restart'],fields=len(s),updates=s[-1]['game'][1],audio_samples=s[-1]['audio_samples'])

def race(result):
    s=common(result)
    for start in range(180,len(s)-90,90):
        w=s[start:start+90]
        assert len({tuple(f['game'][4:7]) for f in w})>1,f'Autopilot did not move at {start}'
        assert any(f['world_changed']>100 for f in w),f'World framebuffer frozen at {start}'
    assert {0,1,2}.issubset({f['game'][11] for f in s[120:]}),'Missing checkpoint'
    assert {1,2,3}.issubset({f['game'][10] for f in s[120:]}),'Missing laps'
    assert any(f['game'][12]>0 for f in s),'Boost pads not detected'
    assert s[-1]['game'][2]==3,'Three-lap race did not finish'
    assert s[-1]['game'][10]==4,'Finish must follow three ordered lap crossings'
    assert all(f['game'][9]==100 for f in s[120:]),'Autopilot left road'
    return dict(checks=['BIOS boot','native entry','nonblack world','GPU heartbeat','DSP sample clock','audible PCM','continuous world animation','all checkpoints','boost pads','three laps','finish'],fields=len(s),updates=s[-1]['game'][1],race_ticks=s[-1]['game'][16],audio_samples=s[-1]['audio_samples'])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--quick',action='store_true');a=ap.parse_args()
    result={'rom_sha256':hashlib.sha256((R/'rom/hexgl.j64').read_bytes()).hexdigest(),'emulator':'Virtual Jaguar Rx 2.1.3 headless core harness','cases':{},'status':'FAIL'}
    out=R/'test-results';out.mkdir(exist_ok=True)
    try:
        for standard in ['ntsc','pal']:
            for boot in ['bios','direct']:
                name='manual-'+standard+('-direct' if boot=='direct' else '')
                extra=['--no-bios'] if boot=='direct' else []
                result['cases'][name]=manual(run(name,standard,1200,INPUT,extra))
            if not a.quick:
                name='race-'+standard
                result['cases'][name]=race(run(name,standard,18000,'100:a+c,120:a', ['--stop-on-finish']))
        for seed in [7,42]:
            name='cold-boot-seed-'+str(seed)
            trace=run(name,'ntsc',600,'100:a+c,120:a',['--no-bios','--seed',str(seed)])
            common(trace)
            result['cases'][name]={'checks':['randomized power-on RAM','direct entry','nonblack world','heartbeat','world animation'],'fields':600}
        for name,flag,expected in [('negative-frozen-gpu','--halt-gpu-at','black'),('negative-black-video','--blank-video-at','black'),('negative-frozen-video','--freeze-video-at','frozen')]:
            negative=run(name,'ntsc',750,'100:a+c,120:a',[flag,'400'],expect_failure=True)
            try:common(negative)
            except AssertionError as e:
                assert expected in str(e).lower(),str(e)
                tail=negative['fields'][450:]
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
