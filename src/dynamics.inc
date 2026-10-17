; Native drift, contact impulses, hover, grade and falling.
; Adapted from ShipControls.js (CC BY-NC 3.0), not its full quaternion solver.
; PHYS: magic, driftQ8, repelXQ8, repelZQ8, falling, fallFields, pitchQ8,
; pitchTargetQ8, heightTargetQ8, contacts, dt, commit, cameraPitchQ8,
; cameraTargetQ8, alphaDrift/Repel/Height/Pitch, proposedX/Z, oldY, dy,
; deltaX/Z, last phase. No test writes to these addresses.
physics_reset:
 movei #PHYS,r15
 move r15,r0
 moveq #0,r1
 moveq #25,r2
.clear
 store r1,(r0)
 addq #4,r0
 subq #1,r2
 jr ne,.clear
 nop
 movei #$50485953,r0
 store r0,(r15)
 jump (LR)
 nop

physics_begin:
 movei #PHYS,r15
 store r19,(r15+40)
 move r19,r0
 subq #1,r0
 shlq #4,r0
 load (r14+80),r1
 movei #60,r2
 cmp r2,r1
 jr eq,.ntsc
 nop
 movei #96,r1
 add r1,r0
.ntsc
 movei #dynamics_coefficients-MODrun_control+MODstart_control,r1
 add r0,r1
 load (r1),r2
 store r2,(r15+56)
 addq #4,r1
 load (r1),r2
 store r2,(r15+60)
 addq #4,r1
 load (r1),r2
 store r2,(r15+64)
 addq #4,r1
 load (r1),r2
 store r2,(r15+68)
 moveq #0,r0
 store r0,(r15+36)
 load (r15+4),r1
 btst #JOY_B_BIT,r20
 jr eq,.target
 nop
 moveq #26,r2
 btst #JOY_LEFT_BIT,r20
 jr eq,.right
 nop
 sub r2,r0
.right
 btst #JOY_RIGHT_BIT,r20
 jr eq,.target
 nop
 add r2,r0
.target
 sub r1,r0
 move r0,r3
 load (r15+56),r2
 imult r2,r0
 sharq #8,r0
 cmpq #0,r0
 jr ne,.driftstep
 nop
 cmpq #0,r3
 jr eq,.driftstep
 nop
 moveq #1,r0
 cmpq #0,r3
 jr pl,.driftstep
 nop
 neg r0
.driftstep
 add r1,r0
 store r0,(r15+4)
 ; Decaying contact velocity, applied to subsequent attempted motion.
 load (r15+8),r0
 load (r15+60),r2
 move r0,r1
 imult r2,r1
 sharq #8,r1
 sub r1,r0
 store r0,(r15+8)
 load (r15+12),r0
 move r0,r1
 imult r2,r1
 sharq #8,r1
 sub r1,r0
 store r0,(r15+12)
 jump (LR)
 nop

physics_lateral:
 ; r24 is speed * dt. Forward movement has already been applied to r21/r22.
 movei #PHYS,r15
 load (r15+4),r2
 imult r24,r2
 movei #SinTab,r15
 load (r15+r23),r0
 move r0,r1
 shrq #16,r1
 imult r2,r0
 imult r2,r1
 sharq #15,r0
 sharq #15,r1
 add r1,r21
 add r0,r22
 movei #PHYS,r15
 load (r15+8),r0
 load (r15+12),r1
 imult r19,r0
 imult r19,r1
 add r0,r21
 add r1,r22
 store r21,(r15+72)
 store r22,(r15+76)
 jump (LR)
 nop

physics_contact:
 ; Roll back penetration, but retain a damped impulse away from the contact.
 ; The original collision map selects the inward gradient; absent neighbours
 ; signal an unsupported fall rather than indefinitely clamping to the road.
 movei #PHYS,r15
 moveq #0,r6
 moveq #0,r7
 movei #collision_map,r0
 add r2,r0
 moveq #0,r8
 moveq #0,r9
 movei #513,r1
 cmp r1,r2
 movei #.fallback,r3
 jump cs,(r3)
 nop
 movei #261630,r1
 cmp r1,r2
 movei #.fallback,r3
 jump cc,(r3)
 nop
 subq #1,r0
 loadb (r0),r1
 cmpq #0,r1
 jr eq,.leftclear
 nop
 subq #1,r6
 addq #1,r8
.leftclear
 addq #2,r0
 loadb (r0),r1
 cmpq #0,r1
 jr eq,.rightclear
 nop
 addq #1,r6
 addq #1,r8
.rightclear
 subq #1,r0
 movei #512,r1
 sub r1,r0
 loadb (r0),r1
 cmpq #0,r1
 jr eq,.backclear
 nop
 subq #1,r7
 addq #1,r8
.backclear
 movei #1024,r1
 add r1,r0
 loadb (r0),r1
 cmpq #0,r1
 jr eq,.frontclear
 nop
 addq #1,r7
 addq #1,r8
.frontclear
 cmpq #0,r8
 jr ne,.gradient
 nop
.fallback
 ; No neighbouring supporting surface: native fall, 1.5 seconds active time.
 moveq #1,r0
 store r0,(r15+16)
 store r21,(r14+16)
 store r22,(r14+24)
.gradient
 move r6,r0
 or r7,r0
 cmpq #0,r0
 jr ne,.normal
 nop
 load (r14+16),r6
 load (r14+24),r7
 sub r21,r6
 sub r22,r7
 sharq #4,r6
 sharq #4,r7
 jr .impulse
 nop
.normal
 movei #1536,r0 ; 6 native units / video field, bounded diagonal impulse.
 imult r0,r6
 imult r0,r7
