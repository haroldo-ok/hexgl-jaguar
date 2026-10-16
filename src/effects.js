; Bounded world-space ShipEffects adaptation. Original sprite art, real emitters.
; Source: Thibaut BKcore Despoulain, ShipEffects.js, CC BY-NC 3.0. See NOTICE.md.
; 16 particles, 8 words each: x/y/z Q8, vx/vy/vz Q8 per 60Hz field, lifeQ8,type.
 MODULE effects,MODend_irq
 PUSHLR
 movei #BLIT_A1_BASE,r14
.wait
 load (r14+$38),r0
 btst #0,r0
 jr eq,.wait
 nop
 movei #GAME,r14
 movei #FX,r15
 load (r14+8),r0
 load (r15),r1
 movei #$46585331,r2
 cmp r2,r1
 movei #fx_reset,r1
 jump ne,(r1)
 nop
 cmpq #0,r0
 jump eq,(r1)
 nop
 cmpq #4,r0
 jump eq,(r1)
 nop
 cmpq #1,r0
 jr eq,.active
 nop
 cmpq #5,r0
 movei #fx_done,r1
 jump ne,(r1)
 nop
.active
 load (r14+52),r0
 cmpq #0,r0
 movei #fx_draw,r1
 jump ne,(r1)
 nop
 ; Replay end holds the effect simulation, just like its recorded pose.
 load (r14+8),r0
 cmpq #5,r0
 jr ne,.advance
 nop
 movei #REPLAY+32,r0
 load (r0),r0
 cmpq #0,r0
 jump ne,(r1)
 nop
.advance
 load (r14+112),r0
 movei #60*256,r1
 mult r1,r0
 load (r14+80),r1
 div r1,r0
 store r0,(r15+56)
 ; Spawn on genuine increasing collision events, never on counter resets.
 load (r14+68),r0
 load (r15+20),r1
 store r0,(r15+20)
 cmp r1,r0
 movei #fx_integrate,r2
 jump cs,(r2)
 nop
 jump eq,(r2)
 nop
 moveq #6,r18
.spawn
 load (r15+44),r0
 move r0,r16
 shlq #5,r16
 movei #FX_POOL,r1
 add r1,r16
 addq #1,r0
 moveq #15,r1
 and r1,r0
 store r0,(r15+44)
 ; Emit at the actual contacted side, 3 original units from the ship axis.
 movei #PHYS+36,r0
 load (r0),r0
 movei #-12,r2
 cmpq #1,r0
 jr eq,.sidechosen
 nop
 moveq #12,r2
 cmpq #2,r0
 jr eq,.sidechosen
 nop
 btst #0,r18
 jr eq,.sidechosen
 nop
 neg r2
.sidechosen
 load (r14+28),r0
 movei #SinTab,r1
 add r0,r1
 load (r1),r0
 move r0,r1
 shrq #16,r1
 imult r2,r0
 imult r2,r1
 sharq #7,r0
 sharq #7,r1
 move r0,r8
 load (r14+16),r0
 add r0,r1
 store r1,(r16)
 load (r14+20),r1
 move r16,r26
 addq #4,r26
 store r1,(r26)
 load (r14+24),r1
 add r8,r1
 move r16,r26
 addq #8,r26
 store r1,(r26)
 ; Deterministic xorshift randomness, independent of host timers.
 load (r15+40),r0
 move r0,r1
 shlq #13,r1
 xor r1,r0
 move r0,r1
 shrq #17,r1
 xor r1,r0
 move r0,r1
 shlq #5,r1
 xor r1,r0
 store r0,(r15+40)
 move r0,r1
 movei #511,r2
 and r2,r1
 movei #256,r2
 sub r2,r1
 move r16,r26
 addq #12,r26
 store r1,(r26)
 shrq #9,r0
 move r0,r1
 movei #255,r2
 and r2,r1
 move r16,r26
 addq #16,r26
 store r1,(r26)
 shrq #8,r0
 movei #511,r2
 and r2,r0
 movei #256,r2
 sub r2,r0
 move r16,r26
 addq #20,r26
 store r0,(r26)
 movei #60*256,r0
 move r16,r26
 addq #24,r26
 store r0,(r26)
 move r18,r0
 moveq #1,r1
 and r1,r0
 move r16,r26
 addq #28,r26
 store r0,(r26)
 load (r15+4),r0
 addq #1,r0
 store r0,(r15+4)
 subq #1,r18
 movei #.spawn,r0
 jump ne,(r0)
 nop
