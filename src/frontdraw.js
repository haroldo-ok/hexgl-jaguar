; Original title/background and rasterized source Bebas Neue typography.
 MODULE frontdraw,MODend_irq
 PUSHLR
 movei #GAME+8,r0
 load (r0),r0
 cmpq #0,r0
 movei #frontdraw_menu,r1
 jump eq,(r1)
 nop
 cmpq #2,r0
 movei #frontdraw_result,r1
 jump eq,(r1)
 nop
 cmpq #3,r0
 jump eq,(r1)
 nop
 cmpq #5,r0
 movei #frontdraw_replay,r1
 jump eq,(r1)
 nop
 POPLR

MACRO FRONT_TEXT
 movei #\0-MODrun_frontdraw+MODstart_frontdraw,r0
 movei #\1,r1
 movei #\2,r2
 movei #FRONT_BLUE,r3
 movei #front_text,r8
 BL (r8)
ENDM

frontdraw_menu:
 movei #FRONT+8,r0
 load (r0),r0
 movei #$992000,r1
 cmpq #0,r0
 jr eq,.background
 nop
 movei #$9b7800,r1
.background
 movei #BLIT_A1_BASE,r14
.wait
 load (r14+$38),r2
 btst #0,r2
 jr z,.wait
 nop
 movefa screen0.a,r2
 store r2,(r14)
 movei #BLIT_PITCH2|BLIT_PIXEL16|BLIT_WID384|BLIT_XADDPIX,r2
 store r2,(r14+_BLIT_A1_FLAGS)
 moveq #0,r2
 store r2,(r14+_BLIT_A1_CLIP)
 store r2,(r14+_BLIT_A1_PIXEL)
 store r2,(r14+_BLIT_A2_PIXEL)
 store r1,(r14+_BLIT_A2_BASE)
 movei #BLIT_PITCH1|BLIT_PIXEL16|BLIT_WID384|BLIT_XADDPIX,r2
 store r2,(r14+_BLIT_A2_FLAGS)
 movei #(1<<16)|((-384)&$ffff),r2
 store r2,(r14+_BLIT_A1_STEP)
 store r2,(r14+_BLIT_A2_STEP)
 movei #200<<16|384,r2
 store r2,(r14+_BLIT_COUNT)
 movei #BLIT_SRCEN|BLIT_LFU_REPLACE|BLIT_UPDA1|BLIT_UPDA2,r2
 store r2,(r14+_BLIT_CMD)
.waitdone
 load (r14+$38),r2
 btst #0,r2
 jr z,.waitdone
 nop
 cmpq #0,r0
 movei #frontdraw_selection,r1
 jump eq,(r1)
 nop
 cmpq #1,r0
 movei #frontdraw_controls,r1
 jump eq,(r1)
 nop
 cmpq #2,r0
 movei #frontdraw_scores,r1
 jump eq,(r1)
 nop
 cmpq #5,r0
 movei #frontdraw_settings,r1
 jump eq,(r1)
 nop
 FRONT_TEXT credits_one,126,61
 FRONT_TEXT credits_two,126,85
 FRONT_TEXT credits_three,126,109
 FRONT_TEXT credits_four,126,133
 FRONT_TEXT return_text,126,164
 POPLR
frontdraw_controls:
 FRONT_TEXT controls_one,126,61
 FRONT_TEXT controls_two,126,85
 FRONT_TEXT controls_three,126,109
 FRONT_TEXT controls_four,126,133
 FRONT_TEXT return_text,126,164
 POPLR
frontdraw_selection:
 movei #FRONT+4,r0
 load (r0),r0
 moveq #18,r1
 mult r1,r0
 movei #81,r1
 add r1,r0
 movei #1536,r1
 mult r1,r0
 movei #136/4*16,r1
 add r1,r0
 movefa screen0.a,r1
 add r1,r0
 movei #FRONT_ORANGE,r2
 movei #140,r3
.line
 storew r2,(r0)
 addq #2,r0
 subq #1,r3
 btst #1,r3
 jr ne,.samephrase
 btst #0,r3
 jr ne,.samephrase
 nop
 addq #8,r0
.samephrase
 cmpq #0,r3
 jr ne,.line
 nop
 movei #FRONT+4,r0
 load (r0),r0
 cmpq #4,r0
 movei #.selection_help,r9
 jump ne,(r9)
 nop
 movei #REPLAY+4,r0
 load (r0),r0
 cmpq #2,r0
 movei #.selection_help,r9
 jump cc,(r9)
 nop
 FRONT_TEXT no_recording,136,174
 POPLR
.selection_help
 FRONT_TEXT select_text,136,174
 POPLR
frontdraw_scores:
 FRONT_TEXT manual_label,126,61
 movei #FRONT+24,r0
 load (r0),r0
 cmpq #0,r0
 movei #FRONT+$80,r0
 jr ne,.manual_present
 nop
 movei #no_record-MODrun_frontdraw+MODstart_frontdraw,r0
.manual_present
 movei #126,r1
 movei #83,r2
 movei #FRONT_BLUE,r3
 movei #front_text,r8
 BL (r8)
 FRONT_TEXT assisted_label,126,110
 movei #FRONT+40,r0
 load (r0),r0
 cmpq #0,r0
 movei #FRONT+$a0,r0
 jr ne,.assisted_present
 nop
 movei #no_record-MODrun_frontdraw+MODstart_frontdraw,r0
.assisted_present
 movei #126,r1
 movei #132,r2
 movei #FRONT_BLUE,r3
 movei #front_text,r8
 BL (r8)
 FRONT_TEXT return_text,126,164
 POPLR

