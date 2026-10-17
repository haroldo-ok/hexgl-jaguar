; Native race-flow presentation derived from BKcore HexGL Gameplay.js.
; Gameplay.js by Thibaut Despoulain: CC BY-NC 3.0; see NOTICE.md.
; Bitmap gauges are drawn separately by bitmap_hud.js. Times are MM:SS.mmm at video-field precision.
; All strings below are read through their DRAM backing address.

MACRO HUDSTRING
 movei #\0-MODrun_pose+MODstart_pose,r0
 movei #\1,r1
 movei #hud_printstring,r2
 BL (r2)
ENDM

draw_race_hud:
 PUSHLR
 HUDSTRING status_line,1<<16
 movei #GAME,r14
 load (r14+32),r0
 moveq #10,r1
 mult r1,r0
 movei #1<<16|12,r1
 movei #print_three,r2
 BL (r2)
 movei #GAME,r14
 load (r14+36),r0
 movei #1<<16|24,r1
 movei #print_three,r2
 BL (r2)
 movei #GAME,r14
 load (r14+40),r0
 cmpq #4,r0
 jr ne,.lapok
 nop
 moveq #3,r0
.lapok
 movei #1<<16|34,r1
 movei #hud_printdec2,r2
 BL (r2)
 HUDSTRING time_line,2<<16
 movei #GAME,r14
 load (r14+64),r0
 movei #2<<16|5,r1
 movei #print_time,r2
 BL (r2)
 movei #GAME,r14
 load (r14+64),r0
 load (r14+84),r2
 sub r2,r0
 load (r14+8),r2
 cmpq #5,r2
 jr ne,.notreplayresult
 nop
 movei #REPLAY+64,r2
 load (r2),r2
.notreplayresult
 cmpq #3,r2
 jr ne,.currentlap
 nop
 load (r14+96),r0
.currentlap
 movei #2<<16|19,r1
 movei #print_time,r2
 BL (r2)
 movei #GAME,r14
 load (r14+100),r0
 movei #2<<16|34,r1
 movei #print_time,r2
 BL (r2)
 HUDSTRING laps_line,3<<16
 movei #GAME,r14
 load (r14+88),r0
 movei #3<<16|3,r1
 movei #print_time,r2
 BL (r2)
 movei #GAME,r14
 load (r14+92),r0
 movei #3<<16|18,r1
 movei #print_time,r2
 BL (r2)
 movei #GAME,r14
 load (r14+96),r0
 movei #3<<16|33,r1
 movei #print_time,r2
 BL (r2)
 ; Select status and message independently of numerical telemetry.
 movei #GAME,r14
 movei #ready_word-MODrun_pose+MODstart_pose,r21
 movei #help_text-MODrun_pose+MODstart_pose,r22
 load (r14+8),r0
 cmpq #0,r0
 movei #hud_status,r2
 jump eq,(r2)
 nop
 cmpq #4,r0
 movei #hud_countdown,r1
 jump eq,(r1)
 nop
 movei #replay_word-MODrun_pose+MODstart_pose,r21
 movei #replay_message-MODrun_pose+MODstart_pose,r22
 cmpq #5,r0
 jump eq,(r2)
 nop
 movei #dead_word-MODrun_pose+MODstart_pose,r21
 movei #dead_message-MODrun_pose+MODstart_pose,r22
 cmpq #2,r0
 jump eq,(r2)
 nop
 movei #finish_word-MODrun_pose+MODstart_pose,r21
 movei #finish_message-MODrun_pose+MODstart_pose,r22
 cmpq #3,r0
 jump eq,(r2)
 nop
 movei #race_word-MODrun_pose+MODstart_pose,r21
 movei #help_text-MODrun_pose+MODstart_pose,r22
 load (r14+40),r0
 cmpq #3,r0
 jr ne,.notfinal
 nop
 movei #final_message-MODrun_pose+MODstart_pose,r22
.notfinal
 load (r14+64),r0
 load (r14+80),r1
 shrq #1,r1
 cmp r1,r0
 jump cc,(r2)
 nop
 movei #go_message-MODrun_pose+MODstart_pose,r22
 jump (r2)
 nop
hud_countdown:
 movei #count_word-MODrun_pose+MODstart_pose,r21
 movei #ready_message-MODrun_pose+MODstart_pose,r22
 load (r14+12),r0
 load (r14+80),r1
 move r1,r3
 shrq #1,r3
 shlq #1,r1
 add r3,r1 ; 2.5 seconds
 cmp r1,r0
 jump mi,(r2)
 nop
 movei #three_message-MODrun_pose+MODstart_pose,r22
 load (r14+80),r1
 shlq #2,r1 ; 4 seconds
 cmp r1,r0
 jump mi,(r2)
 nop
 movei #two_message-MODrun_pose+MODstart_pose,r22
 load (r14+80),r1
 moveq #5,r4
 mult r4,r1
 add r3,r1 ; 5.5 seconds
 cmp r1,r0
 jump mi,(r2)
 nop
 movei #one_message-MODrun_pose+MODstart_pose,r22
