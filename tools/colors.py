#!/usr/bin/env python3
"""Real CrY DAC decode and RGB555->CrY requantization for native blending."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from cry import ch,cry
R=Path(__file__).resolve().parents[1]
def main():
 decode=bytearray()
 for color in np.rint(ch*255).astype(int):decode.extend(bytes([0,*color]))
 values=np.arange(32768)
 rgb=np.stack([((values>>10)&31)*8,((values>>5)&31)*8,(values&31)*8],axis=-1).astype('uint8').reshape(128,256,3)
 encode=cry(Image.fromarray(rgb))
 (R/'assets/color-decode.bin').write_bytes(decode)
 (R/'assets/color-encode.bin').write_bytes(encode)
 (R/'assets/colors.json').write_text(json.dumps({'decode':'256 x 0x00RRGGBB chroma DAC coefficients, intensity multiplication >>8','encode':'32768 RGB555 colors, bit fields R10/G5/B0, intensity floor quantization','outputs':{n:hashlib.sha256((R/'assets'/n).read_bytes()).hexdigest() for n in ['color-decode.bin','color-encode.bin']}},indent=2)+'\n')
if __name__=='__main__':main()