fx_integrate:
 movei #FX_POOL,r16
 moveq #16,r18
.update
 move r16,r26
 addq #24,r26
 load (r26),r0
 cmpq #0,r0
 movei #.next,r26
 jump eq,(r26)
 nop
 load (r15+56),r1
 sub r1,r0
 jr pl,.alive
 nop
 moveq #0,r0
.alive
 move r16,r26
 addq #24,r26
 store r0,(r26)
 move r16,r17
 moveq #3,r19
.xyz
 load (r17),r0
 addq #12,r17
 load (r17),r2
 subq #12,r17
 imult r1,r2
 sharq #8,r2
 add r2,r0
 store r0,(r17)
 addq #4,r17
 subq #1,r19
 jr ne,.xyz
 nop
.next
 addq #32,r16
 subq #1,r18
 movei #.update,r0
 jump ne,(r0)
 nop
fx_draw:
 moveq #0,r0
 store r0,(r15+8)
 store r0,(r15+12)
 store r0,(r15+16)
 movei #FX_POOL,r16
 moveq #16,r18
.draw
 move r16,r26
 addq #24,r26
 load (r26),r0
 cmpq #0,r0
 movei #.drawnext,r0
 jump eq,(r0)
 nop
 load (r15+8),r0
 addq #1,r0
 store r0,(r15+8)
 load (r16),r0
 move r16,r26
 addq #4,r26
 load (r26),r1
 move r16,r26
 addq #8,r26
 load (r26),r2
 move r16,r26
 addq #28,r26
 load (r26),r3
 move r16,r26
 addq #24,r26
 load (r26),r4
 movei #60,r5
 div r5,r4
 movei #fx_project,r8
 BL (r8)
.drawnext
 addq #32,r16
 subq #1,r18
 movei #.draw,r0
 jump ne,(r0)
 nop
 ; Exhaust glow follows the stern of the real ship, intensity follows speed/boost.
 load (r14+8),r0
 cmpq #5,r0
 jr ne,.live
 nop
 movei #REPLAY+64,r0
 load (r0),r0
.live
 cmpq #2,r0
 movei #fx_done,r1
 jump eq,(r1)
 nop
 load (r14+16),r0
 load (r14+20),r1
 load (r14+24),r2
 move r0,r21
 move r1,r22
 move r2,r23
 load (r14+28),r0
 movei #SinTab,r15
 load (r15+r0),r0
 move r0,r1
 shrq #16,r1
 moveq #18,r2
 imult r2,r0
 imult r2,r1
 sharq #7,r0
 sharq #7,r1
 add r0,r21
 sub r1,r23
 move r21,r0
 move r22,r1
 move r23,r2
 moveq #2,r3
 load (r14+32),r4
 shlq #2,r4
 movei #96,r5
 add r5,r4
 load (r14+48),r5
 cmpq #0,r5
 jr eq,.glow
 nop
 movei #255,r4
.glow
 movei #fx_project,r8
 BL (r8)
fx_done:
 movei #FX,r15
 load (r15+48),r0
 addq #1,r0
 store r0,(r15+48)
 POPLR
fx_reset:
 movei #FX,r15
 move r15,r0
 moveq #0,r1
 moveq #16,r2
.clear
 store r1,(r0)
 addq #4,r0
 subq #1,r2
 jr ne,.clear
 nop
 movei #$46585331,r0
 store r0,(r15)
 movei #$3a59b17d,r0
 store r0,(r15+40)
 movei #FX_POOL,r0
 movei #128,r2
.pool
 store r1,(r0)
 addq #4,r0
 subq #1,r2
 jr ne,.pool
 nop
 movei #fx_done,r0
 jump (r0)
 nop