frontdraw_replay:
 FRONT_TEXT replay_label,24,65
 movei #REPLAY+32,r0
 load (r0),r0
 cmpq #0,r0
 movei #.playing_label,r9
 jump eq,(r9)
 nop
 FRONT_TEXT replay_ended,24,89
.playing_label
 POPLR

frontdraw_result:
 ; A compact dark panel leaves the underlying track visible around the result.
 movefa screen0.a,r0
 movei #62*1536+100/4*16,r1
 add r1,r0
 movei #118,r5
 moveq #0,r2
.row
 move r0,r1
 movei #184,r3
.pixel
 storew r2,(r1)
 addq #2,r1
 subq #1,r3
 btst #1,r3
 jr ne,.same
 btst #0,r3
 jr ne,.same
 nop
 addq #8,r1
.same
 cmpq #0,r3
 jr ne,.pixel
 nop
 movei #1536,r1
 add r1,r0
 subq #1,r5
 movei #.row,r8
 jump ne,(r8)
 nop
 movei #GAME+8,r0
 load (r0),r0
 movei #finish_title-MODrun_frontdraw+MODstart_frontdraw,r1
 cmpq #2,r0
 jr ne,.title_chosen
 nop
 movei #destroyed_title-MODrun_frontdraw+MODstart_frontdraw,r1
.title_chosen
 move r1,r0
 movei #128,r1
 movei #64,r2
 movei #FRONT_BLUE,r3
 movei #front_text,r8
 BL (r8)
.resulttimes
 FRONT_TEXT total_label,108,90
 movei #$1205,r0
 movei #172,r1
 movei #90,r2
 movei #FRONT_WHITE,r3
 movei #front_text,r8
 BL (r8)
 FRONT_TEXT lap_label,108,115
 movei #$1222,r0
 movei #172,r1
 movei #115,r2
 movei #FRONT_WHITE,r3
 movei #front_text,r8
 BL (r8)
 movei #result_return-MODrun_frontdraw+MODstart_frontdraw,r0
 movei #FRONT+60,r1
 load (r1),r1
 cmpq #2,r1
 jr ne,.not_saved
 nop
 movei #record_saved-MODrun_frontdraw+MODstart_frontdraw,r0
.not_saved
 cmpq #3,r1
 jr ne,.save_label
 nop
 movei #save_failed-MODrun_frontdraw+MODstart_frontdraw,r0
.save_label
 movei #108,r1
 movei #150,r2
 movei #FRONT_WHITE,r3
 movei #front_text,r8
 BL (r8)
 POPLR

; r0 string in DRAM, r1 x,r2 y,r3 CrY. Proportional converted original font.
front_text:
 move r0,r10
 move r1,r11
 move r2,r12
 move r3,r13
 movefa screen0.a,r16
.char
 loadb (r10),r0
 addq #1,r10
 cmpq #0,r0
 jump eq,(LR)
 nop
 subq #32,r0
 move r0,r1
 movei #front_widths,r2
 add r0,r2
 loadb (r2),r25
 movei #48,r2
 mult r2,r0
 movei #front_font,r17
 add r0,r17
 move r12,r18
 moveq #24,r19
.glyphrow
 loadw (r17),r20
 addq #2,r17
 move r18,r0
 movei #1536,r1
 mult r1,r0
 add r16,r0
 move r11,r1
 shrq #2,r1
 shlq #4,r1
 add r1,r0
 move r11,r21
 moveq #3,r1
 and r1,r21
 shlq #1,r21
 add r21,r0
 move r11,r21
 moveq #16,r22
.glyphpixel
 btst #15,r20
 jr eq,.transparent
 nop
 storew r13,(r0)
.transparent
 shlq #1,r20
 addq #2,r0
 addq #1,r21
 btst #1,r21
 jr ne,.noextra
 btst #0,r21
 jr ne,.noextra
 nop
 addq #8,r0
.noextra
 subq #1,r22
 movei #.glyphpixel,r8
 jump ne,(r8)
 nop
 addq #1,r18
 subq #1,r19
 movei #.glyphrow,r8
 jump ne,(r8)
 nop
 add r25,r11
 movei #.char,r8
 jump (r8)
 nop
 include "settings_draw.inc"
 align 4
record_saved: dc.b "RECORD SAVED",0
save_failed: dc.b "EEPROM UNAVAILABLE",0
no_record: dc.b "NO RECORD",0
no_recording: dc.b "NO RECORDING YET",0
replay_label: dc.b "REPLAY   PAUSE / OPTION",0
replay_ended: dc.b "END OF RECORDING",0
select_text: dc.b "UP/DOWN SELECT   A CONFIRM",0
controls_one: dc.b "A / UP: THRUST",0
controls_two: dc.b "LEFT / RIGHT: STEER   B: BRAKE",0
controls_three: dc.b "C: AUTOPILOT   PAUSE: HOLD",0
controls_four: dc.b "OPTION: RESTART / MENU",0
credits_one: dc.b "HEXGL BY BKCORE",0
credits_two: dc.b "THIBAUT DESPOULAIN",0
credits_three: dc.b "NATIVE ENGINE: 42BASTIAN",0
credits_four: dc.b "FONT: BEBAS NEUE",0
return_text: dc.b "OPTION: MAIN MENU",0
manual_label: dc.b "MANUAL BEST",0
assisted_label: dc.b "AUTOPILOT BEST",0
finish_title: dc.b "RACE COMPLETE",0
destroyed_title: dc.b "DESTROYED",0
total_label: dc.b "TOTAL",0
lap_label: dc.b "LAP BEST",0
result_return: dc.b "OPTION: MAIN MENU",0
 align 8
 ENDMODULE frontdraw
 echo "ENDE (frontdraw): %HMODend_frontdraw"
