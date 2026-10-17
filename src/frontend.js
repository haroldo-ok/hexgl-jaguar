; Native front-end controller and 93C46 cartridge EEPROM journal.
; Does not replace the emulator EEPROM or patch game RAM from the host.
 MODULE frontend,MODend_irq
 PUSHLR
 JOYPAD1 99
 movei #FRONT,r14
 load (r14),r0
 movei #$46524e54,r1
 cmp r1,r0
 movei #front_initialized,r2
 jump eq,(r2)
 nop
 move r1,r20
 move r14,r0
 moveq #0,r1
 movei #48,r2
.zero
 store r1,(r0)
 addq #4,r0
 subq #1,r2
 jr ne,.zero
 nop
 store r20,(r14)
 movei #ee_load,r0
 BL (r0)
 movei #front_format_all,r0
 BL (r0)
front_initialized:
 movei #settings_input,r0
 BL (r0)
 movei #FRONT,r14
 movei #LastJoy+4,r0
 load (r0),r0
 btst #JOY_OPTION_BIT,r0
 jr eq,.keep_selection
 nop
 moveq #0,r0
 store r0,(r14+4)
 store r0,(r14+8)
.keep_selection
 moveq #0,r0
 store r0,(r14+12)
 movei #GAME,r15
 load (r15+8),r0
 load (r14+76),r1
 store r0,(r14+76)
 cmpq #0,r0
 movei #front_menu,r2
 jump eq,(r2)
 nop
 cmpq #1,r0
 movei #.active,r9
 jump eq,(r9)
 cmpq #4,r0
 jr ne,.finished
 nop
.active
 load (r15+56),r2
 cmpq #0,r2
 jr eq,.finished
 nop
 moveq #1,r2
 store r2,(r14+56)
.finished
 cmpq #3,r0
 movei #front_return,r2
 jump ne,(r2)
 nop
 cmpq #3,r1
 jump eq,(r2)
 nop
 movei #ee_save_result,r0
 BL (r0)
 movei #front_format_all,r0
 BL (r0)
 movei #front_return,r0
 jump (r0)
 nop
front_menu:
 moveq #0,r0
 store r0,(r14+56)
 store r0,(r14+60)
 movei #LastJoy+4,r0
 load (r0),r20
 btst #JOY_OPTION_BIT,r20
 jr eq,.keepmenu
 nop
 moveq #0,r0
 store r0,(r14+4)
 store r0,(r14+8)
.keepmenu
 load (r14+8),r0
 cmpq #0,r0
 movei #front_panel,r1
 jump ne,(r1)
 nop
 load (r14+4),r0
 btst #JOY_DOWN_BIT,r20
 jr eq,.up
 nop
 addq #1,r0
.up
 btst #JOY_UP_BIT,r20
 jr eq,.wrap
 nop
 subq #1,r0
.wrap
 cmpq #0,r0
 jr pl,.positive_choice
 nop
 moveq #5,r0
.positive_choice
 cmpq #6,r0
 jr ne,.valid_choice
 nop
 moveq #0,r0
.valid_choice
 store r0,(r14+4)
 cmpq #0,r0
 movei #front_return,r1
 jump eq,(r1)
 nop
 moveq #1,r1
 store r1,(r14+12)
 btst #JOY_A_BIT,r20
 movei #front_return,r1
 jump eq,(r1)
 nop
 cmpq #4,r0
 movei #.regular_panel,r9
 jump ne,(r9)
 nop
 movei #REPLAY,r15
 load (r15+4),r0
 cmpq #1,r0
 jump cs,(r1)
 nop
 jump eq,(r1)
 nop
 moveq #1,r0
 store r0,(r15+8)
 moveq #0,r0
 store r0,(r15+12)
 store r0,(r15+16)
 store r0,(r15+32)
 store r0,(r15+40)
 movei #VBL_TICKS,r2
 load (r2),r2
 store r2,(r15+20)
 movei #GAME,r15
 store r0,(r15+52)
 moveq #5,r0
 store r0,(r15+8)
 jump (r1)
 nop
.regular_panel
 store r0,(r14+8)
 jump (r1)
 nop
front_panel:
 moveq #1,r0
 store r0,(r14+12)
 movei #FRONT+8,r1
 load (r1),r1
 cmpq #5,r1
 jr ne,.notsettings
 nop
 movei #settings_panel,r8
 BL (r8)
