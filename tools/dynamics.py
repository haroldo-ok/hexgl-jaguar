#!/usr/bin/env python3
"""Native ShipControls response tables, not substitute track content."""
from pathlib import Path
import math,json
R=Path(__file__).resolve().parents[1]
rows=[];tables={}
for hz in (60,50):
 rows_h=[]
 for dt in range(1,7):
  row=[round(256*(1-(1-r)**(dt*60/hz))) for r in (.35,.1,.4,.05)]
  rows_h.append(row);rows.append(' dc.l '+','.join(map(str,row)))
 tables[str(hz)]=rows_h
angles=[round(math.atan(i/256)*2048/(2*math.pi)*256) for i in range(129)]
(R/'assets/dynamics.inc').write_text(' align 4\ndynamics_coefficients:\n'+'\n'.join(rows)+'\natan_slope:\n'+'\n'.join(' dc.l '+','.join(map(str,angles[i:i+8])) for i in range(0,129,8))+'\n')
(R/'assets/dynamics.json').write_text(json.dumps({'source':'vendor/HexGL/bkcore/hexgl/ShipControls.js','rates':[.35,.1,.4,.05],'coefficients':tables,'atan_q8':angles,'drift_ratio_q8':26,'fall_native_units_per_60hz_field':80,'fall_seconds':1.5,'slope_probe_native_units':96},indent=2)+'\n')
