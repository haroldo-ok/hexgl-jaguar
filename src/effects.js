; Bounded world-space ShipEffects adaptation. Original sprite art, real emitters.
; Source: Thibaut BKcore Despoulain, ShipEffects.js, CC BY-NC 3.0. See NOTICE.md.
; 16 particles, 8 words each: x/y/z Q8, vx/vy/vz Q8 per 60Hz field, lifeQ8,type.
 MODULE effects,MODend_irq
 IFD FX_SELFTEST
 PUSHLR
 movei #fx_selftest,r0
 BL (r0)
 POPLR
 ENDIF
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
 movei #fx_inherit,r0
 BL (r0)
 movei #GAME,r14
 movei #FX,r15
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
 movei #FX_AUX+16,r2
 load (r2),r2
 add r2,r1
 store r1,(r26)
 shrq #9,r0
 move r0,r1
 movei #255,r2
 and r2,r1
 move r16,r26
 addq #16,r26
 movei #FX_AUX+20,r2
 load (r2),r2
 add r2,r1
 store r1,(r26)
 shrq #8,r0
 movei #511,r2
 and r2,r0
 movei #256,r2
 sub r2,r0
 move r16,r26
 addq #20,r26
 movei #FX_AUX+24,r2
 load (r2),r2
 add r2,r0
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
 movei #FX_AUX+92,r1
 store r0,(r1)
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
 movei #FX_AUX,r0
 moveq #0,r1
 movei #128,r2
.auxclear
 store r1,(r0)
 addq #4,r0
 subq #1,r2
 jr ne,.auxclear
 nop
 movei #GAME,r14
 movei #FX_AUX,r15
 load (r14+16),r0
 store r0,(r15+4)
 load (r14+20),r0
 store r0,(r15+8)
 load (r14+24),r0
 store r0,(r15+12)
 movei #fx_done,r0
 jump (r0)
 nop

fx_inherit:
 ; Source ShipEffects currentVelocity * .7, per reference 60Hz field.
 movei #GAME+16,r16
 movei #FX_AUX,r15
 moveq #4,r17
.inherit_axis
 load (r16),r0
 load (r15+r17),r1
 store r0,(r15+r17)
 sub r1,r0
 move r0,r2
 abs r0
 shlq #8,r0
 movei #FX+56,r1
 load (r1),r1
 div r1,r0
 movei #32767,r1
 cmp r1,r0
 jr cs,.bounded_velocity
 nop
 move r1,r0
.bounded_velocity
 movei #179,r1
 mult r1,r0
 shrq #8,r0
 cmpq #0,r2
 jr pl,.velocity_sign
 nop
 neg r0
.velocity_sign
 move r17,r1
 addq #12,r1
 store r0,(r15+r1)
 addq #4,r16
 addq #4,r17
 moveq #16,r0
 cmp r0,r17
 movei #.inherit_axis,r0
 jump ne,(r0)
 nop
 jump (LR)
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
 movei #FX_AUX+28,r0
 store r2,(r0)
 movei #32768,r3
 div r2,r3
 ; Source world sizes: spark 2*4, cloud 6*4. Glow has bounded native scale.
 moveq #8,r25
 cmpq #1,r20
 jr ne,.notcloud
 nop
 moveq #24,r25
.notcloud
 cmpq #2,r20
 jr ne,.worldsize
 nop
 moveq #16,r25
.worldsize
 mult r3,r25
 shrq #7,r25
 cmpq #2,r25
 jr pl,.sizemin
 nop
 moveq #2,r25
.sizemin
 movei #32,r0
 cmp r0,r25
 jr mi,.sizemax
 nop
 move r0,r25
.sizemax
 movei #FX_AUX+32,r0
 store r25,(r0)
 movei #FX_AUX+36,r0
 store r24,(r0)
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
 movei #192,r0
 add r0,r5
 movei #100,r0
 add r0,r6
 ; Store center; query real submitted geometry before touching sprite pixels.
 movei #FX_AUX,r15
 store r5,(r15+48)
 store r6,(r15+52)
 store r20,(r15+96)
 cmpq #2,r20 ; source boosterSprite mergeWith3D=false; leave glow unoccluded
 movei #.depth_done,r0
 jump eq,(r0)
 nop
 move r5,r0
 move r6,r1
 load (r15+28),r2
 movei #fx_occluded,r8
 BL (r8)
 cmpq #0,r0
 movei #.done,r1
 jump ne,(r1)
 nop
 movei #FX_AUX,r15
 load (r15+48),r5
 load (r15+52),r6