.notsettings
 ; Option returns to the main screen through the normal reset path.
front_return:
 POPLR

; Read all four 8-word journal slots. No EEPROM writes occur at boot.
ee_load:
 PUSHLR
 moveq #0,r20
 movei #EE_BUFFER,r21
.loop
 move r20,r0
 movei #ee_read,r8
 BL (r8)
 storew r0,(r21)
 addq #2,r21
 addq #1,r20
 cmpq #0,r20
 movei #32,r0
 cmp r0,r20
 jr ne,.loop
 nop
 movei #FRONT+24,r24
 moveq #0,r25
 movei #ee_choose,r8
 BL (r8)
 movei #FRONT+40,r24
 moveq #16,r25
 movei #ee_choose,r8
 BL (r8)
 POPLR

; r24 category state, r25 first EEPROM word (0 manual,16 assisted).
ee_choose:
 PUSHLR
 move r25,r0
 addq #8,r0
 move r24,r7
 addq #12,r7
 store r0,(r7)
 move r25,r26
 shlq #1,r26
 movei #EE_BUFFER,r0
 add r0,r26
 move r26,r0
 movei #ee_validate,r8
 BL (r8)
 move r0,r20
 move r26,r0
 addq #16,r0
 movei #ee_validate,r8
 BL (r8)
 cmpq #0,r0
 movei #.a,r9
 jump eq,(r9)
 nop
 cmpq #0,r20
 jr eq,.b
 nop
 move r26,r0
 addq #2,r0
 loadw (r0),r1
 addq #16,r0
 loadw (r0),r2
 sub r2,r1
 shlq #16,r1
 sharq #16,r1
 cmpq #0,r1
 jr pl,.a
 nop
.b
 addq #16,r26
 addq #8,r25
 jr .use
 nop
.a
 cmpq #0,r20
 movei #ee_choose_done,r0
 jump eq,(r0)
 nop
.use
 move r26,r7
 addq #4,r7
 load (r7),r0
 store r0,(r24)
 move r26,r7
 addq #8,r7
 load (r7),r0
 move r24,r7
 addq #4,r7
 store r0,(r7)
 move r26,r0
 addq #2,r0
 loadw (r0),r0
 move r24,r7
 addq #8,r7
 store r0,(r7)
 move r24,r7
 addq #12,r7
 store r25,(r7)
 movei #FRONT+68,r0
 load (r0),r1
 addq #1,r1
 store r1,(r0)
ee_choose_done:
 POPLR

; Validate magic, version, bounded nonzero scores and checksum. r0 ptr -> bool.
ee_validate:
 move r0,r4
 loadw (r0),r1
 movei #$4847,r2
 cmp r2,r1
 movei #ee_invalid,r8
 jump ne,(r8)
 nop
 addq #12,r0
 loadw (r0),r1
 cmpq #1,r1
 jump ne,(r8)
 nop
 move r4,r7
 addq #4,r7
 load (r7),r1
 move r4,r7
 addq #8,r7
 load (r7),r2
 cmpq #0,r1
 jump eq,(r8)
 nop
 cmpq #0,r2
 jump eq,(r8)
 nop
 movei #6000000,r3
 cmp r3,r1
 jump cc,(r8)
 nop
 cmp r1,r2
 jr eq,.score_ordered
 nop
 jump cc,(r8)
 nop
.score_ordered
 move r4,r0
 addq #2,r0
 movei #$a5c3,r1
 moveq #6,r2
.xor
 loadw (r0),r3
 xor r3,r1
 addq #2,r0
 subq #1,r2
 jr ne,.xor
 nop
 loadw (r0),r2
 cmp r2,r1
 jump ne,(r8)
 nop
 moveq #1,r0
 jump (LR)
 nop
ee_invalid:
 moveq #0,r0
 jump (LR)
 nop

; Journal improved results only. Assisted and manual records never compete.
ee_save_result:
 PUSHLR
 movei #FRONT,r14
 movei #FRONT+24,r24
 load (r14+56),r0
 cmpq #0,r0
 jr eq,.category
 nop
 addq #16,r24