hud_status:
 load (r14+52),r0
 cmpq #0,r0
 jr eq,.notpaused
 nop
 movei #pause_word-MODrun_pose+MODstart_pose,r21
 movei #pause_message-MODrun_pose+MODstart_pose,r22
.notpaused
 store r22,(r14+104)
 store r21,(r14+108)
 move r21,r0
 movei #1<<16,r1
 movei #hud_printstring,r2
 BL (r2)
 move r22,r0
 moveq #0,r1
 movei #hud_printstring,r2
 BL (r2)
 POPLR

 ; Suppress writes before the text object is scanned, not only at end-of-frame.
 ; Keep time/status backing strings live even with the HUD disabled.
hud_printstring:
 movei #PrintString_YX,r3
 jr hud_printgate
 nop
hud_printdec2:
 movei #PrintDEC2_YX,r3
hud_printgate:
 movei #SETTINGS+4,r4
 load (r4),r4
 cmpq #0,r4
 jump ne,(r3)
 nop
 movei #GAME+8,r4
 load (r4),r4
 cmpq #1,r4
 jr eq,.hidden
 nop
 cmpq #4,r4
 jr eq,.hidden
 nop
 cmpq #5,r4
 jump ne,(r3)
 nop
.hidden
 jump (LR)
 nop

; r0 unsigned field count, r1 y:x. Formatter scratch is DRAM, not GPU local RAM.
print_time:
 PUSHLR r20,r21,r22,r23,r24
 move r1,r24
 movei #GAME+80,r2
 load (r2),r2
 move r0,r20
 div r2,r0
 move r0,r21 ; total seconds
 mult r0,r2
 sub r2,r20
 movei #1000,r2
 mult r2,r20
 movei #GAME+80,r2
 load (r2),r2
 div r2,r20 ; fractional milliseconds, truncated
 movei #60,r2
 div r2,r0
 move r0,r22 ; minutes
 mult r0,r2
 sub r2,r21 ; seconds
 movei #100,r2
 div r2,r0
 mult r0,r2
 sub r2,r22 ; minutes modulo 100, fixed-width display
 ; Keep each formatted time at a distinct observable DRAM address.
 move r24,r23
 shrq #16,r23
 subq #2,r23
 shlq #6,r23
 move r24,r1
 shlq #16,r1
 shrq #16,r1
 add r1,r23
 movei #$1200,r1
 add r1,r23
 PUSH r23
 move r22,r0
 movei #emit_two,r3
 BL (r3)
 movei #58,r0
 storeb r0,(r23)
 addq #1,r23
 move r21,r0
 movei #emit_two,r3
 BL (r3)
 movei #46,r0
 storeb r0,(r23)
 addq #1,r23
 move r20,r0
 movei #emit_three,r3
 BL (r3)
 moveq #0,r0
 storeb r0,(r23)
 POP r0
 move r24,r1
 movei #hud_printstring,r2
 BL (r2)
 POPLR r20,r21,r22,r23,r24

print_three:
 PUSHLR r23,r24
 move r1,r24
 movei #$1200,r23
 movei #emit_three,r3
 BL (r3)
 moveq #0,r0
 storeb r0,(r23)
 movei #$1200,r0
 move r24,r1
 movei #hud_printstring,r2
 BL (r2)
 POPLR r23,r24

emit_three:
 movei #100,r1
 move r0,r2
 div r1,r0
 mult r0,r1
 sub r1,r2
 addq #24,r0
 addq #24,r0
 storeb r0,(r23)
 addq #1,r23
 move r2,r0
emit_two:
 moveq #10,r1
 move r0,r2
 div r1,r0
 mult r0,r1
 sub r1,r2
 addq #24,r0
 addq #24,r0
 storeb r0,(r23)
 addq #1,r23
 addq #24,r2
 addq #24,r2
 storeb r2,(r23)
 jump (LR)
 addq #1,r23

 align 4
status_line: dc.b "        SPD      SHIELD       LAP   /3         ",0
time_line: dc.b   "TIME           LAP           BEST              ",0
laps_line: dc.b   "1:             2:             3:               ",0
ready_word: dc.b "READY   ",0
race_word: dc.b "RACING  ",0
count_word: dc.b "START   ",0
dead_word: dc.b "WRECKED ",0
finish_word: dc.b "FINISH  ",0
pause_word: dc.b "PAUSED  ",0
help_text: dc.b "A THRUST B BRAKE C AUTO / OPTION RESTART         ",0
ready_message: dc.b "GET READY                                      ",0
three_message: dc.b "3                                              ",0
two_message: dc.b "2                                              ",0
one_message: dc.b "1                                              ",0
go_message: dc.b "GO                                             ",0
final_message: dc.b "FINAL LAP                                      ",0
dead_message: dc.b "DESTROYED - OPTION TO RESTART                   ",0
finish_message: dc.b "FINISH - LAP SPLITS ABOVE - OPTION TO RESTART   ",0
pause_message: dc.b "PAUSED - PRESS PAUSE TO RESUME                  ",0

replay_word: dc.b "REPLAY  ",0
replay_message: dc.b "REPLAY - PAUSE PLAYBACK / OPTION MAIN MENU     ",0
