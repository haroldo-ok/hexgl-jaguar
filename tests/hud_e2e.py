#!/usr/bin/env python3
"""Focused controller-only gauge sweep: speed, damage, destruction and reset."""
import json,hashlib
from e2e import R,run,common

def main():
    summary={'status':'FAIL','rom_sha256':hashlib.sha256((R/'rom/hexgl.j64').read_bytes()).hexdigest(),'cases':{}}
    try:
        for standard,h in [('ntsc',60),('pal',50)]:
            go=100+7*h
            inputs=f'100:a,{go+90}:a+left,{go+340}:option,{go+350}:none'
            captures=[180,280,*[go+i for i in [6,10,14,18,26,60,94,112,132,152,172,192,212,232,252,300,330,360]]]
            result=run('hud-live-'+standard,standard,go+380,inputs,['--no-bios','--dump-max','32','--dump-at',','.join(map(str,captures))])
            common(result);c=result['bitmap_hud']['captures']
            speeds={v['speed'] for v in c};shields={v['shield'] for v in c}
            assert {0,28}.issubset(speeds) and any(0<v<28 for v in speeds),'Missing actual partial/full/zero speed'
            assert {0,100}.issubset(shields) and any(0<v<100 for v in shields),'Missing actual partial/full/empty shield'
            assert any(f['game'][2]==2 for f in result['fields']),'No destruction'
            assert result['fields'][-1]['game'][2]==0 and c[-1]['shield']==100 and c[-1]['speed']==0,'Restart did not restore visible gauges'
            summary['cases'][standard]={'checks':['throttle/collision speed levels','collision shield loss','empty shield on destruction','full shield after reset','actual source-art pixel equality'],'speeds_seen':sorted(speeds),'shields_seen':sorted(shields),'fields':len(result['fields']),'bitmap_hud':result['bitmap_hud']}
        summary['status']='PASS'
    finally:(R/'test-results/hud-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
