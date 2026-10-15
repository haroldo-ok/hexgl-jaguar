#!/usr/bin/env python3
"""Idempotently add a DAC write counter to a Virtual Jaguar source tree.

The headless test runner wants to know whether the emulated DSP is actually
pushing samples to the DAC (i.e. that the music player in the ROM is alive),
so we instrument VJ's DAC write path with a counter.  The change is tiny and
does not alter emulation behaviour.
"""
import re
import sys
import pathlib

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parents[2] / "vendor/virtualjaguar"))

h = root / "src/dac.h"
c = root / "src/dac.cpp"

hdr_decl = ("\n// [hexgl-jaguar test harness] number of DAC writes since reset\n"
            "extern uint32_t dacWriteCount;\n")
cnt_decl = ("// [hexgl-jaguar test harness]\n"
            "uint32_t dacWriteCount = 0;\n\n")

def patch_header():
    t = h.read_text()
    if "dacWriteCount" in t:
        return False
    t = t.replace('#include "memory.h"\n', '#include "memory.h"\n' + hdr_decl, 1)
    h.write_text(t)
    return True

def patch_cpp():
    t = c.read_text()
    changed = False
    if "uint32_t dacWriteCount" not in t:
        t = t.replace("// Local variables\n", "// Local variables\n\n" + cnt_decl, 1)
        changed = True
    for fn in ("void DACWriteByte(", "void DACWriteWord("):
        idx = t.find(fn)
        if idx < 0:
            raise SystemExit("instrument_vj: cannot find " + fn)
        brace = t.find("{", idx)
        stmt = "\n\tdacWriteCount++;\t// [hexgl-jaguar test harness]\n"
        if "dacWriteCount++" not in t[brace:brace + 200]:
            t = t[:brace + 1] + stmt + t[brace + 1:]
            changed = True
    if changed:
        c.write_text(t)
    return changed

p1 = patch_header()
p2 = patch_cpp()
print("instrument_vj: %s (dac.h), %s (dac.cpp)" % ("patched" if p1 else "already patched",
                                                   "patched" if p2 else "already patched"))
