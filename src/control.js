; Native Jaguar gameplay, using the original Cityscape collision/height data.
; No JavaScript runs on the console. 32-bit positions use 8 fractional bits.
 include <js/macro/joypad1.mac>
 include <js/symbols/joypad.js>
 MODULE control,MODend_irq
 PUSHLR
 JOYPAD1 99
 movei #GAME,r14
 load (r14),r0
 cmpq #0,r0
 movei #reset_game,r1
 jump eq,(r1)
 nop
 movei #LastJoy+4,r0
 load (r0),r20
 btst #JOY_OPTION_BIT,r20
 jump ne,(r1)
 nop
 btst #JOY_PAUSE_BIT,r20
 load (r14+52),r0
 jr eq,.nopause
 nop
 moveq #1,r1
 xor r1,r0
 store r0,(r14+52)
.nopause
 btst #JOY_C_BIT,r20
 load (r14+56),r0
 jr eq,.noreplay
 nop
 moveq #1,r1
 xor r1,r0
 store r0,(r14+56)
.noreplay
 movei #LastJoy,r0
 load (r0),r20
 store r20,(r14+76)
 load (r14+4),r0
 addq #1,r0
 store r0,(r14+4)
 movei #VBL_TICKS,r0
 load (r0),r1
 load (r14+72),r2
 store r1,(r14+72)
 sub r2,r1
 move r1,r19
 cmpq #6,r19
 jr mi,.dtok
 nop
 moveq #6,r19
.dtok
 cmpq #0,r19
 jr ne,.dtset
 nop
 moveq #1,r19
.dtset
 load (r14+52),r0
 cmpq #0,r0
 movei #camera_update,r1
 jump ne,(r1)
 nop
 load (r14+8),r0
 cmpq #1,r0
 jr eq,.race
 nop
 cmpq #0,r0
 jump ne,(r1)
 nop
 btst #JOY_A_BIT,r20
 jr ne,.start
 btst #JOY_UP_BIT,r20
 jump eq,(r1)
 nop
.start
 moveq #1,r0
 store r0,(r14+8)
.race
 load (r14+64),r0
 add r19,r0
 store r0,(r14+64)
 load (r14+56),r0
 cmpq #0,r0
 movei #run_autopilot,r1
 jump ne,(r1)
 nop
 load (r14+16),r21
 load (r14+24),r22
 load (r14+28),r23
 load (r14+32),r24
 ; Turn is 1/512 revolution per video field; B doubles airbrake steering.
 move r19,r1
 shlq #2,r1
 btst #JOY_B_BIT,r20
 jr eq,.turn
 nop
 shlq #1,r1
.turn
 btst #JOY_LEFT_BIT,r20
 jr eq,.right
 nop
 add r1,r23
.right
 btst #JOY_RIGHT_BIT,r20
 jr eq,.turnend
 nop
 sub r1,r23
.turnend
 movei #2044,r0
 and r0,r23
 store r23,(r14+28)
 btst #JOY_A_BIT,r20
 jr ne,.thrust
 btst #JOY_UP_BIT,r20
 jr ne,.thrust
 nop
 sub r19,r24
 jr .speedlimit
 nop
.thrust
 add r19,r24
.speedlimit
 btst #JOY_B_BIT,r20
 jr eq,.minspeed
 btst #JOY_DOWN_BIT,r20
 ; B is airbrake, down also brakes below.
 sub r19,r24
 sub r19,r24
.minspeed
 btst #JOY_DOWN_BIT,r20
 jr eq,.clamp
 nop
 sub r19,r24
.clamp
 cmpq #0,r24
 jr pl,.maxspeed
 nop
 moveq #0,r24
.maxspeed
 moveq #28,r0
 cmp r0,r24
 jr mi,.move
 nop
 moveq #28,r24
.move
 store r24,(r14+32)
 load (r14+48),r0
 cmpq #0,r0
 jr eq,.noboost
 nop
 sub r19,r0
 jr pl,.boostok
 nop
 moveq #0,r0
