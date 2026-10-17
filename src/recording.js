; Actual controller-driven run recording and elapsed-field interpolated playback.
 MODULE recording,MODend_irq
 PUSHLR
 movei #REPLAY,r15
 load (r15),r0
 movei #$5245504c,r1
 cmp r1,r0
 movei #record_initialized,r2
 jump eq,(r2)
 nop
 move r1,r3
 move r15,r0
 moveq #0,r1
 moveq #20,r2
.zero
 store r1,(r0)
 addq #4,r0
 subq #1,r2
 jr ne,.zero
 nop
 store r3,(r15)
record_initialized:
 movei #GAME,r14
 load (r15+8),r0
 cmpq #0,r0
 movei #replay_play,r1
 jump ne,(r1)
 nop
 load (r14+8),r0
 load (r15+24),r1
 store r0,(r15+24)
 cmpq #4,r0
 movei #.recordphase,r9
 jump ne,(r9)
 nop
 cmpq #4,r1
 movei #record_done,r2
 jump eq,(r2)
 nop
 moveq #0,r0
 store r0,(r15+4)
 store r0,(r15+28)
 store r0,(r15+32)
 store r0,(r15+36)
 load (r14+80),r0
 store r0,(r15+56)
 jump (r2)
 nop
.recordphase
 cmpq #1,r0
 jr eq,.capture
 nop
 cmpq #1,r1
 movei #record_done,r2
 jump ne,(r2)
 nop
 cmpq #2,r0
 jr eq,.capture
 nop
 cmpq #3,r0
 jump ne,(r2)
 nop
.capture
 load (r14+52),r0
 cmpq #0,r0
 movei #record_done,r2
 jump ne,(r2)
 nop
 load (r15+4),r0
 cmpq #0,r0
 jr eq,.space
 nop
 load (r14+64),r1
 load (r15+36),r3
 cmp r3,r1
 jump eq,(r2)
 nop
.space
 movei #REPLAY_CAPACITY,r1
 cmp r1,r0
 jr cs,.write
 nop
 moveq #1,r0
 store r0,(r15+28)
 jump (r2)
 nop
.write
 move r0,r16
 shlq #6,r16
 movei #REPLAY_BUFFER,r1
 add r1,r16
 movei #record_sources-MODrun_recording+MODstart_recording,r17
 moveq #16,r18
.copy
 load (r17),r0
 addq #4,r17
 load (r0),r0
 store r0,(r16)
 addq #4,r16
 subq #1,r18
 jr ne,.copy
 nop
 ; Compact signed Euler steps supplement each complete record, in reserved RAM.
 load (r15+4),r0
 shlq #1,r0
 movei #REPLAY_ANGLES,r1
 add r0,r1
 movei #PHYS+24,r0
 load (r0),r0
 sharq #10,r0
 storeb r0,(r1)
 addq #1,r1
 movei #PHYS+48,r0
 load (r0),r0
 sharq #10,r0
 storeb r0,(r1)
 ; Actual camera and composed bank supplement the 64-byte gameplay sample.
 load (r15+4),r16
 moveq #24,r0
 mult r0,r16
 movei #REPLAY_VIEW,r0
 add r0,r16
 movei #record_extra_sources-MODrun_recording+MODstart_recording,r17
 moveq #6,r18
.extra_write
 load (r17),r0
 addq #4,r17
 load (r0),r0
 store r0,(r16)
 addq #4,r16
 subq #1,r18
 jr ne,.extra_write
 nop
 load (r14+88),r0
 store r0,(r15+68)
 load (r14+92),r0
 store r0,(r15+72)
 load (r14+96),r0
 store r0,(r15+76)
 load (r14+64),r0
 store r0,(r15+36)
 load (r15+4),r0
 addq #1,r0
 store r0,(r15+4)
record_done:
 POPLR

replay_play:
 movei #LastJoy+4,r0
 load (r0),r0
 btst #JOY_OPTION_BIT,r0
 jr eq,.keepplaying
 nop
 moveq #0,r0
 store r0,(r15+8)
 store r0,(r15+24)
 movei #record_done,r0
 jump (r0)
 nop
.keepplaying
 movei #VBL_TICKS,r0
 load (r0),r0
 load (r15+20),r1
 store r0,(r15+20)
 sub r1,r0
 load (r14+52),r1
 cmpq #0,r1
 jr eq,.notpaused
 nop
 moveq #0,r0
.notpaused
 load (r15+16),r1
 add r0,r1
 store r1,(r15+16)
 load (r15+12),r20
 load (r15+4),r21
 subq #1,r21
 movei #REPLAY_BUFFER,r22
.seek
 move r20,r23
 shlq #6,r23
 add r22,r23
 cmp r21,r20
 movei #.end,r9
 jump eq,(r9)
 nop
 move r23,r24
 addq #32,r24
 addq #32,r24
 move r24,r0
 addq #28,r0
 load (r0),r0
 cmp r0,r1
 movei #.span,r9
 jump cs,(r9)
 nop
 addq #1,r20
 movei #.seek,r8
 jump (r8)
 nop
.end
 moveq #1,r0
 store r0,(r15+32)
 move r23,r24
 moveq #0,r25
 move r23,r0
 addq #28,r0
 load (r0),r0
 store r0,(r15+16)
 store r0,(r15+48)
 store r0,(r15+52)
 jr .apply
 nop
.span
 store r0,(r15+52)
 move r23,r2
 addq #28,r2
 load (r2),r2
 store r2,(r15+48)
 sub r2,r0
 sub r2,r1
 shlq #8,r1
 div r0,r1
 move r1,r25
