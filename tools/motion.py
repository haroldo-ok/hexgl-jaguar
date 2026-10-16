#!/usr/bin/env python3
"""Fixed-point response coefficients, not replacement artwork/geometry.
Roll .08 and speed offset .30 are from upstream ShipControls/CameraChase.
Height response .15 is an explicit native adaptation. Coefficients are Q0.8;
compound per-60-Hz-step retention so PAL/NTSC have comparable response times.
"""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
rates=[.08,.30,.15]
rows=[];manifest={}
for hz in [60,50]:
    table=[]
    for fields in range(1,7):
        coefficients=[round(256*(1-(1-rate)**(fields*60/hz))) for rate in rates]
        table.append(coefficients);rows.append(' dc.l '+','.join(map(str,coefficients)))
    manifest[str(hz)]=table
(R/'assets/motion.inc').write_text('; Q0.8 bank/pullback/height coefficients: NTSC then PAL, dt 1..6.\n align 4\nmotion_coefficients:\n'+'\n'.join(rows)+'\n')
(R/'assets/motion.json').write_text(json.dumps({'rates_per_60hz_step':rates,'coefficients':manifest,'base_distance':160,'max_pullback':40,'bank_target':196,'airbrake_bank_target':332},indent=2)+'\n')