; r0/r1/r2 Q8 world, r3 sprite 0/1/2, r4 opacity 0..256.
; Projection matches the engine's yaw, pitch, reciprocal and video aspect.
fx_project:
 PUSHLR
 move r3,r20
 move r4,r24
 sharq #8,r0
 sharq #8,r1
 sharq #8,r2
 movei #CAMERA_X,r15
 load (r15),r3
 load (r15+4),r4
 load (r15+8),r5
 sub r3,r0
 sub r4,r1
 sub r5,r2
 load (r15+12),r3
 movei #SinTab,r15
 load (r15+r3),r3
 move r3,r4
 shrq #16,r4
 imultn r4,r0
 imacn r3,r2
 resmac r5
 neg r3
 imultn r3,r0
 imacn r4,r2
 resmac r2
 sharq #15,r5
 sharq #15,r2
 movei #PHYS+48,r0
 load (r0),r0
 sharq #8,r0
 movei #2044,r3
 and r3,r0
 load (r15+r0),r3
 move r3,r4
 shrq #16,r4
 imultn r4,r1
 imacn r3,r2
 resmac r6
 neg r1
 imultn r4,r2
 imacn r3,r1
 resmac r2
 sharq #15,r6
 sharq #15,r2
 movei #.done,r0
 cmpq #10,r2
 jump mi,(r0)
 nop
 movei #32768,r3
 div r2,r3
 move r5,r0
 abs r5
 mult r3,r5
 shrq #7,r5
 cmpq #0,r0
 jr pl,.positive_x
 nop
 neg r5
.positive_x
 move r6,r0
 abs r6
 mult r3,r6
 shrq #7,r6
 cmpq #0,r0
 jr mi,.negative_y
 nop
 neg r6
.negative_y
 moveq #11,r0
 load (r14+80),r1
 movei #60,r2
 cmp r2,r1
 jr eq,.aspect
 nop
 moveq #12,r0
.aspect
 imult r0,r6
 sharq #4,r6
 movei #184,r0
 add r0,r5
 movei #92,r0
 add r0,r6
 ; Entire sprite clipped; no out-of-bounds writes, never paint over top HUD.
 movei #.done,r0
 cmpq #0,r5
 jump mi,(r0)
 nop
 movei #368,r1
 cmp r1,r5
 jump cc,(r0)
 nop
 movei #50,r1
 cmp r1,r6
 jump mi,(r0)
 nop
 movei #184,r1
 cmp r1,r6
 jump cc,(r0)
 nop
 movei #FX,r15
 load (r15+12),r0
 addq #1,r0
 store r0,(r15+12)
 shlq #10,r20
 movei #effect_atlas,r0
 add r0,r20
 moveq #0,r21
.row
 moveq #0,r22
.pixel
 load (r20),r0
 addq #4,r20
 move r0,r1
 shrq #16,r1
 mult r24,r1
 shrq #8,r1
 ; Stable 4x4 ordered coverage; fade is driven by native lifetime.
 move r21,r2
 moveq #3,r3
 and r3,r2
 shlq #2,r2
 move r22,r3
 moveq #3,r4
 and r4,r3
 xor r3,r2
 shlq #4,r2
 cmp r2,r1
 movei #.skip,r4
 jump cs,(r4)
 nop
 cmpq #0,r1
 movei #.skip,r4
 jump eq,(r4)
 nop
 move r6,r2
 add r21,r2
 movei #1536,r3
 mult r3,r2
 move r5,r3
 add r22,r3
 move r3,r4
 shrq #2,r3
 shlq #4,r3
 add r3,r2
 moveq #3,r3
 and r3,r4
 shlq #1,r4
 add r4,r2
 movefa screen0.a,r3
 add r3,r2
 storew r0,(r2)
 load (r15+16),r0
 addq #1,r0
 store r0,(r15+16)
.skip
 addq #1,r22
 moveq #16,r0
 cmp r0,r22
 movei #.pixel,r0
 jump ne,(r0)
 nop
 addq #1,r21
 moveq #16,r0
 cmp r0,r21
 movei #.row,r0
 jump ne,(r0)
 nop
.done
 movei #FX,r15
 POPLR
 align 8
 ENDMODULE effects
