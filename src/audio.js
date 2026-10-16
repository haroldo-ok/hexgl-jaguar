; Five-channel PCM mixer on the DSP, paced by the real JERRY I2S latch.
; All original audio samples are streamed directly from cartridge ROM.
 dsp
 include "../assets/audio.inc"
 run $f1b000
 movei #$f1a100,r30
 movei #$3e00,r0
 store r0,(r30)
 nop
 nop
 movei #bg_start,r20
 movei #wind_start,r21
 movei #boost_start,r22
 movei #crash_end,r23
 movei #destroyed_end,r24
 moveq #0,r25
 moveq #0,r26
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
 ; Background loop, -6dB headroom for the effects.
 loadb (r20),r0
 addq #1,r20
 shlq #24,r0
 sharq #18,r0
 move r0,r10
 movei #bg_end,r1
 cmp r1,r20
 jr ne,.bgok
 nop
 movei #bg_start,r20
.bgok
 load (r14+32),r1
 cmpq #0,r1
 jr eq,.windskip
 nop
 loadb (r21),r0
 addq #1,r21
 shlq #24,r0
 sharq #19,r0
 add r0,r10
 movei #wind_end,r1
 cmp r1,r21
 jr ne,.windskip
 nop
 movei #wind_start,r21
.windskip
 load (r14+48),r1
 cmpq #0,r1
 jr eq,.boostskip
 nop
 loadb (r22),r0
 addq #1,r22
 shlq #24,r0
 sharq #19,r0
 add r0,r10
 movei #boost_end,r1
 cmp r1,r22
 jr ne,.boostskip
 nop
 movei #boost_start,r22
.boostskip
 load (r14+68),r0
 cmp r25,r0
 jr eq,.crashcheck
 nop
 move r0,r25
 jr cs,.crashcheck ; Counter reset or replay rewind is not a collision.
 nop
 movei #crash_start,r23
.crashcheck
 movei #crash_end,r1
 cmp r1,r23
 jr eq,.crashskip
 nop
 loadb (r23),r0
 addq #1,r23
 shlq #24,r0
 sharq #18,r0
 add r0,r10
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
.destroycheck
 movei #destroyed_end,r1
 cmp r1,r24
 jr eq,.destroyskip
 nop
 loadb (r24),r0
 addq #1,r24
 shlq #24,r0
 sharq #18,r0
 add r0,r10
.destroyskip
 movei #$f1a148,r0
 store r10,(r0)
 addq #4,r0
 store r10,(r0)
 ; Observable sample count belongs to the program, not the emulator.
 movei #$1084,r0
 load (r0),r1
 addq #1,r1
 store r1,(r0)
 jump (r29)
 nop
 align 8
 end
