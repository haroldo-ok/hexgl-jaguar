#!/usr/bin/env python3
"""Black-box end-to-end test of the STOCK Virtual Jaguar Qt/OpenGL executable.
No emulator patch, RAM reads/writes, custom ROM loader, or deterministic DSP
scheduler. Drives X11 keyboard events and captures actual displayed pixels.
Run under xvfb-run (make test-gui). Separate clean config for every launch.
"""
from pathlib import Path
import argparse, hashlib, json, os, shutil, signal, subprocess, tempfile, time
import numpy as np
from PIL import ImageGrab

ROOT=Path(__file__).resolve().parents[1]

class VisualFailure(AssertionError): pass

def command(*args):
    return subprocess.check_output(['xdotool',*map(str,args)],stderr=subprocess.DEVNULL,text=True,timeout=3).strip()

def world(image):
    # Image is the actual top-level VJ window. Exclude menus, status bar,
    # HUD (bottom 40 console lines), and the upper sky. Never score desktop.
    w,h=image.size
    return np.asarray(image.convert('RGB'))[int(h*.50):int(h*.78),int(w*.22):int(w*.78)].copy()

def metrics(pixels,previous=None):
    rgb=pixels.astype(np.int16)
    luma=(rgb[:,:,0]*30+rgb[:,:,1]*59+rgb[:,:,2]*11)/100
    return {'lit_fraction':float((luma>8).mean()),
            'contrast':float(luma.std()),
            'colors':int(len(np.unique((pixels//16).reshape(-1,3),axis=0))),
            'changed_fraction':None if previous is None else float((np.abs(rgb-previous.astype(np.int16)).max(axis=2)>8).mean())}

def visible(m):
    return m['lit_fraction']>.15 and m['contrast']>3 and m['colors']>=8

def run_case(binary,rom,out,standard,boot,freeze=False):
    out.mkdir(parents=True,exist_ok=True)
    for old in out.glob('capture-*.png'):old.unlink()
    samples=[]; p=None; win=None; previous=None; begin=time.monotonic()
    result={'status':'FAIL','rom_sha256':hashlib.sha256(rom.read_bytes()).hexdigest(),'video':standard,'boot':boot,'samples':samples}
    with tempfile.TemporaryDirectory(prefix='vj-home-') as home, (out/'emulator.log').open('w') as log:
        env=dict(os.environ,HOME=home,XDG_CONFIG_HOME=home+'/config',XDG_DATA_HOME=home+'/data',SDL_AUDIODRIVER='dummy',LIBGL_ALWAYS_SOFTWARE='1')
        argv=[binary,str(rom),'--'+standard,'--gpu','--dsp','--no-blur']
        if boot!='default':argv.append('--'+boot)
        result['command']=argv
        try:
            p=subprocess.Popen(argv,cwd=home,env=env,stdout=log,stderr=subprocess.STDOUT)
            deadline=time.monotonic()+15
            # A missing/non-mapped window cannot be mistaken for a working ROM.
            while time.monotonic()<deadline:
                if p.poll() is not None: raise VisualFailure('emulator exited before presenting video')
                try:
                    ids=command('search','--onlyvisible','--pid',p.pid).splitlines()
                    for wid in ids:
                        geo=dict(line.split('=',1) for line in command('getwindowgeometry','--shell',wid).splitlines())
                        if int(geo['WIDTH'])>=300 and int(geo['HEIGHT'])>=250:
                            win=wid;break
                    if win:break
                except subprocess.CalledProcessError:pass
                time.sleep(.25)
            if not win:
                ImageGrab.grab().save(out/'failure-desktop.png')
                raise VisualFailure('no game window by startup deadline')
            command('windowfocus',win)
            # Cursor parking is cosmetic, not a controller action. Some X11
            # setups reject a redundant warp; record it without skipping any
            # pixel/input assertions. Focus and all gameplay keys stay strict.
            try:command('mousemove',0,0)
            except subprocess.CalledProcessError:
                result.setdefault('warnings',[]).append('X11 cursor parking failed; all image/input assertions retained')
            geo=dict(line.split('=',1) for line in command('getwindowgeometry','--shell',win).splitlines())
            x,y,w,h=[int(geo[k]) for k in ('X','Y','WIDTH','HEIGHT')]
            bbox=(x,y,x+w,y+h);result['window_bbox']=bbox
            def capture(phase):
                nonlocal previous
                if p.poll() is not None:raise VisualFailure('emulator exited while running')
                image=ImageGrab.grab(bbox=bbox)
                pixels=world(image);m=metrics(pixels,previous);previous=pixels
                m.update(seconds=round(time.monotonic()-begin,3),phase=phase)
                samples.append(m)
                # Keep regular visual evidence without bloating the source bundle.
                if len(samples)%4==0 or len(samples)==1 or samples[-2]['phase']!=phase:
                    image.save(out/f'capture-{len(samples):03d}.png')
                image.save(out/'latest.png')
                return m
            # BIOS/logo/menu brightness alone is not sufficient: later checks
            # require track-region animation in response to controller input.
            while time.monotonic()<deadline:
                if visible(capture('boot')):break
                time.sleep(.5)
            else:raise VisualFailure('world black or untextured at startup deadline')
            def key(action,*keys):command(action,*keys)
            def observe(phase,seconds,moving=False,paused=False):
                end=time.monotonic()+seconds;dark_since=None;last_motion=time.monotonic();changed=0;stable=0
                while time.monotonic()<end:
                    time.sleep(.5);m=capture(phase);now=time.monotonic()
                    if not visible(m):
                        dark_since=dark_since or now
                        if now-dark_since>=1.5:raise VisualFailure('world black/untextured for 1.5 seconds')
                    else:dark_since=None
                    if (m['changed_fraction'] or 0)>.02:
                        changed+=1;last_motion=now
                    else:stable+=1
                    if moving and now-last_motion>3:raise VisualFailure('world frozen for 3 seconds during throttle')
                if moving and changed<3:raise VisualFailure('insufficient world animation after controller input')
                if paused and stable<3:raise VisualFailure('pause did not hold displayed world')
            def await_countdown():
                # Gameplay now intentionally remains still for seven emulated
                # seconds. Keep checking real pixels; wait for actual world
                # motion instead of treating a valid countdown as a freeze.
                # The new menu legitimately changes to a stationary track.
                # Establish its baseline before testing for premature motion.
                time.sleep(.5);capture('countdown-entry')
                start=time.monotonic();deadline=start+25
                while time.monotonic()<deadline:
                    time.sleep(.5);m=capture('countdown')
                    if not visible(m):raise VisualFailure('world black during countdown')
                    if (m['changed_fraction'] or 0)>.02:
                        if time.monotonic()-start<4:raise VisualFailure('ship moved before countdown')
                        return
                raise VisualFailure('countdown never reached moving gameplay')
            observe('idle',2)
            key('keydown','l','j');time.sleep(.35);key('keyup','j') # Jaguar A + C, then held A
            await_countdown()
            if freeze:
                observe('moving-before-freeze',4,moving=True)
                os.kill(p.pid,signal.SIGSTOP)
                observe('injected-process-freeze',5,moving=True)
                raise AssertionError('fault injection was not detected')
            observe('throttle-autopilot',8,moving=True)
            key('keydown','p');time.sleep(.25);key('keyup','p')
            observe('pause',3,paused=True)
            key('keydown','p');time.sleep(.25);key('keyup','p')
            observe('resume',4,moving=True)
            key('keyup','l');key('keydown','o');time.sleep(.3);key('keyup','o')
            observe('restart-ready',2)
            key('keydown','l','j');time.sleep(.3);key('keyup','j')
            await_countdown()
            observe('restart-moving',4,moving=True)
            key('keyup','l')
            result['status']='PASS'
        except VisualFailure as e:
            result['error']=str(e)
        except subprocess.CalledProcessError:
            # An intentionally corrupted entry may close its window while an
            # X11 operation is in flight. Only an observed process exit counts
            # as emulator failure; infrastructure errors still abort the suite.
            if p and p.poll() is not None:result['error']='emulator exited while running'
            else:raise
        finally:
            if p and p.poll() is None:
                if freeze:os.kill(p.pid,signal.SIGCONT)
                p.terminate()
                try:p.wait(timeout=2)
                except subprocess.TimeoutExpired:p.kill();p.wait()
            result['emulator_exit_code']=p.returncode if p else None
            result['elapsed_seconds']=round(time.monotonic()-begin,2)
            (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(out.name,result['status'],result.get('error',''),flush=True)
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,default=ROOT/'rom/hexgl.j64');ap.add_argument('--binary',default='virtualjaguar');ap.add_argument('--out',type=Path,default=ROOT/'test-results/gui');ap.add_argument('--case',choices=['default-ntsc','no-bios-ntsc','bios-ntsc','no-bios-pal','bios-pal']);a=ap.parse_args()
    if not os.environ.get('DISPLAY'):raise SystemExit('Run through xvfb-run -a -s "-screen 0 1024x768x24"')
    binary=shutil.which(a.binary)
    if not binary:raise SystemExit('Install the stock virtualjaguar executable')
    rom=a.rom.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
    summary={'status':'FAIL','rom_sha256':hashlib.sha256(rom.read_bytes()).hexdigest(),'emulator_binary_sha256':hashlib.sha256(Path(binary).read_bytes()).hexdigest(),'emulator_version':subprocess.check_output([binary,'--help'],text=True).splitlines()[0],'cases':{}}
    try:
        cases=[('ntsc','default'),('ntsc','no-bios'),('ntsc','bios'),('pal','no-bios'),('pal','bios')]
        for standard,boot in cases:
            name=boot+'-'+standard
            if a.case and name!=a.case:continue
            r=run_case(binary,rom,out/name,standard,boot)
            summary['cases'][name]={k:v for k,v in r.items() if k!='samples'}
            if r['status']!='PASS':raise VisualFailure(name+': '+r.get('error','failed'))
        if not a.case:
            # Recreate ONLY the old broken direct-entry vector. The encrypted
            # retail loader and game payload remain identical to this build.
            bad=bytearray(rom.read_bytes());bad[0x404:0x408]=(0x802000).to_bytes(4,'big')
            with tempfile.TemporaryDirectory(prefix='vj-negative-') as temp:
                badrom=Path(temp)/'broken-entry.j64';badrom.write_bytes(bad)
                r=run_case(binary,badrom,out/'negative-old-entry','ntsc','no-bios')
            assert r['status']=='FAIL' and r.get('error') in ('no game window by startup deadline','world black or untextured at startup deadline','emulator exited before presenting video','emulator exited while running'),'broken-entry fault was not rejected'
            summary['cases']['negative-old-entry']={'status':'EXPECTED_FAILURE','detected':r['error']}
            r=run_case(binary,rom,out/'negative-frozen-window','ntsc','no-bios',freeze=True)
            assert r['status']=='FAIL' and 'world frozen' in r.get('error',''),'frozen-window detector failed'
            summary['cases']['negative-frozen-window']={'status':'EXPECTED_FAILURE','detected':r['error']}
        summary['status']='PASS_SINGLE' if a.case else 'PASS'
    except Exception as e:
        summary['error']=str(e);raise
    finally:(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
