#!/usr/bin/env python3
"""Generate the repetitive five-channel native DSP IMA stereo mixer.
The produced src/audio.js is delivered and assembled directly by make rom.
"""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def call(name,register,channel):
 return f''' move {register},r16
 movei #${0x1a80+channel*24:x},r15
 movei #.{name}_decoded,r18
 movei #decode_stereo,r17
 jump (r17)
 nop
.{name}_decoded
 move r16,{register}
'''
def reset(channel):
 return f''' movei #${0x1a80+channel*24+16:x},r0
 moveq #0,r1
 store r1,(r0)
'''
s='''; Native original-stereo IMA ADPCM through stock JERRY I2S.
; Five channels, original complete durations; no host audio/ROM expansion.
 dsp
 include "../assets/audio.inc"
 run $f1b000
 movei #$f1a100,r30
 movei #$3e00,r0
 store r0,(r30)
 nop
 nop
 movei #$1a80,r0
 moveq #0,r1
 moveq #30,r2
.clear
 store r1,(r0)
 addq #4,r0
 subq #1,r2
 jr ne,.clear
 nop
 movei #bg_start,r20
 movei #wind_start,r21
 movei #boost_end,r22
 movei #crash_end,r23
 movei #destroyed_end,r24
 moveq #0,r25
 moveq #0,r26
 moveq #0,r19
 movei #$1000,r14
 movei #$f1a150,r0
 movei #51,r1
 store r1,(r0)
 addq #4,r0
 moveq #13,r1
 store r1,(r0)
 movei #$f1a114,r28
 movei #sample,r29
sample:
 load (r28),r0
 btst #7,r0
 jump eq,(r29)
 nop
 movei #1<<10,r0
 store r0,(r30)
 nop
 nop
'''
s+=call('bg','r20',0)+''' movei #$1f90,r0
 load (r0),r0
 cmpq #0,r0
 jr ne,.music_enabled
 nop
 moveq #0,r12
 moveq #0,r13
.music_enabled
 sharq #2,r12
 sharq #2,r13
 move r12,r10
 move r13,r9
 moveq #0,r11
 moveq #0,r8
 movei #bg_end,r1
 cmp r1,r20
 jr ne,.bgok
 nop
 movei #bg_start,r20
'''+reset(0)+'''.bgok
 load (r14+32),r1
 cmpq #0,r1
 movei #.windskip,r2
 jump eq,(r2)
 nop
'''+call('wind','r21',1)+''' sharq #3,r12
 sharq #3,r13
 add r12,r11
 add r13,r8
 movei #wind_end,r1
 cmp r1,r21
 jr ne,.windskip
 nop
 movei #wind_start,r21
'''+reset(1)+'''.windskip
 load (r14+48),r2
 cmpq #0,r2
 jr ne,.boostactive
 nop
 movei #boost_end,r22
 jr .booststate
 nop
.boostactive
 cmp r19,r2
 jr cs,.booststate
 nop
 jr eq,.booststate
 nop
 movei #boost_start,r22
'''+reset(2)+'''.booststate
 move r2,r19
 movei #boost_end,r1
 cmp r1,r22
 movei #.boostskip,r2
 jump eq,(r2)
 nop
'''+call('boost','r22',2)+''' sharq #3,r12
 sharq #3,r13
 add r12,r11
 add r13,r8
.boostskip
 load (r14+68),r0
 cmp r25,r0
 jr eq,.crashcheck
 nop
 move r0,r25
 jr cs,.crashcheck
 nop
 movei #crash_start,r23
'''+reset(3)+'''.crashcheck
 movei #crash_end,r1
 cmp r1,r23
 movei #.crashskip,r2
 jump eq,(r2)
 nop
'''+call('crash','r23',3)+''' sharq #2,r12
 sharq #2,r13
 add r12,r11
 add r13,r8
.crashskip
 load (r14+8),r0
 cmpq #5,r0
 jr ne,.live_phase
 nop
 movei #$1540,r0
 load (r0),r0
.live_phase
 cmp r26,r0
 jr eq,.destroycheck
 nop
 move r0,r26
 cmpq #2,r0
 jr ne,.destroycheck
 nop
 movei #destroyed_start,r24
'''+reset(4)+'''.destroycheck
 movei #destroyed_end,r1
 cmp r1,r24
 movei #.destroyskip,r2
 jump eq,(r2)
 nop
'''+call('destroyed','r24',4)+''' movei #$1f94,r0
 load (r0),r0
 cmpq #0,r0
 jr ne,.destroy_enabled
 nop
 moveq #0,r12
 moveq #0,r13
.destroy_enabled
 sharq #2,r12
 sharq #2,r13
 add r12,r10
 add r13,r9
.destroyskip
 movei #$1f94,r0
 load (r0),r0
 cmpq #0,r0
 jr ne,.sfx_enabled
 nop
 moveq #0,r11
 moveq #0,r8
.sfx_enabled
 ; Preserve source stereo; balance the spatial bus, never collapse music to mono.
 movei #$1604,r0
 load (r0),r16
 shlq #1,r16
 movei #112,r0
 cmp r0,r16
 jr mi,.panmax
 nop
 move r0,r16
.panmax
 neg r0
 cmp r0,r16
 jr pl,.panmin
 nop
 move r0,r16
.panmin
 movei #86,r0
 imult r0,r11
 imult r0,r8
 sharq #7,r11
 sharq #7,r8
 movei #128,r17
 move r17,r18
 sub r16,r17
 add r16,r18
 move r11,r12
 move r8,r13
 imult r17,r12
 imult r18,r13
 sharq #7,r12
 sharq #7,r13
 add r10,r12
 add r9,r13
 sat16s r12
 sat16s r13
 movei #$f1a148,r0
 store r12,(r0)
 addq #4,r0
 store r13,(r0)
 movei #$1a00,r15
 load (r15),r0
 addq #1,r0
 store r0,(r15)
 store r12,(r15+4)
 store r13,(r15+8)
 store r16,(r15+12)
 store r10,(r15+16)
 store r11,(r15+20)
 store r9,(r15+24)
 store r8,(r15+28)
 store r20,(r15+32)
 store r22,(r15+36)
 addq #1,r0
 store r0,(r15)
 movei #$1084,r0
 load (r0),r1
 addq #1,r1
 store r1,(r0)
 jump (r29)
 nop

; r16 cartridge cursor, r15 channel state, r18 return. r12/r13 decoded stereo.
; State: predictorL/indexL/predictorR/indexR/remaining/reserved, 24 bytes.
decode_stereo:
 load (r15+16),r0
 cmpq #0,r0
 movei #.packet,r1
 jump ne,(r1)
 nop
 loadw (r16),r0
 addq #2,r16
 shlq #16,r0
 sharq #16,r0
 store r0,(r15)
 loadw (r16),r0
 addq #2,r16
 store r0,(r15+4)
 loadw (r16),r0
 addq #2,r16
 shlq #16,r0
 sharq #16,r0
 store r0,(r15+8)
 loadw (r16),r0
 addq #2,r16
 store r0,(r15+12)
 movei #2048,r0
.packet
 subq #1,r0
 store r0,(r15+16)
 loadb (r16),r7
 addq #1,r16
 move r7,r2
 shrq #4,r2
'''
for side,offset,out in [('left',0,'r12'),('right',8,'r13')]:
 if side=='right':s+=' move r7,r2\n moveq #15,r0\n and r0,r2\n'
 s+=f''' load (r15+{offset+4}),r4
 move r4,r0
 shlq #2,r0
 movei #adpcm_steps,r5
 add r0,r5
 load (r5),r0
 move r0,r1
 shrq #3,r1
 btst #0,r2
 jr eq,.{side}_bit1
 nop
 move r0,r5
 shrq #2,r5
 add r5,r1
.{side}_bit1
 btst #1,r2
 jr eq,.{side}_bit2
 nop
 move r0,r5
 shrq #1,r5
 add r5,r1
.{side}_bit2
 btst #2,r2
 jr eq,.{side}_sign
 nop
 add r0,r1
.{side}_sign
 btst #3,r2
 jr eq,.{side}_positive
 nop
 neg r1
.{side}_positive
 load (r15+{offset}),r3
 add r1,r3
 sat16s r3
 store r3,(r15+{offset})
 move r3,{out}
 moveq #7,r0
 and r0,r2
 shlq #2,r2
 movei #adpcm_delta,r5
 add r2,r5
 load (r5),r0
 add r0,r4
 cmpq #0,r4
 jr pl,.{side}_min
 nop
 moveq #0,r4
.{side}_min
 movei #88,r0
 cmp r0,r4
 jr mi,.{side}_max
 nop
 move r0,r4
.{side}_max
 store r4,(r15+{offset+4})
'''
s+=' jump (r18)\n nop\n include "../assets/adpcm.inc"\n align 8\n end\n'
(R/'src/audio.js').write_text(s)