.category
 movei #GAME,r15
 load (r15+64),r0
 load (r15+80),r1
 movei #fields_ms,r8
 BL (r8)
 move r0,r20
 load (r15+100),r0
 load (r15+80),r1
 movei #fields_ms,r8
 BL (r8)
 move r0,r21
 moveq #0,r22
 load (r24),r0
 cmpq #0,r0
 jr eq,.total
 nop
 cmp r0,r20
 jr cc,.lap
 nop
.total
 store r20,(r24)
 moveq #1,r22
.lap
 move r24,r7
 addq #4,r7
 load (r7),r0
 cmpq #0,r0
 jr eq,.bestlap
 nop
 cmp r0,r21
 jr cc,.ready
 nop
.bestlap
 move r24,r7
 addq #4,r7
 store r21,(r7)
 moveq #1,r22
.ready
 cmpq #0,r22
 movei #ee_save_done,r0
 jump eq,(r0)
 nop
 moveq #1,r0
 store r0,(r14+60)
 move r24,r7
 addq #8,r7
 load (r7),r0
 addq #1,r0
 shlq #16,r0
 shrq #16,r0
 movei #EE_WORK,r23
 move r23,r1
 addq #2,r1
 storew r0,(r1)
 load (r24),r0
 move r23,r7
 addq #4,r7
 store r0,(r7)
 move r24,r7
 addq #4,r7
 load (r7),r0
 move r23,r7
 addq #8,r7
 store r0,(r7)
 move r23,r1
 addq #12,r1
 moveq #1,r0
 storew r0,(r1)
 move r23,r1
 addq #2,r1
 movei #$a5c3,r0
 moveq #6,r2
.checksum
 loadw (r1),r3
 xor r3,r0
 addq #2,r1
 subq #1,r2
 jr ne,.checksum
 nop
 storew r0,(r1)
 move r24,r7
 addq #12,r7
 load (r7),r25
 moveq #8,r0
 xor r0,r25
 ; Invalidate target slot before writing payload; old slot remains intact.
 move r25,r0
 moveq #0,r1
 movei #ee_write,r8
 BL (r8)
 moveq #1,r26
.payload
 move r26,r1
 shlq #1,r1
 add r23,r1
 loadw (r1),r1
 move r25,r0
 add r26,r0
 movei #ee_write,r8
 BL (r8)
 addq #1,r26
 cmpq #8,r26
 jr ne,.payload
 nop
 ; Commit magic last, then verify the entire slot via serial readback.
 move r25,r0
 movei #$4847,r1
 movei #ee_write,r8
 BL (r8)
 moveq #0,r26
.readback
 move r25,r0
 add r26,r0
 movei #ee_read,r8
 BL (r8)
 move r26,r1
 shlq #1,r1
 add r23,r1
 storew r0,(r1)
 addq #1,r26
 cmpq #8,r26
 jr ne,.readback
 nop
 move r23,r0
 movei #ee_validate,r8
 BL (r8)
 cmpq #0,r0
 movei #.failed,r9
 jump eq,(r9)
 nop
 move r23,r7
 addq #4,r7
 load (r7),r0
 load (r24),r1
 cmp r1,r0
 movei #.failed,r9
 jump ne,(r9)
 nop
 move r23,r7
 addq #8,r7
 load (r7),r0
 move r24,r7
 addq #4,r7
 load (r7),r1
 cmp r1,r0
 movei #.failed,r9
 jump ne,(r9)
 nop
 move r23,r0
 addq #2,r0
 loadw (r0),r0
 move r24,r7
 addq #8,r7
 store r0,(r7)
 move r24,r7
 addq #12,r7
 store r25,(r7)
 moveq #2,r0
 jr .status
 nop
.failed
 moveq #3,r0
.status
 movei #FRONT+60,r1
 store r0,(r1)
ee_save_done:
 POPLR

; r0 address -> r0 word. Word I/O preserves EEPROM DO bit on actual JERRY.
ee_read:
 PUSHLR
 movei #$180,r1
 or r1,r0
 shlq #23,r0
 moveq #9,r1
 movei #$f15000,r2
 loadw (r2),r2
 movei #ee_bits,r8
 BL (r8)
 movei #$f14000,r4
 moveq #16,r5
 moveq #0,r0
.read
 loadw (r4),r1
 moveq #1,r2
 and r2,r1
 shlq #1,r0
 or r1,r0
 moveq #16,r3
