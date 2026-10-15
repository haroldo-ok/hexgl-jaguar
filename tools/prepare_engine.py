#!/usr/bin/env python3
"""Prepare the platform entry point from the pinned upstream engine demo.
Renderer source files in src/ contain the separately maintained port changes.
"""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'vendor/jag_3d_engine/polygon.js').read_text()
s=s.replace('GOURAUD\t\tset 1','GOURAUD\t\tset 0').replace('LANDSCAPE\tset 1','LANDSCAPE\tset 0')
s=s.replace('CAM_X\t\tequ -60','CAM_X\t\tequ -9072').replace('CAM_Y\t\tequ 30','CAM_Y\t\tequ 1628').replace('CAM_Z\t\tequ 2500\t;2418','CAM_Z\t\tequ -3704').replace('CAM_ANGLE\tequ 228','CAM_ANGLE\tequ 0')
a=s.index('\tRSSET object_data');b=s.index('mem_end\tEQU RSADDR',a)
s=s[:a]+'''\tinclude "../assets/limits.inc"
\tRSSET object_data
\tdefobj scratch,MAX_VERTICES,MAX_FACES
\tRSALIGN 8
\tRSL tri_ptrs_ram,1024
\tRSB tri_array_ram,24*8192+32
tri_array_end equ RSADDR
'''+s[b:]
a=s.index('\tmovei\t#OBJECT_LIST,r0',s.index('skip_modules'));b=s.index('\tmovei\t#CAMERA_X,r15',a)
s=s[:a]+s[b:]
s=s.replace('\tMyINITMODULE engine\n\tMBL\tengine','\tMyINITMODULE control\n\tMBL control\n\tMyINITMODULE engine\n\tMBL\tengine')
s=s.replace('\tMyINITMODULE control\n\tMBL\tcontrol','')
a=s.index('\tPOP\tr1',s.index('main_loop:'));b=s.index('\tmovei\t#main_loop,r0',a)
s=s[:a]+'\tPOP r1\n\tPOP r0\n'+s[b:]
s=s.replace('Hallo:\t\tDC.B " 000000 tris   move: 123 + U/D focus:Opt",0','Hallo:\t\tDC.B "HEXGL   CITYSCAPE   /   ATARI JAGUAR",0')
s=s.replace('ms:\t\tDC.B "00FPS 000ms X 123456 Y 123456 Z 123456",0','ms:\t\tDC.B "A/UP THRUST  B BRAKE  LEFT/RIGHT STEER",0')
s=s.replace('info:\t\tdc.b "     3D poly engine (c)\'25 42Bastian",0','info:\t\tdc.b "OPTION RESTART   PAUSE   C AUTOPILOT",0')
s=s.replace('\tinclude "pobjects.inc"','world_list:\n\tinclude "../assets/model_list.inc"\n\tinclude "../assets/models.inc"')
a=s.index('\tinclude "textures/texture.inc"');b=s.index('\tIF MOD = 1',a)
s=s[:a]+'\tinclude "../assets/textures.inc"\n'+s[b:]
s=s.replace('\tinclude "engine.h"','\tinclude "engine.h"\n\tinclude "game.h"')
a=s.index('\tmoveq\t#FPS-1,r0',s.index('skip_modules'))
code='''; Load native DSP mixer after RAM initialization.
 movei #pcm_code,r0
 movei #$f1b000,r1
 movei #(pcm_end-pcm_code)/4,r2
.pcmcopy
 load (r0),r3
 store r3,(r1)
 addq #4,r0
 addq #4,r1
 subq #1,r2
 jr ne,.pcmcopy
 nop
 movei #$f1a100,r14
 movei #$3e00,r0
 store r0,(r14)
 movei #$f1b000,r0
 store r0,(r14+16)
 moveq #1,r0
 store r0,(r14+20)
'''
s=s[:a]+code+s[a:]
s=s.replace('\talign\t32\nende:', '\talign 8\npcm_code:\n\tincbin "audio.bin"\npcm_end:\n\talign\t32\nende:')
s=s.replace('#$0FF0F0FF,r1','#$000088ff,r1')
a=s.index('\nlogo:\n');b=s.index('\n\talign 4\nASCII',a)
s=s[:a]+'\nlogo:\n\tdc.l 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n'+s[b:]
(R/'src/hexgl.js').write_text(s)
