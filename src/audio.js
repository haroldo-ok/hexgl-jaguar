; Native original-stereo IMA ADPCM through stock JERRY I2S.
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
 move r20,r16
 movei #$1a80,r15
 movei #.bg_decoded,r18
 movei #decode_stereo,r17
 jump (r17)
 nop
.bg_decoded
 move r16,r20
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
 movei #$1a90,r0
 moveq #0,r1
 store r1,(r0)
.bgok
 load (r14+32),r1
 cmpq #0,r1
 movei #.windskip,r2
 jump eq,(r2)
 nop
 move r21,r16
 movei #$1a98,r15
 movei #.wind_decoded,r18
 movei #decode_stereo,r17
 jump (r17)
 nop
.wind_decoded
 move r16,r21
 sharq #3,r12
 sharq #3,r13
 add r12,r11
 add r13,r8
 movei #wind_end,r1
 cmp r1,r21
 jr ne,.windskip
 nop
 movei #wind_start,r21
 movei #$1aa8,r0
 moveq #0,r1
 store r1,(r0)
.windskip
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
 movei #$1ac0,r0
 moveq #0,r1
 store r1,(r0)
.booststate
 move r2,r19
 movei #boost_end,r1
 cmp r1,r22
 movei #.boostskip,r2
 jump eq,(r2)
 nop
 move r22,r16
 movei #$1ab0,r15
 movei #.boost_decoded,r18
 movei #decode_stereo,r17
 jump (r17)
 nop
.boost_decoded
 move r16,r22
 sharq #3,r12
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
 movei #$1ad8,r0
 moveq #0,r1
 store r1,(r0)
.crashcheck
 movei #crash_end,r1
 cmp r1,r23
 movei #.crashskip,r2
 jump eq,(r2)
 nop
 move r23,r16
 movei #$1ac8,r15
 movei #.crash_decoded,r18
 movei #decode_stereo,r17
 jump (r17)
 nop
.crash_decoded
 move r16,r23
 sharq #2,r12
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
 movei #$1af0,r0
 moveq #0,r1
 store r1,(r0)
.destroycheck
 movei #destroyed_end,r1
 cmp r1,r24
 movei #.destroyskip,r2
 jump eq,(r2)
 nop
 move r24,r16
 movei #$1ae0,r15
 movei #.destroyed_decoded,r18
 movei #decode_stereo,r17
 jump (r17)
 nop
.destroyed_decoded
 move r16,r24
 sharq #2,r12
 sharq #2,r13
 add r12,r10
 add r13,r9
.destroyskip
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
 load (r15+4),r4
 move r4,r0
 shlq #2,r0
 movei #adpcm_steps,r5
 add r0,r5
 load (r5),r0
 move r0,r1
 shrq #3,r1
 btst #0,r2
 jr eq,.left_bit1
 nop
 move r0,r5
 shrq #2,r5
 add r5,r1
.left_bit1
 btst #1,r2
 jr eq,.left_bit2
 nop
 move r0,r5
 shrq #1,r5
 add r5,r1
.left_bit2
 btst #2,r2
 jr eq,.left_sign
 nop
 add r0,r1
.left_sign
 btst #3,r2
 jr eq,.left_positive
 nop
 neg r1
.left_positive
 load (r15+0),r3
 add r1,r3
 sat16s r3
 store r3,(r15+0)
 move r3,r12
 moveq #7,r0
 and r0,r2
 shlq #2,r2
 movei #adpcm_delta,r5
 add r2,r5
 load (r5),r0
 add r0,r4
 cmpq #0,r4
 jr pl,.left_min
 nop
 moveq #0,r4
.left_min
 movei #88,r0
 cmp r0,r4
 jr mi,.left_max
 nop
 move r0,r4
.left_max
 store r4,(r15+4)
 move r7,r2
 moveq #15,r0
 and r0,r2
 load (r15+12),r4
 move r4,r0
 shlq #2,r0
 movei #adpcm_steps,r5
 add r0,r5
 load (r5),r0
 move r0,r1
 shrq #3,r1
 btst #0,r2
 jr eq,.right_bit1
 nop
 move r0,r5
 shrq #2,r5
 add r5,r1
.right_bit1
 btst #1,r2
 jr eq,.right_bit2
 nop
 move r0,r5
 shrq #1,r5
 add r5,r1
.right_bit2
 btst #2,r2
 jr eq,.right_sign
 nop
 add r0,r1
.right_sign
 btst #3,r2
 jr eq,.right_positive
 nop
 neg r1
.right_positive
 load (r15+8),r3
 add r1,r3
 sat16s r3
 store r3,(r15+8)
 move r3,r13
 moveq #7,r0
 and r0,r2
 shlq #2,r2
 movei #adpcm_delta,r5
 add r2,r5
 load (r5),r0
 add r0,r4
 cmpq #0,r4
 jr pl,.right_min
 nop
 moveq #0,r4
.right_min
 movei #88,r0
 cmp r0,r4
 jr mi,.right_max
 nop
 move r0,r4
.right_max
 store r4,(r15+12)
 jump (r18)
 nop
 include "../assets/adpcm.inc"
 align 8
 end