.delay
 subq #1,r3
 jr ne,.delay
 nop
 subq #1,r5
 jr ne,.read
 nop
 POPLR

; r0 address, r1 data. Bounded busy wait, so absent EEPROM cannot freeze game.
ee_write:
 PUSHLR
 move r0,r10
 move r1,r11
 movei #$130<<23,r0
 moveq #9,r1
 movei #$f15000,r2
 loadw (r2),r2
 movei #ee_bits,r8
 BL (r8)
 move r10,r0
 movei #$140,r1
 or r1,r0
 shlq #23,r0
 moveq #9,r1
 movei #$f15000,r2
 loadw (r2),r2
 movei #ee_bits,r8
 BL (r8)
 move r11,r0
 shlq #16,r0
 moveq #16,r1
 movei #ee_bits,r8
 BL (r8)
 movei #VBL_TICKS,r4
 load (r4),r5
 movei #$f14000,r6
.busy
 loadw (r6),r0
 btst #0,r0
 jr ne,.written
 nop
 load (r4),r0
 sub r5,r0
 cmpq #3,r0
 jr mi,.busy
 nop
.written
 movei #FRONT+64,r0
 load (r0),r1
 addq #1,r1
 store r1,(r0)
 ; Disable writes after every word, including after a timeout.
 movei #$100<<23,r0
 moveq #9,r1
 movei #$f15000,r2
 loadw (r2),r2
 movei #ee_bits,r8
 BL (r8)
 POPLR

ee_bits:
 movei #$f14800,r4
.bit_loop
 move r0,r2
 shrq #31,r2
 storew r2,(r4)
 shlq #1,r0
 moveq #16,r3
.bit_delay
 subq #1,r3
 jr ne,.bit_delay
 nop
 subq #1,r1
 jr ne,.bit_loop
 nop
 jump (LR)
 nop

; Video fields -> milliseconds, split multiply avoids 16-bit operand truncation.
fields_ms:
 move r0,r2
 div r1,r2
 movei #6000,r3
 cmp r3,r2
 jr cs,.inrange
 nop
 movei #5999990,r0
 jump (LR)
 nop
.inrange
 move r2,r3
 mult r1,r3
 sub r3,r0
 movei #1000,r3
 mult r3,r0
 div r1,r0
 mult r3,r2
 add r2,r0
 jump (LR)
 nop

front_format_all:
 PUSHLR
 movei #FRONT+24,r18
 movei #FRONT+$80,r19
 moveq #4,r22
.next
 load (r18),r0
 move r19,r1
 movei #format_ms,r8
 BL (r8)
 addq #4,r18
 addq #16,r19
 subq #1,r22
 cmpq #2,r22
 jr ne,.notgap
 nop
 addq #8,r18
.notgap
 cmpq #0,r22
 movei #.next,r9
 jump ne,(r9)
 nop
 POPLR

format_ms:
 PUSHLR
 move r0,r6
 movei #60000,r2
 div r2,r0
 move r0,r3
 mult r2,r3
 sub r3,r6
 movei #format_pair,r8
 BL (r8)
 moveq #26,r2
 addq #32,r2
 storeb r2,(r1)
 addq #1,r1
 move r6,r0
 movei #1000,r2
 div r2,r0
 move r0,r3
 mult r2,r3
 sub r3,r6
 movei #format_pair,r8
 BL (r8)
 movei #46,r2
 storeb r2,(r1)
 addq #1,r1
 move r6,r0
 movei #100,r2
 div r2,r0
 move r0,r3
 mult r2,r3
 sub r3,r6
 addq #32,r0
 addq #16,r0
 storeb r0,(r1)
 addq #1,r1
 move r6,r0
 movei #format_pair,r8
 BL (r8)
 moveq #0,r0
 storeb r0,(r1)
 POPLR
format_pair:
 move r0,r2
 moveq #10,r3
 div r3,r2
 move r2,r4
 mult r3,r4
 sub r4,r0
 addq #32,r2
 addq #16,r2
 storeb r2,(r1)
 addq #1,r1
 addq #32,r0
 addq #16,r0
 storeb r0,(r1)
 addq #1,r1
 jump (LR)
 nop
 include "settings.inc"
 align 8
 ENDMODULE frontend
 echo "ENDE (frontend): %HMODend_frontend"