.boostok
 store r0,(r14+48)
 addq #14,r24
.noboost
 mult r19,r24
 movei #SinTab,r15
 load (r15+r23),r0
 move r0,r1
 shrq #16,r1
 imult r24,r0
 imult r24,r1
 sharq #7,r0
 sharq #7,r1
 sub r0,r21
 add r1,r22
 move r21,r0
 move r22,r1
 movei #sample_map,r2
 BL (r2)
 ; r3=terrain, r4=height. Reject invalid position and drain shield on impact.
 cmpq #0,r3
 movei #valid_move,r0
 jump ne,(r0)
 nop
 load (r14+68),r0
 addq #1,r0
 store r0,(r14+68)
 load (r14+36),r0
 sub r19,r0
 jr pl,.healthok
 nop
 moveq #0,r0
.healthok
 store r0,(r14+36)
 cmpq #0,r0
 jr ne,.bounce
 nop
 moveq #2,r0
 store r0,(r14+8)
.bounce
 moveq #0,r0
 store r0,(r14+32)
 store r0,(r14+48)
 movei #camera_update,r0
 jump (r0)
 nop
valid_move:
 store r21,(r14+16)
 store r22,(r14+24)
 shlq #8,r4
 store r4,(r14+20)
 cmpq #2,r3
 jr ne,.checkpoints
 nop
 movei #90,r0
 store r0,(r14+48)
.checkpoints
 cmpq #3,r3
 movei #camera_update,r2
 jump mi,(r2)
 nop
 subq #3,r3
 load (r14+44),r0
 cmp r3,r0
 jump eq,(r2)
 nop
 ; Only ordered checkpoints 0 -> 1 -> 2 -> 0 advance a lap.
 addq #1,r0
 cmpq #3,r0
 jr ne,.cpcompare
 nop
 moveq #0,r0
.cpcompare
 cmp r0,r3
 jump ne,(r2)
 nop
 store r3,(r14+44)
 cmpq #0,r3
 jump ne,(r2)
 nop
 load (r14+40),r0
 addq #1,r0
 store r0,(r14+40)
 cmpq #4,r0
 jump ne,(r2)
 nop
 moveq #3,r0
 store r0,(r14+8)
 jump (r2)
 nop

reset_game:
 movei #GAME,r14
 movei #$48455847,r0
 store r0,(r14)
 moveq #0,r0
 move r14,r1
 addq #4,r1
 moveq #19,r2
.clear
 store r0,(r1)
 addq #4,r1
 subq #1,r2
 jr ne,.clear
 nop
 movei #-2268*4*256,r0
 store r0,(r14+16)
 movei #387*4*256,r0
 store r0,(r14+20)
 movei #-886*4*256,r0
 store r0,(r14+24)
 movei #100,r0
 store r0,(r14+36)
 moveq #1,r0
 store r0,(r14+40)
 movei #camera_update,r0
 jump (r0)
 nop

run_autopilot:
 ; Optional autopilot: waypoints extracted from the original collision image.
 load (r14+60),r0
 movei #route_count-1,r1
 cmp r1,r0
 jr mi,.rok
 nop
 moveq #0,r0
.rok
 move r0,r1
 shlq #4,r1
 movei #route_data,r15
 add r1,r15
 load (r15),r1
 load (r15+4),r2
 load (r15+8),r3
 load (r15+12),r4
 store r1,(r14+16)
 store r2,(r14+20)
 store r3,(r14+24)
 store r4,(r14+28)
 addq #1,r0
 store r0,(r14+60)
 moveq #28,r0
 store r0,(r14+32)
 load (r14+16),r21
 load (r14+24),r22
 move r21,r0
 move r22,r1
 movei #sample_map,r2
 BL (r2)
 movei #valid_move,r0
 jump (r0)
 nop

