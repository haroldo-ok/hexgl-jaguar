; Native adaptation of BKcore ShipControls roll and CameraChase speed offset.
; Upstream source is CC BY-NC 3.0; see NOTICE.md. Full quaternion/physics parity
; is NOT implemented. Camera height filtering is an explicit native adaptation.
;
; MOTION words: roll Q8, pullback Q8, camera Y Q8, last heading, roll target Q8,
; pullback target Q8, height target Q8, dt fields, alpha bank/pull/height,
; effective distance, camera X/Y/Z, applied ship/booster roll (packed words),
; committed pose sequence. Sequence increments only after all outputs are set.

motion_reset:
 movei #MOTION,r15
 moveq #0,r0
 move r15,r1
 moveq #17,r2
.clear
 store r0,(r1)
 addq #4,r1
 subq #1,r2
 jr ne,.clear
 nop
 load (r14+20),r0
 movei #64*256,r1
 add r1,r0
 store r0,(r15+8)
 store r0,(r15+24)
 jump (LR)
 nop

motion_update:
 PUSHLR
 movei #GAME,r14
 load (r14+8),r0
 cmpq #1,r0
 movei #motion_done,r1
 jump ne,(r1)
 nop
 load (r14+52),r0
 cmpq #0,r0
 jump ne,(r1)
 nop
 ; Choose response coefficients by actual video mode and capped elapsed fields.
 move r19,r0
 subq #1,r0
 moveq #12,r1
 mult r1,r0
 load (r14+80),r1
 movei #60,r2
 cmp r2,r1
 jr eq,.ntsc
 nop
 addq #24,r0
 addq #24,r0
 addq #24,r0
.ntsc
 movei #motion_coefficients-MODrun_pose+MODstart_pose,r15
 add r0,r15
 load (r15),r8
 load (r15+4),r9
 load (r15+8),r10
 movei #MOTION,r15
 store r19,(r15+28)
 store r8,(r15+32)
 store r9,(r15+36)
 store r10,(r15+40)
 ; Left/right roll matches the upstream visual mesh roll sign.
 moveq #0,r0
 load (r14+76),r20
 movei #196,r1 ; .6 rad, quantized to 49 of 512 angular steps
 btst #JOY_B_BIT,r20
 jr eq,.rollamount
 nop
 movei #332,r1 ; .6 * 1.7 rad airbrake bank, quantized to 83 steps
.rollamount
 btst #JOY_LEFT_BIT,r20
 jr eq,.rightbank
 nop
 sub r1,r0
.rightbank
 btst #JOY_RIGHT_BIT,r20
 jr eq,.banktarget
 nop
 add r1,r0
.banktarget
 load (r14+28),r12
 load (r15+12),r13
 store r12,(r15+12)
 load (r14+56),r1
 cmpq #0,r1
 movei #.manualbank,r3
 jump eq,(r3)
 nop
 ; Autopilot is a native feature: bank from shortest wrapped heading change.
 sub r13,r12
 movei #1024,r1
 add r1,r12
 movei #2047,r2
 and r2,r12
 sub r1,r12
 neg r12
 shlq #4,r12
 move r12,r0
 abs r0
 div r19,r0
 movei #196,r1
 cmp r1,r0
 jr mi,.autoclamp
 nop
 move r1,r0
.autoclamp
 cmpq #0,r12
 jr pl,.manualbank
 nop
 neg r0
.manualbank
 shlq #8,r0
 store r0,(r15+16)
 load (r15),r1
 move r8,r2
 movei #smooth_component,r3
 BL (r3)
 store r0,(r15)
 ; CameraChase speedOffsetMax=10 original units -> 40 native world units.
 load (r14+32),r0
 movei #40*256,r1
 mult r1,r0
 moveq #28,r1
 div r1,r0
 store r0,(r15+20)
 load (r15+4),r1
 move r9,r2
 movei #smooth_component,r3
 BL (r3)
 store r0,(r15+4)
 ; Follow height smoothly, but never allow the camera to sink into the road.
 load (r14+20),r0
 movei #64*256,r1
 add r1,r0
 store r0,(r15+24)
 load (r15+8),r1
 move r10,r2
 movei #smooth_component,r3
 BL (r3)
 load (r14+20),r1
 movei #24*256,r2
 add r2,r1
 cmp r1,r0
 jr pl,.heightabove
 nop
 move r1,r0
.heightabove
 movei #56*256,r2
 add r2,r1 ; upper bound: ship Y + 80
 cmp r1,r0
 jr mi,.heightbounded
 nop
 move r1,r0
.heightbounded
 store r0,(r15+8)
motion_done:
 POPLR

; r0 target Q8, r1 old Q8, r2 alpha Q8 -> r0 new Q8, clobbers r3..r5.
; Split the delta before Jaguar's 16-bit multiply; direct IMULT of Q8 bank
; or height deltas would overflow/truncate. Round, then take a one-LSB step
; if necessary so no positive residual can stick forever.
smooth_component:
 sub r1,r0
 move r0,r4
 move r0,r3
 sharq #8,r0
 imult r2,r0
 shlq #24,r3
 shrq #24,r3
 mult r2,r3
 movei #128,r5
 add r5,r3
 shrq #8,r3
 add r3,r0
 cmpq #0,r0
 jr ne,.smoothdone
 nop
 cmpq #0,r4
 jr eq,.smoothdone
 nop
 moveq #1,r0
 cmpq #0,r4
 jr pl,.smoothdone
 nop
 neg r0
.smoothdone
 add r1,r0
 jump (LR)
 nop

 include "../assets/motion.inc"
