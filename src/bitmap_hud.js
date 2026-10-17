; Original BKcore HUD artwork, converted by tools/hud.py.
; Clip geometry from HUD.js (CC BY-NC 3.0, Thibaut Despoulain).
; Draw only into the completed BACK buffer; main loop publishes at next VBL.
 MODULE bitmap_hud,MODend_irq
 PUSHLR
 ; The settings panel uses the upper viewport for its original-font title.
 movei #GAME+8,r0
 load (r0),r0
 cmpq #0,r0
 jr ne,.settings_done
 nop
 movei #FRONT+8,r0
 load (r0),r0
 cmpq #5,r0
 jr ne,.settings_done
 nop
 POPLR
.settings_done
 movei #SETTINGS+4,r0
 load (r0),r0
 cmpq #0,r0
 movei #.hudvisible,r3
 jump ne,(r3)
 nop
 movei #GAME+8,r0
 load (r0),r0
 cmpq #1,r0
 jr eq,.hidehud
 nop
 cmpq #4,r0
 jr eq,.hidehud
 nop
 cmpq #5,r0
 movei #.hudvisible,r3
 jump ne,(r3)
 nop
.hidehud
 movei #TxtScreen,r0
 movei #((max_x_txt>>3)*max_y_txt)/4,r1
 moveq #0,r2
.cleartext
 store r2,(r0)
 addq #4,r0
 subq #1,r1
 jr ne,.cleartext
 nop
 POPLR
.hudvisible
 ; Renderer may have launched its final blit asynchronously.
 movei #BLIT_A1_BASE,r14
.hudwait
 load (r14+$38),r0
 btst #0,r0
 jr z,.hudwait
 nop
 movefa screen0.a,r3
 movei #hud_bg_data,r0
 movei #HUD_BG_COUNT,r1
 moveq #0,r2
 movei #hud_layer,r8
 BL (r8)
 movei #GAME+32,r4
 load (r4),r2
 movei #hud_speed_data,r0
 movei #HUD_SPEED_COUNT,r1
 BL (r8)
 movei #GAME+36,r4
 load (r4),r2
 movei #hud_shield_data,r0
 movei #HUD_SHIELD_COUNT,r1
 BL (r8)
 ; Same native numeric scale as the existing footer: speed * 10, shield %.
 movei #GAME+32,r4
 load (r4),r0
 moveq #10,r1
 mult r1,r0
 movei #14*384*4+180/4*16,r9
 add r3,r9
 movei #hud_number,r8
 BL (r8)
 movei #GAME+36,r4
 load (r4),r0
 movei #25*384*4+180/4*16,r9
 add r3,r9
 BL (r8)
 POPLR

; r0 records, r1 count, r2 live threshold, r3 back buffer.
; r8 stays as this routine's entry, r3 stays intact.
hud_layer:
 load (r0),r4
 addq #4,r0
 load (r0),r5
 addq #4,r0
 move r4,r6
 shrq #24,r6
 cmp r6,r2
 jr cs,.skip
 nop
 shlq #8,r4
 shrq #8,r4
 add r3,r4
 storew r5,(r4)
.skip
 subq #1,r1
 jr ne,hud_layer
 nop
 jump (LR)
 nop

; Three 8x8 native digits. r9 aligned to four-pixel phrase, advance by 8 pixels.
hud_number:
 PUSHLR
 move r0,r10
 movei #100,r11
 moveq #3,r12
.digit
 move r10,r0
 div r11,r0
 move r0,r1
 mult r11,r1
 sub r1,r10
 shlq #3,r0
 movei #ASCII+8+48*8,r4
 add r0,r4
 move r9,r5
 moveq #8,r6
.row
 loadb (r4),r7
 addq #1,r4
 moveq #8,r13
 move r5,r15
.pixel
 shlq #1,r7
 moveq #0,r16
 btst #8,r7
 jr eq,.blank
 nop
 movei #$88ff,r16
.blank
 storew r16,(r15)
 addq #2,r15
 subq #1,r13
 btst #1,r13
 jr ne,.notphrase
 btst #0,r13
 jr ne,.notphrase
 nop
 addq #8,r15
.notphrase
 cmpq #0,r13
 movei #.pixel,r17
 jump ne,(r17)
 nop
 movei #384*4,r0
 add r0,r5
 subq #1,r6
 movei #.row,r17
 jump ne,(r17)
 nop
 addq #32,r9
 moveq #10,r0
 div r0,r11
 subq #1,r12
 movei #.digit,r17
 jump ne,(r17)
 nop
 POPLR
 align 8
 ENDMODULE bitmap_hud
 echo "Size (bitmap HUD): %HMODlen_bitmap_hud"
 echo "ENDE (bitmap HUD): %HMODend_bitmap_hud"