camera_update:
 movei #GAME,r14
 load (r14+16),r21
 load (r14+20),r24
 load (r14+24),r22
 load (r14+28),r23
 sharq #8,r21
 sharq #8,r24
 sharq #8,r22
 ; Match engine Y-axis Euler rotation to the camera heading.
 move r23,r18
 neg r18
 movei #2044,r0
 and r0,r18
 movei #obj_ship+2,r0
 storew r21,(r0)
 addq #2,r0
 storew r24,(r0)
 addq #2,r0
 storew r22,(r0)
 addq #6,r0
 storew r18,(r0)
 movei #obj_booster+2,r0
 storew r21,(r0)
 addq #2,r0
 storew r24,(r0)
 addq #2,r0
 storew r22,(r0)
 addq #6,r0
 storew r18,(r0)
 movei #SinTab,r15
 load (r15+r23),r0
 move r0,r1
 shrq #16,r1
 movei #160,r2
 imult r2,r0
 imult r2,r1
 sharq #15,r0
 sharq #15,r1
 add r0,r21
 sub r1,r22
 addq #32,r24
 addq #32,r24
 movei #CAMERA_X,r15
 store r21,(r15)
 store r24,(r15+4)
 store r22,(r15+8)
 store r23,(r15+12)
 ; Strings are read from the DRAM backing copy: GPU-local LOADB is word-wide.
 ; HUD is outside the 3D viewport, so failure checks inspect world pixels too.
 movei #PrintString_YX,r5
 movei #ready_text-MODrun_control+MODstart_control,r0
 load (r14+8),r1
 cmpq #0,r1
 movei #print_status,r2
 jump eq,(r2)
 nop
 movei #race_text-MODrun_control+MODstart_control,r0
 cmpq #1,r1
 movei #print_status,r2
 jump eq,(r2)
 nop
 movei #dead_text-MODrun_control+MODstart_control,r0
 cmpq #2,r1
 movei #print_status,r2
 jump eq,(r2)
 nop
 movei #finish_text-MODrun_control+MODstart_control,r0
print_status:
 movei #1<<16,r1
 BL (r5)
 movei #GAME,r14
 load (r14+32),r0
 moveq #10,r1
 mult r1,r0
 movei #1<<16|12,r1
 movei #PrintDEC_YX,r2
 BL (r2)
 movei #GAME,r14
 load (r14+36),r0
 movei #1<<16|24,r1
 movei #PrintDEC_YX,r2
 BL (r2)
 movei #GAME,r14
 load (r14+40),r0
 movei #1<<16|37,r1
 movei #PrintDEC2_YX,r2
 BL (r2)
 POPLR

; Q24.8 world x,z -> 512-square maps spanning [-3000,+3000] original units.
; r0/r1 input, r2 pixel index, r3 terrain, r4 native quarter-unit height.
sample_map:
 sharq #8,r0
 sharq #8,r1
 movei #12000,r2
 add r2,r0
 add r2,r1
 movei #24000,r2
 movei #outside_map,r3
 cmp r2,r0
 jump cc,(r3)
 nop
 cmp r2,r1
 jump cc,(r3)
 nop
 shlq #9,r0
 shlq #9,r1
 div r2,r0
 div r2,r1
 shlq #9,r1
 add r1,r0
 move r0,r2
 movei #collision_map,r1
 add r0,r1
 loadb (r1),r3
 shlq #1,r0
 movei #height_map,r1
 add r0,r1
 loadw (r1),r4
 jump (LR)
 nop
outside_map:
 moveq #0,r3
 jump (LR)
 moveq #0,r4

 align 4
ready_text: dc.b "READY   SPD        SHIELD        LAP      ",0
race_text: dc.b "RACING  SPD        SHIELD        LAP      ",0
dead_text: dc.b "WRECKED SPD        SHIELD        LAP      ",0
finish_text: dc.b "FINISH  SPD        SHIELD        LAP      ",0
 align 8
 ENDMODULE control