.impulse
 store r6,(r15+8)
 store r7,(r15+12)
 movei #SinTab,r0
 add r23,r0
 load (r0),r0
 move r0,r1
 shrq #16,r1
 imultn r1,r6
 imacn r0,r7
 resmac r1
 moveq #4,r0
 cmpq #0,r1
 jr eq,.contactside
 nop
 moveq #1,r0
 cmpq #0,r1
 jr pl,.contactside
 nop
 moveq #2,r0
.contactside
 store r0,(r15+36)
 jump (LR)
 nop

physics_fall:
 movei #PHYS,r15
 load (r15+20),r0
 add r18,r0
 store r0,(r15+20)
 load (r14+80),r1
 move r1,r2
 shrq #1,r2
 add r2,r1
 cmp r1,r0
 jr cs,.drop
 nop
 moveq #2,r0
 store r0,(r14+8)
 moveq #0,r0
 store r0,(r14+36)
.drop
 ; Keep BOTH 16-bit multiply operands bounded even at dt=6.
 movei #80*60,r0
 mult r19,r0
 shlq #8,r0
 load (r14+80),r1
 div r1,r0
 load (r14+20),r1
 sub r0,r1
 store r1,(r14+20)
 moveq #0,r0
 store r0,(r14+32)
 store r0,(r14+48)
 jump (LR)
 nop

physics_hover:
 PUSHLR
 ; Bilinear surface height; discard invalid neighbours at track boundaries.
 move r21,r0
 move r22,r1
 movei #height_bilinear,r2
 BL (r2)
 movei #PHYS,r15
 store r0,(r15+32)
 load (r14+20),r1
 store r1,(r15+80)
 sub r1,r0
 store r0,(r15+84)
 cmpq #0,r0
 jr pl,.heightup
 nop
 load (r15+64),r2
 movei #physics_scale,r3
 BL (r3)
.heightup
 add r1,r0
 store r0,(r14+20)
 ; Ahead surface probe derives real pitch, rather than banking-only geometry.
 movei #SinTab,r15
 load (r14+28),r23
 load (r15+r23),r0
 move r0,r1
 shrq #16,r1
 movei #96,r2
 imult r2,r0
 imult r2,r1
 sharq #7,r0
 sharq #7,r1
 neg r0
 add r21,r0
 add r22,r1
 movei #sample_map,r2
 BL (r2)
 cmpq #0,r3
 movei #.noprobe,r0
 jump eq,(r0)
 nop
 movei #PHYS,r15
 load (r15+32),r0
 shrq #8,r0
 sub r0,r4
 move r4,r0
 movei #96,r1
 movei #physics_atan,r2
 BL (r2)
 neg r0
 movei #PHYS,r15
 store r0,(r15+28)
.noprobe
 movei #PHYS,r15
 load (r15+28),r0
 load (r15+24),r1
 sub r1,r0
 load (r15+68),r2
 movei #physics_scale,r3
 BL (r3)
 add r1,r0
 store r0,(r15+24)
 POPLR

; r0 signed Q8 delta * r2 Q8, exact split 16-bit IMULT. r1 retained.
physics_scale:
 move r0,r3
 sharq #8,r0
 imult r2,r0
 movei #255,r4
 and r4,r3
 mult r2,r3
 shrq #8,r3
 add r3,r0
 jump (LR)
 nop

; Signed rise r0 / run r1 -> Q8 angle-index, bounded +/-atan(.5).
physics_atan:
 move r0,r5
 abs r0
 shlq #8,r0
 div r1,r0
 movei #128,r1
 cmp r1,r0
 jr cs,.bounded
 nop
 move r1,r0
.bounded
 shlq #2,r0
 movei #atan_slope-MODrun_control+MODstart_control,r1
 add r0,r1
 load (r1),r0
 cmpq #0,r5
 jr pl,.done
 nop
 neg r0
.done
 jump (LR)
 nop

height_bilinear:
 PUSHLR
 movei #12000,r2
 sharq #8,r0
 sharq #8,r1
 add r2,r0
 add r2,r1
 shlq #17,r0
 shlq #17,r1
 movei #24000,r2
 div r2,r0
 div r2,r1
 movei #255,r2
 move r0,r6
 move r1,r7
 and r2,r6
 and r2,r7
 shrq #8,r0
 shrq #8,r1
 ; A valid center can occupy the final column/row: clamp neighbour there.
 movei #510,r2
 cmp r2,r0
 jr cs,.xok
 nop
 move r2,r0
.xok
 cmp r2,r1
 jr cs,.zok
 nop
 move r2,r1
.zok
 shlq #9,r1
 add r1,r0
 shlq #1,r0
 movei #height_map,r1
 add r0,r1
 loadw (r1),r8
 addq #2,r1
 loadw (r1),r9
 movei #1022,r0
 add r0,r1
 loadw (r1),r10
 addq #2,r1
 loadw (r1),r11
 movei #65535,r0
 cmp r0,r9
 jr ne,.bvalid
 nop
 move r8,r9
.bvalid
 cmp r0,r10
 jr ne,.cvalid
 nop
 move r8,r10
.cvalid
 cmp r0,r11
 jr ne,.dvalid
 nop
 move r8,r11
.dvalid
 sub r8,r9
 imult r6,r9
 shlq #8,r8
 add r9,r8
 sub r10,r11
 imult r6,r11
 shlq #8,r10
 add r11,r10
 move r10,r0
 sub r8,r0
 move r7,r2
 movei #physics_scale,r3
 BL (r3)
 add r8,r0
 POPLR

 include "../assets/dynamics.inc"
