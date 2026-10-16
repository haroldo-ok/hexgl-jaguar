#!/usr/bin/env python3
"""Native menu, replay, real EEPROM persistence and corrupt-journal recovery."""
import argparse,json,hashlib,gzip,shutil,struct
from pathlib import Path
from e2e import R,run,common
import frontend_checks as fc

def summary_save(summary):
    required={'menu-ntsc','menu-pal','replay-ntsc','replay-pal','save-ntsc','save-pal','journal-torn','journal-checksum','journal-wrap','journal-invalid'}
    summary['status']='PASS' if required.issubset(summary['cases']) else 'IN_PROGRESS'
    (R/'test-results/frontend-summary.json').write_text(json.dumps(summary,indent=2)+'\n')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--part',choices=['ui','save','all'],default='all');part=ap.parse_args().part
    sha=hashlib.sha256((R/'rom/hexgl.j64').read_bytes()).hexdigest();summary_path=R/'test-results/frontend-summary.json'
    summary=json.loads(summary_path.read_text()) if summary_path.exists() else {}
    if summary.get('rom_sha256')!=sha:summary={'rom_sha256':sha,'status':'IN_PROGRESS','cases':{}}
    summary['status']='IN_PROGRESS'
    for name in list(summary['cases']):
        is_ui=name.startswith(('menu-','replay-'))
        if part=='all' or (part=='ui' and is_ui) or (part=='save' and not is_ui):
            del summary['cases'][name]
    summary_path.write_text(json.dumps(summary,indent=2)+'\n')
    try:
        if part in ['ui','all']:
            for standard in ['ntsc','pal']:
                script='100:down,120:none,140:a,160:none,220:option,240:none,260:down,280:none,300:down,320:none,340:a,360:none,420:option,440:none,460:up,480:none,500:up,520:none,540:a,560:none,620:option,640:none,660:a,680:none'
                t=run('menu-'+standard,standard,950,script,['--no-bios','--dump-max','20','--dump-at','80,180,380,580,880'])
                common(t);s=t['fields'];d=Path(t['output_dir']);pixels=0
                for n,panel,text in [(180,1,'A / UP: THRUST'),(380,2,'MANUAL BEST'),(580,3,'HEXGL BY BKCORE')]:
                    assert s[n]['front'][2]==panel and s[n]['game'][2]==0
                    pixels+=fc.text_pixels(d/f'frame_{n:05d}.png',text,126,61,standard)
                assert s[880]['game'][2]==4 and all(f['game'][16]==0 for f in s[80:880])
                assert all(f['front'][16]==0 for f in s[80:])
                summary['cases']['menu-'+standard]={'checks':['controller navigation','controls/records/credits','Option return','real source font pixels','Start enters countdown','no unsolicited saves'],'source_font_pixels':pixels}
                script='100:a+c,120:a,850:option,870:none,900:up,920:none,950:a,970:none,1080:pause,1100:none,1150:pause,1170:none,1500:option,1520:none'
                if standard=='ntsc':script=script.replace('100:a+c,120:a','100:a,600:a+right,630:a')
                t=run('replay-'+standard,standard,1570,script,['--no-bios','--dump-max','24','--dump-at','880,1040,1140,1250,1460,1550'])
                common(t);case=fc.replay(t);case['recording_input']='manual throttle and steering' if standard=='ntsc' else 'autopilot'
                fc.text_pixels(Path(t['output_dir'])/'frame_01040.png','REPLAY   PAUSE / OPTION',24,65,standard)
                fc.text_pixels(Path(t['output_dir'])/'frame_01460.png','END OF RECORDING',24,89,standard)
                summary['cases']['replay-'+standard]=case
        if part in ['save','all']:
            core=json.loads((R/'test-results/summary.json').read_text())
            assert core['status']=='PASS' and core['rom_sha256']==sha,'Run full current-ROM core suite first'
            originals={}
            for standard in ['ntsc','pal']:
                directory=R/'test-results'/('race-'+standard)
                p=directory/'run_report.json'
                trace=json.loads(p.read_text()) if p.exists() else json.loads(gzip.decompress(p.with_suffix('.json.gz').read_bytes()))
                f=trace['fields'][-1];g=f['game'];state=f['front'];assert state[15]==2 and state[16]==9,'New result was not serially saved and verified once'
                ep=directory/'eeprom'/fc.filename();data=ep.read_bytes();assert len(data)==128
                manual=fc.choose(data,0);auto=fc.choose(data,16)
                assert manual is None and auto['total_ms']==g[16]*1000//g[20] and auto['lap_ms']==g[25]*1000//g[20]
                assert state[6:8]==[0,0] and state[10:12]==[auto['total_ms'],auto['lap_ms']]
                # Independent process, same cartridge EEPROM file; no RAM restored.
                t=run('save-reboot-'+standard,standard,400,'100:down,120:none,140:down,160:none,180:a,200:none',['--eeprom-dir',str(ep.parent),*(['--no-bios'] if standard=='ntsc' else [])])
                common(t);end=t['fields'][-1];assert end['front'][10:12]==state[10:12] and end['front'][17]==1 and end['front'][16]==0
                assert ep.read_bytes()==data,'Loading a record wrote EEPROM'
                fc.text_pixels(Path(t['output_dir'])/'final.png',end['records'][2],126,132,standard)
                summary['cases']['save-'+standard]={'checks':['real full-race serial EEPROM write','nine writes only on improvement','readback verified','new process cold-load','PAL/NTSC normalized milliseconds','manual/assisted separation','visible original-font saved time'],'record':auto,'eeprom_sha256':hashlib.sha256(data).hexdigest()}
                originals[standard]=data
            base=originals['ntsc'];old=fc.choose(base,16)
            for fault in ['torn','checksum','wrap','invalid']:
                directory=R/'test-results'/('journal-'+fault);directory.mkdir(exist_ok=True);epdir=directory/'fixture-eeprom';epdir.mkdir(exist_ok=True)
                data=bytearray(base)
                # Fault fixtures are EEPROM-format inputs, not fabricated race evidence.
                if fault in ['torn','checksum']:
                    data[48:64]=fc.encode(old['generation']+1,old['total_ms'],old['lap_ms'])
                    if fault=='torn':data[48:50]=b'\x00\x00'
                    else:data[62]^=1
                    expected=old['total_ms'];generation=old['generation']
                elif fault=='wrap':
                    data[32:48]=fc.encode(65535,old['total_ms'],old['lap_ms'])
                    data[48:64]=fc.encode(0,old['total_ms'],old['lap_ms']);expected=old['total_ms'];generation=0
                else:data[:]=b'\xff'*128;expected=0;generation=0
                (epdir/fc.filename()).write_bytes(data)
                t=run('journal-'+fault,'ntsc',400,'0:none',['--no-bios','--eeprom-dir',str(epdir)])
                common(t);end=t['fields'][-1];assert end['front'][10]==expected and end['front'][12]==generation
                assert end['front'][16]==0 and (epdir/fc.filename()).read_bytes()==data
                summary['cases']['journal-'+fault]={'checks':['EEPROM boot recovery','bounded boot/no freeze','no repair writes'],'fixture':fault,'loaded_total_ms':expected,'generation':generation}
    except Exception as e:
        summary['error']=str(e);summary['status']='FAIL';summary_path.write_text(json.dumps(summary,indent=2)+'\n');raise
    summary.pop('error',None);summary_save(summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