.apply
 store r20,(r15+12)
 store r25,(r15+44)
 ; Interpolate position and all recorded camera/roll coordinates, not waypoints.
 moveq #0,r26
.component
 move r23,r0
 add r26,r0
 load (r0),r0
 move r24,r1
 add r26,r1
 load (r1),r1
 sub r0,r1
 cmpq #12,r26
 jr ne,.linear
 nop
 movei #1024,r2
 add r2,r1
 movei #2047,r3
 and r3,r1
 sub r2,r1
.linear
 movei #replay_lerp,r8
 BL (r8)
 movei #replay_destinations-MODrun_recording+MODstart_recording,r1
 add r26,r1
 load (r1),r1
 cmpq #12,r26
 jr ne,.store
 nop
 movei #2044,r2
 and r2,r0
.store
 store r0,(r1)
 addq #4,r26
 moveq #28,r2
 cmp r2,r26
 movei #.component,r8
 jump ne,(r8)
 nop
 ; Interpolate recorded pitch steps; never recompute playback physics.
 move r20,r16
 shlq #1,r16
 movei #REPLAY_ANGLES,r0
 add r0,r16
 move r24,r17
 movei #REPLAY_BUFFER,r0
 sub r0,r17
 shrq #5,r17
 movei #REPLAY_ANGLES,r0
 add r0,r17
 movei #PHYS+24,r18
 movei #replay_angle,r8
 BL (r8)
 addq #1,r16
 addq #1,r17
 movei #PHYS+48,r18
 movei #replay_angle,r8
 BL (r8)
 ; Replay the recorded actual view, not the current live view/settings.
 move r23,r16
 move r24,r17
 movei #REPLAY_BUFFER,r0
 sub r0,r16
 sub r0,r17
 shrq #6,r16
 shrq #6,r17
 moveq #24,r0
 mult r0,r16
 mult r0,r17
 movei #REPLAY_VIEW,r0
 add r0,r16
 add r0,r17
 movei #record_extra_sources-MODrun_recording+MODstart_recording,r21
 moveq #6,r20
.extra_read
 load (r16),r0
 load (r17),r1
 addq #4,r16
 addq #4,r17
 sub r0,r1
 cmpq #3,r20
 jr ne,.extra_linear
 nop
 movei #1024,r2
 add r2,r1
 movei #2047,r3
 and r3,r1
 sub r2,r1
.extra_linear
 movei #replay_lerp,r8
 BL (r8)
 cmpq #3,r20
 jr ne,.extra_store
 nop
 movei #2044,r1
 and r1,r0
.extra_store
 load (r21),r1
 addq #4,r21
 store r0,(r1)
 subq #1,r20
 movei #.extra_read,r8
 jump ne,(r8)
 nop
 ; Step-valued telemetry/audio events use the preceding sample, not interpolation.
 move r23,r16
 addq #32,r16
 movei #replay_steps-MODrun_recording+MODstart_recording,r17
 moveq #8,r18
.step
 load (r16),r0
 addq #4,r16
 load (r17),r1
 addq #4,r17
 store r0,(r1)
 subq #1,r18
 jr ne,.step
 nop
 load (r14+40),r0
 moveq #0,r1
 cmpq #1,r0
 jr cs,.lap1zero
 nop
 jr eq,.lap1zero
 nop
 load (r15+68),r1
.lap1zero
 store r1,(r14+88)
 moveq #0,r1
 cmpq #2,r0
 jr cs,.lap2zero
 nop
 jr eq,.lap2zero
 nop
 load (r15+72),r1
.lap2zero
 store r1,(r14+92)
 moveq #0,r1
 cmpq #3,r0
 jr cs,.lap3zero
 nop
 jr eq,.lap3zero
 nop
 load (r15+76),r1
.lap3zero
 store r1,(r14+96)
 load (r15+16),r0
 store r0,(r14+64)
 moveq #5,r0
 store r0,(r14+8)
 load (r15+40),r0
 addq #1,r0
 store r0,(r15+40)
 movei #MOTION+64,r0
 load (r0),r0
 addq #1,r0
 store r0,(r15+60)
 movei #record_done,r0
 jump (r0)
 nop

replay_angle:
 PUSHLR
 loadb (r16),r0
 loadb (r17),r1
 shlq #24,r0
 shlq #24,r1
 sharq #14,r0
 sharq #14,r1
 sub r0,r1
 movei #replay_lerp,r8
 BL (r8)
 store r0,(r18)
 POPLR

; r0 base + ((signed r1 delta * r25 Q8 alpha)>>8), exact split IMULT.
replay_lerp:
 move r1,r2
 sharq #8,r2
 movei #255,r3
 and r3,r1
 imult r25,r2
 mult r25,r1
 shrq #8,r1
 add r2,r0
 add r1,r0
 jump (LR)
 nop
 align 4
record_extra_sources:
 dc.l VIEW+32,VIEW+36,VIEW+40,VIEW+16,VIEW+20,HANDLING+64
record_sources:
 dc.l GAME+16,GAME+20,GAME+24,GAME+28,MOTION,MOTION+4,MOTION+8,GAME+64
 dc.l GAME+32,GAME+36,GAME+40,GAME+48,GAME+68,GAME+8,GAME+84,GAME+100
replay_destinations:
 dc.l GAME+16,GAME+20,GAME+24,GAME+28,MOTION,MOTION+4,MOTION+8
replay_steps:
 dc.l GAME+32,GAME+36,GAME+40,GAME+48,GAME+68,REPLAY+64,GAME+84,GAME+100
 align 8
 ENDMODULE recording
 echo "ENDE (recording): %HMODend_recording"