.depth_done
 move r25,r0
 shrq #1,r0
 sub r0,r5
 sub r0,r6
 movei #.done,r0
 move r5,r1
 add r25,r1
 cmpq #0,r1
 jump mi,(r0)
 nop
 movei #384,r1
 cmp r1,r5
 jump cc,(r0)
 nop
 move r6,r1
 add r25,r1
 movei #50,r2
 cmp r2,r1
 jump mi,(r0)
 nop
 movei #200,r1
 cmp r1,r6
 jump cc,(r0)
 nop
 movei #FX,r15
 load (r15+12),r0
 addq #1,r0
 store r0,(r15+12)
 moveq #0,r21
.row
 moveq #0,r22
.pixel
 ; Clip each output texel, so sprites can straddle the viewport edges safely.
 move r5,r23
 add r22,r23
 movei #.skip,r26
 cmpq #0,r23
 jump mi,(r26)
 nop
 movei #384,r0
 cmp r0,r23
 jump cc,(r26)
 nop
 move r6,r0
 add r21,r0
 movei #50,r1
 cmp r1,r0
 jump mi,(r26)
 nop
 movei #200,r1
 cmp r1,r0
 jump cc,(r26)
 nop
 movei #1536,r1
 mult r1,r0
 move r23,r1
 shrq #2,r1
 shlq #4,r1
 add r1,r0
 moveq #3,r1
 and r1,r23
 shlq #1,r23
 add r23,r0
 movefa screen0.a,r1
 add r1,r0
 move r0,r23 ; destination address survives blend_rgb
 move r21,r0
 shlq #4,r0
 div r25,r0
 shlq #4,r0
 move r22,r1
 shlq #4,r1
 div r25,r1
 add r1,r0
 shlq #2,r0
 move r20,r1
 shlq #10,r1
 add r1,r0
 movei #effect_atlas,r1
 add r1,r0
 load (r0),r0
 move r0,r2
 shrq #16,r2
 mult r24,r2
 shrq #8,r2
 cmpq #0,r2
 jump eq,(r26)
 nop
 ; Source cloud opacity is .8; sparks and glow use additive composition.
 moveq #1,r3
 cmpq #1,r20
 jr ne,.compose
 nop
 moveq #0,r3
 movei #204,r1
 mult r1,r2
 shrq #8,r2
.compose
 loadw (r23),r1
 movei #FX_AUX,r15
 store r5,(r15+40)
 store r6,(r15+44)
 movei #32,r7
 cmp r7,r2
 movei #.compose_call,r4
 jump cs,(r4)
 nop
 load (r15+60),r4
 addq #1,r4
 store r4,(r15+60)
 store r25,(r15+100)
 store r24,(r15+104)
 store r20,(r15+108)
 load (r15+28),r4
 store r4,(r15+56)
 store r0,(r15+64)
 store r1,(r15+68)
 store r2,(r15+72)
 store r3,(r15+76)
 store r23,(r15+84)
 store r5,(r15+112)
 store r6,(r15+116)
 store r22,(r15+120)
 store r21,(r15+124)
.compose_call
 movei #blend_rgb,r8
 BL (r8)
 storew r0,(r23)
 load (r15+60),r4
 btst #0,r4
 jr eq,.compose_restored
 nop
 store r0,(r15+80)
 addq #1,r4
 store r4,(r15+60)
.compose_restored
 load (r15+40),r5
 load (r15+44),r6
 movei #FX,r15
 load (r15+16),r0
 addq #1,r0
 store r0,(r15+16)
.skip
 addq #1,r22
 cmp r25,r22
 movei #.pixel,r0
 jump ne,(r0)
 nop
 addq #1,r21
 cmp r25,r21
 movei #.row,r0
 jump ne,(r0)
 nop
.done
 movei #FX,r15
 POPLR
 include "blend.inc"
 include "fx_depth.inc"
 IFD FX_SELFTEST
 include "../tests/fx_probe.inc"
 ENDIF
 align 8
 ENDMODULE effects
