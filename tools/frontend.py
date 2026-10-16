#!/usr/bin/env python3
"""Native front-end assets from HexGL's actual bg/title and Bebas Neue font."""
from pathlib import Path
import hashlib,json,struct
from PIL import Image,ImageDraw,ImageFont,ImageOps
from cry import cry
R=Path(__file__).resolve().parents[1];S=R/'vendor/HexGL/css';A=R/'assets'
def main():
    font=ImageFont.truetype(str(S/'BebasNeue-webfont.ttf'),18)
    bg=ImageOps.fit(Image.open(S/'bg.jpg').convert('RGB'),(384,200),method=Image.Resampling.LANCZOS)
    # Original title, premultiplied-alpha Lanczos via Pillow RGBA.
    title=Image.open(S/'title.png').convert('RGBA').resize((112,70),Image.Resampling.LANCZOS)
    bg.paste(title,(6,66),title)
    # Native two-column placement; original assets, not substitute pictures.
    main=bg.copy();d=ImageDraw.Draw(main)
    for y,text in [(60,'START'),(82,'CONTROLS'),(104,'LOCAL RECORDS'),(126,'CREDITS'),(148,'REPLAY LAST RUN')]:
        d.text((136,y),text,font=font,fill='#4190bb')
    (A/'front-main.cry').write_bytes(cry(main));(A/'front-bg.cry').write_bytes(cry(bg))
    glyphs=[];widths=[]
    for code in range(32,128):
        im=Image.new('L',(16,24));ImageDraw.Draw(im).text((0,0),chr(code),font=font,fill=255)
        assert font.getbbox(chr(code))[2]<=16
        widths.append(max(1,min(16,round(font.getlength(chr(code))))))
        for y in range(24):glyphs.append(struct.pack('>H',sum((im.getpixel((x,y))>=128)<<(15-x) for x in range(16))))
    (A/'front-font.bin').write_bytes(b''.join(glyphs));(A/'front-widths.bin').write_bytes(bytes(widths))
    files=['bg.jpg','title.png','BebasNeue-webfont.ttf']
    manifest={'sources':{str((S/n).relative_to(R)):hashlib.sha256((S/n).read_bytes()).hexdigest() for n in files},'dimensions':[384,200],'font':{'size':18,'cell':[16,24],'codes':[32,127],'coverage':'monochrome 128 threshold'},'rom_offsets':{'front-main.cry':'0x590000','front-bg.cry':'0x5b5800'},'adaptations':['native two-column layout','Jaguar control labels','separate manual and autopilot local records'],'outputs':{n:hashlib.sha256((A/n).read_bytes()).hexdigest() for n in ['front-main.cry','front-bg.cry','front-font.bin','front-widths.bin']}}
    (A/'frontend.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (A/'frontend.inc').write_text('\talign 8\nfront_font:\n\tincbin "../assets/front-font.bin"\nfront_widths:\n\tincbin "../assets/front-widths.bin"\n')
    with (A/'frontend.inc').open('a') as f:
        for name,color in [('BLUE','#4190bb'),('ORANGE','#f66439'),('WHITE','#ffffff')]:
            f.write(f'FRONT_{name} equ ${int.from_bytes(cry(Image.new("RGB",(1,1),color)),"big"):04x}\n')
    print('Original front end converted; two backgrounds and actual Bebas Neue atlas')
if __name__=='__main__':main()
