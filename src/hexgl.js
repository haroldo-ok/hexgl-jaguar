;; -*-asm-*-

LYXASS	EQU 1
	gpu

GOURAUD		set 0
SOFTCLIP	set 1
LANDSCAPE	set 0
TEXTURE		set 1
DARKEN		set 0		; distance darkening (broken!)

FPS		set 1		; fixed number of rendering frames

IFND MOD
MOD		EQU 0
ENDIF

chip		equ 0
gone		equ 0
galactic	equ 1

	include <js/symbols/jagregeq.js>
	include <js/symbols/blit_eq.js>
	include <js/macro/help.mac>
	include <js/macro/module.mac>

	include "globalreg.h"
	include "video.h"
	include "structs.inc"
	include "engine.h"
	include "game.h"
 IF MOD = 1
	include "hively.inc"
 ENDIF


//->CAM_X	equ -3372
//->CAM_Y	equ 50
//->CAM_Z	equ 2843
//->CAM_ANGLE EQU 88

CAM_X		equ -9072
CAM_Y		equ 1628
CAM_Z		equ -3704
CAM_ANGLE	equ 0

;;; -590 10 336 168
;;->CAM_X		equ -280
;;->CAM_Y		equ 50
;;->CAM_Z		equ 1900
;;->CAM_ANGLE	equ 52

//->CAM_X		equ -318
//->CAM_Y		equ 50
//->CAM_Z		equ 2468
//->CAM_ANGLE	equ 256

	echo "TxtScreen: %H TxtScreen"
	echo "screen1:   %H screen1"
	echo "screen0:   %H screen0"

MACRO MyINITMODULE
.\dest equ (MODrun_\0)+$8000
 IF MODrun_\0 >= $f03000
	movei #(MODrun_\0)+$8000,r0	; dest-adr
 ELSE
	movei #(MODrun_\0),r0	; dest-adr
 ENDIF
	movei #MODstart_\0,r1
	movei #1<<16|(MODlen_\0 >> 2),r2
	movei #overlay,r3
	BL (r3)
ENDM

	macro	storei
	store	\0,(\1)
	addqt	#4,\1
	endm

stacktop	equ $f03ffc

IRQ_STACK	equ $f03020-4

object_data	equ $110000

	macro	defobj 	; name,npoints,nfaces
	RSB	\0_rotated,	 	4+\1*_3d_size
	RSB	\0_projected,		4+\1*proj_size
	RSB	\0_normals_rotated,	4+\2*_3d_size
	RSB	\0_vnormals_rotated,	4+\1*_3d_size
	RSB	\0_visible,		4+\2*4
;;->	echo "\0 p %H\0_projected"
;;->	echo "\0 r %H\0_rotated"
//->	echo "\0 n %H\0_normals_rotated"
;;->	echo "\0 v %H\0_vnormals_rotated"
	endm

	include "../assets/limits.inc"
	RSSET object_data
	defobj scratch,MAX_VERTICES,MAX_FACES
	RSALIGN 8
	RSL tri_ptrs_ram,1024
	RSB tri_array_ram,24*8192+32
tri_array_end equ RSADDR
mem_end	EQU RSADDR

	echo "memory end: %H mem_end"

	echo "stacktop %H stacktop"
 IFD x_save
	echo "x_save %H x_save"
 ENDIF

	RSSET $800
	RSL	OBJECT_LIST,64
	RSL	CAMERA_X
	RSL	CAMERA_Y
	RSL	CAMERA_Z
	RSL	CAMERA_ANGLE_Y
	RSL	CAMERA_SPEED
	RSL	LIGHT_X
	RSL	LIGHT_Y
	RSL	LIGHT_Z
	RSL	RLIGHT_X
	RSL	RLIGHT_Y
	RSL	RLIGHT_Z
	RSL	OBJECT_PTR
	RSL	ANGLE_X
	RSL	ANGLE_Y
	RSL	ANGLE_Z
	RSL	X_POS
	RSL	Y_POS
	RSL	Z_POS
	RSL	USE_GOURAUD
	RSL	USE_PHRASE
	RSL	IS_PAL
	RSL	LastJoy,2

_CAMERA_Y	EQU CAMERA_Y-CAMERA_X
_CAMERA_Z	EQU CAMERA_Z-CAMERA_X
_CAMERA_ANGLE_Y	EQU CAMERA_ANGLE_Y-CAMERA_X
_CAMERA_SPEED	EQU CAMERA_SPEED-CAMERA_X
_LIGHT_X	EQU LIGHT_X-CAMERA_X
_LIGHT_Y	EQU LIGHT_Y-CAMERA_X
_LIGHT_Z	EQU LIGHT_Z-CAMERA_X
_RLIGHT_X	EQU RLIGHT_X-CAMERA_X
_RLIGHT_Y	EQU RLIGHT_Y-CAMERA_X
_RLIGHT_Z	EQU RLIGHT_Z-CAMERA_X

	include <js/var/txtscr.var>

	echo "RSPC: %H RSADDR"

	MACRO WAITBLITTER
.\waitblit	load (blitter+$38),tmp0
	btst	#0,tmp0
	jr	z,.\waitblit
	nop
	ENDM

	run $2000
//->	run $6000 		; for VJ
start::
********************
* init
init:
	movei	#skip_modules,r0
	nop
	jump	(r0)
	nop
	dc.l	$4e722700
	include "irq.js"
//->	include "genmap.inc"
	include "engine.js"
	include "control.js"
	include "pose.js"
	include "handling.js"
	include "view.js"
; Real banked panorama resampling using Jaguar A1 fractional source increments.
; Source CameraChase cube orientation counterpart: all original six sky faces.
; No framebuffer readback, host drawing, tiled imitation or extra framebuffer.
 MODULE skybank,MODend_irq
 PUSHLR
 movei #SKY_STATE,r15
 movei #$534b5942,r0
 store r0,(r15)
 moveq #0,r0
 store r0,(r15+12)
 movei #VIEW+28,r0
 load (r0),r0
 cmpq #0,r0
 movei #skybank_done,r1
 jump eq,(r1)
 nop
 move r0,r19
 shlq #16,r19
 sharq #16,r19
 move r0,r18
 shrq #16,r18
 ; Center yaw is the unrolled crop center, wrapped per scanline/segment.
 movei #CAMERA_ANGLE_Y,r0
 load (r0),r0
 neg r0
 movei #192,r1
 add r1,r0
 movei #2047,r1
 and r1,r0
 store r0,(r15+16)
 move r0,r20
 ; Same native vertical look-at projection as the engine's unrolled crop.
 movei #PHYS+48,r0
 load (r0),r0
 sharq #8,r0
 movei #2044,r1
 and r1,r0
 movei #SinTab,r1
 add r0,r1
 load (r1),r0
 move r0,r1
 shrq #16,r1
 shlq #16,r0
 sharq #16,r0
 movei #176,r2
 imult r2,r0
 move r0,r2
 abs r0
 div r1,r0
 cmpq #0,r2
 jr pl,.pitchpositive
 nop
 neg r0
.pitchpositive
 movei #256,r1
 add r1,r0
 ; Bound the complete rotated viewport, not just its unrotated top row.
 move r19,r1
 abs r1
 movei #192,r2
 imult r2,r1
 move r18,r2
 movei #100,r3
 imult r3,r2
 add r2,r1
 sharq #15,r1
 addq #2,r1
 cmp r1,r0
 jr pl,.mintop
 nop
 move r1,r0
.mintop
 movei #511,r2
 sub r1,r2
 cmp r2,r0
 jr mi,.maxbottom
 nop
 move r2,r0
.maxbottom
 store r0,(r15+20)
 move r0,r21
 ; Start at screen (0,0), using signed Q16 affine source coordinates.
 shlq #16,r20
 shlq #16,r21
 move r18,r0
 movei #192,r1
 imult r1,r0
 move r19,r2
 movei #100,r3
 imult r3,r2
 add r2,r0
 shlq #1,r0
 move r20,r22
 sub r0,r22
 move r19,r0
 imult r1,r0
 move r18,r2
 imult r3,r2
 sub r2,r0
 shlq #1,r0
 move r21,r23
 add r0,r23
 store r22,(r15+36)
 store r23,(r15+40)
 shlq #1,r18
 shlq #1,r19
 store r18,(r15+24)
 store r19,(r15+28)
 moveq #0,r0
 store r0,(r15+32)
 movei #BLIT_A1_BASE,r14
.wait
 load (r14+$38),r0
 btst #0,r0
 jr eq,.wait
 nop
 movei #$c00000,r0
 store r0,(r14)
 movei #BLIT_PITCH1|BLIT_PIXEL16|BLIT_WID2048|BLIT_XADDINC,r0
 store r0,(r14+_BLIT_A1_FLAGS)
 movefa screen0.a,r16
 store r16,(r14+_BLIT_A2_BASE)
 movei #BLIT_PITCH2|BLIT_PIXEL16|BLIT_WID384|BLIT_XADDPIX,r0
 store r0,(r14+_BLIT_A2_FLAGS)
 moveq #0,r0
 store r0,(r14+_BLIT_A1_STEP)
 store r0,(r14+_BLIT_A1_FSTEP)
 store r0,(r14+_BLIT_A2_STEP)
 move r18,r0
 shrq #16,r0
 move r19,r1
 neg r1
 movei #$ffff0000,r2
 and r2,r1
 or r1,r0
 store r0,(r14+_BLIT_A1_INC)
 move r18,r0
 shlq #16,r0
 shrq #16,r0
 move r19,r1
 neg r1
 shlq #16,r1
 or r1,r0
 store r0,(r14+_BLIT_A1_FINC)
 moveq #0,r17
.row
 movei #$07ffffff,r0
 and r0,r22
 move r22,r26
 move r23,r13
 movei #384,r24
 moveq #0,r25
.segment
 ; A1 lacks an X mask. Split at the actual 2048-wide panorama seam.
 movei #$07ffffff,r0
 sub r26,r0
 div r18,r0
 addq #1,r0
 cmp r24,r0
 jr mi,.segment_size
 nop
 move r24,r0
.segment_size
 move r0,r12
 move r26,r1
 shrq #16,r1
 move r13,r2
 movei #$ffff0000,r3
 and r3,r2
 or r2,r1
 store r1,(r14+_BLIT_A1_PIXEL)
 move r26,r1
 shlq #16,r1
 shrq #16,r1
 move r13,r2
 shlq #16,r2
 or r2,r1
 store r1,(r14+_BLIT_A1_FPIXEL)
 move r17,r1
 shlq #16,r1
 or r25,r1
 store r1,(r14+_BLIT_A2_PIXEL)
 bset #16,r0
 store r0,(r14+_BLIT_COUNT)
 movei #BLIT_SRCEN|BLIT_DSTA2|BLIT_LFU_REPLACE,r0
 store r0,(r14+_BLIT_CMD)
.waitsegment
 load (r14+$38),r0
 btst #0,r0
 jr eq,.waitsegment
 nop
 load (r15+32),r0
 addq #1,r0
 store r0,(r15+32)
 sub r12,r24
 add r12,r25
 cmpq #0,r24
 movei #.nextrow,r0
 jump eq,(r0)
 nop
 move r18,r0
 mult r12,r0
 add r0,r26
 movei #$07ffffff,r0
 and r0,r26
 ; Signed multiplication is split: Q16 sin may exceed signed 16-bit.
 move r19,r0
 sharq #1,r0
 imult r12,r0
 shlq #1,r0
 sub r0,r13
 movei #.segment,r0
 jump (r0)
 nop
.nextrow
 add r19,r22
 add r18,r23
 addq #1,r17
 movei #200,r0
 cmp r0,r17
 movei #.row,r0
 jump ne,(r0)
 nop
 moveq #1,r0
 store r0,(r15+12)
 movei #VIEW+20,r0
 load (r0),r0
 store r0,(r15+8)
 movei #MOTION+64,r0
 load (r0),r0
 store r0,(r15+4)
skybank_done:
 POPLR
 align 8
 ENDMODULE skybank

	include "presentation.js"
; Moving, source-mesh silhouette contact shadow on the original track.
; Hardware adaptation: projected ground-plane affine footprint, not a depth map.
 MODULE postfx,MODend_irq
 PUSHLR
 movei #BLIT_A1_BASE,r14
.waitshadow
 load (r14+$38),r0
 btst #0,r0
 jr eq,.waitshadow
 nop
 movei #POST_STATE,r15
 movei #$504f5354,r0
 store r0,(r15)
 moveq #0,r0
 store r0,(r15+12)
 movei #AVSET+8,r0
 load (r0),r0
 cmpq #0,r0
 movei #post_done,r1
 jump eq,(r1)
 nop
 movei #GAME,r14
 load (r14+8),r0
 cmpq #1,r0
 jr eq,.active
 nop
 cmpq #5,r0
 movei #post_done,r1
 jump ne,(r1)
 nop
.active
 movei #PHYS+16,r0
 load (r0),r0
 cmpq #0,r0
 movei #post_done,r1
 jump ne,(r1)
 nop
 ; Track height map conversion adds exactly 16 native units of hover.
 load (r14+16),r16
 movei #PHYS+32,r0
 load (r0),r17
 movei #16*256,r0
 sub r0,r17
 load (r14+24),r18
 load (r15+56),r0
 addq #1,r0
 bset #0,r0
 store r0,(r15+56)
 move r16,r0
 move r17,r1
 move r18,r2
 movei #post_project,r8
 BL (r8)
 cmpq #0,r3
 movei #post_done,r4
 jump eq,(r4)
 nop
 movei #POST_SCRATCH,r15
 store r0,(r15)
 store r1,(r15+4)
 store r2,(r15+8)
 ; Source Feisar X/Z ground axes, rotated by the real ship heading.
 movei #GAME+28,r0
 load (r0),r0
 movei #SinTab,r15
 load (r15+r0),r19
 move r19,r20
 shrq #16,r20
 move r20,r0
 moveq #15,r1
 imult r1,r0
 sharq #7,r0
 add r16,r0
 move r19,r2
 imult r1,r2
 sharq #7,r2
 add r18,r2
 move r17,r1
 movei #post_project,r8
 BL (r8)
 cmpq #0,r3
 movei #post_done,r4
 jump eq,(r4)
 nop
 movei #POST_SCRATCH,r15
 load (r15),r4
 sub r4,r0
 store r0,(r15+12)
 load (r15+4),r4
 sub r4,r1
 store r1,(r15+16)
 move r19,r0
 moveq #27,r1
 imult r1,r0
 sharq #7,r0
 add r16,r0
 move r20,r2
 imult r1,r2
 sharq #7,r2
 neg r2
 add r18,r2
 move r17,r1
 movei #post_project,r8
 BL (r8)
 cmpq #0,r3
 movei #post_done,r4
 jump eq,(r4)
 nop
 movei #POST_SCRATCH,r15
 load (r15),r4
 sub r4,r0
 store r0,(r15+20)
 load (r15+4),r4
 sub r4,r1
 store r1,(r15+24)
 load (r15+12),r2
 imult r1,r2
 load (r15+16),r3
 imult r0,r3
 sub r3,r2
 move r2,r21
 move r2,r24
 abs r24
 cmpq #4,r24
 movei #post_done,r4
 jump mi,(r4)
 nop
 store r21,(r15+28)
 load (r15+12),r0
 abs r0
 load (r15+20),r1
 abs r1
 add r1,r0
 load (r15),r16
 move r16,r17
 sub r0,r16
 add r0,r17
 cmpq #0,r16
 jr pl,.xmin
 nop
 moveq #0,r16
.xmin
 movei #383,r0
 cmp r0,r17
 jr mi,.xmax
 nop
 move r0,r17
.xmax
 load (r15+16),r0
 abs r0
 load (r15+24),r1
 abs r1
 add r1,r0
 load (r15+4),r18
 move r18,r19
 sub r0,r18
 add r0,r19
 movei #50,r0
 cmp r0,r18
 jr pl,.ymin
 nop
 move r0,r18
.ymin
 movei #199,r0
 cmp r0,r19
 jr mi,.ymax
 nop
 move r0,r19
.ymax
 store r16,(r15+32)
 store r17,(r15+36)
 store r18,(r15+40)
 store r19,(r15+44)
 movei #$9fa000,r20
 movefa screen0.a,r13
 moveq #0,r12
 move r18,r23
.shadow_row
 move r16,r22
.shadow_pixel
 load (r15),r0
 move r22,r4
 sub r0,r4
 load (r15+4),r0
 move r23,r5
 sub r0,r5
 load (r15+24),r0
 imult r4,r0
 load (r15+20),r1
 imult r5,r1
 sub r1,r0
 shlq #3,r0
 cmpq #0,r21
 jr pl,.u_det
 nop
 neg r0
.u_det
 move r0,r1
 abs r0
 div r24,r0
 cmpq #0,r1
 jr pl,.u_signed
 nop
 neg r0
.u_signed
 addq #8,r0
 move r0,r6
 movei #.shadow_next,r8
 cmpq #0,r6
 jump mi,(r8)
 nop
 moveq #16,r0
 cmp r0,r6
 jump cc,(r8)
 nop
 load (r15+12),r0
 imult r5,r0
 load (r15+16),r1
 imult r4,r1
 sub r1,r0
 shlq #3,r0
 cmpq #0,r21
 jr pl,.v_det
 nop
 neg r0
.v_det
 move r0,r1
 abs r0
 div r24,r0
 cmpq #0,r1
 jr pl,.v_signed
 nop
 neg r0
.v_signed
 addq #8,r0
 cmpq #0,r0
 jump mi,(r8)
 nop
 moveq #16,r1
 cmp r1,r0
 jump cc,(r8)
 nop
 shlq #4,r0
 add r6,r0
 shlq #2,r0
 add r20,r0
 load (r0),r9
 shrq #16,r9
 movei #96,r0
 mult r0,r9
 shrq #8,r9
 cmpq #0,r9
 jump eq,(r8)
 nop
 ; Exact interleaved stock framebuffer address and CrY alpha-darkening.
 move r23,r8
 movei #1536,r0
 mult r0,r8
 move r22,r0
 shrq #2,r0
 shlq #4,r0
 add r0,r8
 move r22,r0
 moveq #3,r1
 and r1,r0
 shlq #1,r0
 add r0,r8
 add r13,r8
 loadw (r8),r10
 move r10,r11
 movei #255,r0
 and r0,r11
 movei #256,r0
 sub r9,r0
 mult r0,r11
 shrq #8,r11
 move r10,r0
 movei #$ff00,r1
 and r1,r0
 or r11,r0
 storew r0,(r8)
 addq #1,r12
 ; Last real composed pixel is independently checked in emulator screenshots.
 store r8,(r15+48)
 store r9,(r15+52)
 store r10,(r15+56)
 store r0,(r15+60)
.shadow_next
 addq #1,r22
 cmp r17,r22
 movei #.shadow_pixel,r0
 jump mi,(r0)
 nop
 addq #1,r23
 cmp r19,r23
 movei #.shadow_row,r0
 jump mi,(r0)
 nop
 movei #POST_STATE,r15
 store r12,(r15+12)
post_done:
 movei #POST_STATE,r15
 movei #MOTION+64,r0
 load (r0),r0
 store r0,(r15+4)
 load (r15+56),r0
 addq #1,r0
 bclr #0,r0
 store r0,(r15+56)
 POPLR
post_project:
 PUSHLR
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
 movei #VIEW+28,r0
 load (r0),r0
 cmpq #0,r0
 jr eq,.particle_bank_done
 nop
 move r0,r1
 shrq #16,r1
 imultn r1,r5
 imacn r0,r6
 resmac r3
 neg r0
 imultn r0,r5
 imacn r1,r6
 resmac r6
 sharq #15,r3
 sharq #15,r6
 move r3,r5
.particle_bank_done
 movei #post_project_behind,r0
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
 movei #GAME+80,r1
 load (r1),r1
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
 move r5,r0
 move r6,r1
 moveq #1,r3
 POPLR
post_project_behind:
 moveq #0,r3
 POPLR
 align 8
 ENDMODULE postfx

	include "effects.js"
; Source BloomPass counterpart: separable convolution then additive screen.
; Native low-resolution 48x25, binomial five-tap blur, 0.8 CrY luminance glow.
; Upstream BloomPass has NO bright-pass threshold. Preserve that behavior.
; Stock blitter performs two signed-safe <=102 intensity-add passes per tile.
 MODULE bloom,MODend_irq
 PUSHLR
 movei #AVSET+4,r0
 load (r0),r0
 cmpq #0,r0
 movei #bloom_done,r1
 jump eq,(r1)
 nop
 movei #POST_STATE,r15
 load (r15+60),r0
 addq #1,r0
 bset #0,r0
 store r0,(r15+60)
 moveq #0,r0
 store r0,(r15+16)
 store r0,(r15+20)
 movei #BLIT_A1_BASE,r14
.wait
 load (r14+$38),r0
 btst #0,r0
 jr eq,.wait
 nop
 movefa screen0.a,r16
 movei #BLOOM_GRID,r17
 moveq #0,r18
 moveq #0,r19
.sample_row
 moveq #0,r20
.sample_pixel
 ; Four actual scene samples per cell, prior to any bloom writes.
 move r19,r0
 shlq #3,r0
 addq #2,r0
 movei #1536,r1
 mult r1,r0
 move r20,r2
 shlq #5,r2
 addq #4,r2
 add r2,r0
 add r16,r0
 loadw (r0),r1
 addq #16,r0
 loadw (r0),r2
 movei #6128,r3
 add r3,r0
 loadw (r0),r3
 addq #16,r0
 loadw (r0),r4
 movei #255,r5
 and r5,r1
 and r5,r2
 and r5,r3
 and r5,r4
 add r2,r1
 add r3,r1
 add r4,r1
 shrq #2,r1
 store r1,(r17)
 addq #4,r17
 addq #1,r20
 movei #48,r0
 cmp r0,r20
 movei #.sample_pixel,r0
 jump ne,(r0)
 nop
 addq #1,r19
 moveq #25,r0
 cmp r0,r19
 movei #.sample_row,r0
 jump ne,(r0)
 nop
 moveq #0,r20
 movei #BLOOM_GRID,r18
 movei #BLOOM_TMP,r19
.filter_pass
 moveq #0,r17
.filter_cell
 movei #BLOOM_PROOF,r13
 cmpq #0,r20
 jr eq,.proof_horizontal
 nop
 addq #20,r13
.proof_horizontal
 move r17,r22
 movei #48,r0
 div r0,r22
 moveq #24,r23
 moveq #0,r0
 cmp r0,r20
 jr ne,.vertical
 movei #48,r21
 mult r21,r22
 move r17,r0
 sub r22,r0
 move r0,r22
 moveq #1,r21
 movei #47,r23
.vertical
 moveq #0,r12
 move r22,r0
 subq #2,r0
 cmpq #0,r0
 jr pl,.filter_0_min
 nop
 moveq #0,r0
.filter_0_min
 cmp r23,r0
 jr mi,.filter_0_max
 nop
 move r23,r0
.filter_0_max
 sub r22,r0
 imult r21,r0
 add r17,r0
 shlq #2,r0
 add r18,r0
 load (r0),r1
 movei #488,r0
 cmp r0,r17
 jr ne,.proof_0_skip
 nop
 store r1,(r13)
 addq #4,r13
.proof_0_skip
 add r1,r12
 move r22,r0
 subq #1,r0
 cmpq #0,r0
 jr pl,.filter_1_min
 nop
 moveq #0,r0
.filter_1_min
 cmp r23,r0
 jr mi,.filter_1_max
 nop
 move r23,r0
.filter_1_max
 sub r22,r0
 imult r21,r0
 add r17,r0
 shlq #2,r0
 add r18,r0
 load (r0),r1
 movei #488,r0
 cmp r0,r17
 jr ne,.proof_1_skip
 nop
 store r1,(r13)
 addq #4,r13
.proof_1_skip
 moveq #4,r2
 mult r2,r1
 add r1,r12
 move r22,r0
 nop
 cmpq #0,r0
 jr pl,.filter_2_min
 nop
 moveq #0,r0
.filter_2_min
 cmp r23,r0
 jr mi,.filter_2_max
 nop
 move r23,r0
.filter_2_max
 sub r22,r0
 imult r21,r0
 add r17,r0
 shlq #2,r0
 add r18,r0
 load (r0),r1
 movei #488,r0
 cmp r0,r17
 jr ne,.proof_2_skip
 nop
 store r1,(r13)
 addq #4,r13
.proof_2_skip
 moveq #6,r2
 mult r2,r1
 add r1,r12
 move r22,r0
 addq #1,r0
 cmpq #0,r0
 jr pl,.filter_3_min
 nop
 moveq #0,r0
.filter_3_min
 cmp r23,r0
 jr mi,.filter_3_max
 nop
 move r23,r0
.filter_3_max
 sub r22,r0
 imult r21,r0
 add r17,r0
 shlq #2,r0
 add r18,r0
 load (r0),r1
 movei #488,r0
 cmp r0,r17
 jr ne,.proof_3_skip
 nop
 store r1,(r13)
 addq #4,r13
.proof_3_skip
 moveq #4,r2
 mult r2,r1
 add r1,r12
 move r22,r0
 addq #2,r0
 cmpq #0,r0
 jr pl,.filter_4_min
 nop
 moveq #0,r0
.filter_4_min
 cmp r23,r0
 jr mi,.filter_4_max
 nop
 move r23,r0
.filter_4_max
 sub r22,r0
 imult r21,r0
 add r17,r0
 shlq #2,r0
 add r18,r0
 load (r0),r1
 movei #488,r0
 cmp r0,r17
 jr ne,.proof_4_skip
 nop
 store r1,(r13)
 addq #4,r13
.proof_4_skip
 add r1,r12
 shrq #4,r12
 move r17,r0
 shlq #2,r0
 add r19,r0
 store r12,(r0)
 movei #488,r0
 cmp r0,r17
 jr ne,.proof_filter_skip
 nop
 move r20,r0
 shlq #2,r0
 movei #POST_STATE+28,r1
 add r0,r1
 store r12,(r1)
.proof_filter_skip
 addq #1,r17
 movei #1200,r0
 cmp r0,r17
 movei #.filter_cell,r0
 jump ne,(r0)
 nop
 cmpq #0,r20
 jr ne,.filter_done
 nop
 moveq #1,r20
 movei #BLOOM_TMP,r18
 movei #BLOOM_OUT,r19
 movei #.filter_pass,r0
 jump (r0)
 nop
.filter_done
 movei #BLIT_A1_BASE,r14
 movei #BLIT_PITCH2|BLIT_PIXEL16|BLIT_WID384|BLIT_XADDPIX,r0
 store r0,(r14+_BLIT_A1_FLAGS)
 movei #BLIT_PITCH1|BLIT_PIXEL16|BLIT_WID8|BLIT_XADD0,r0
 store r0,(r14+_BLIT_A2_FLAGS)
 store r16,(r14)
 movei #$0001fff8,r0
 store r0,(r14+_BLIT_A1_STEP)
 moveq #0,r0
 store r0,(r14+_BLIT_A1_FSTEP)
 store r0,(r14+_BLIT_A1_FPIXEL)
 store r0,(r14+_BLIT_A2_PIXEL)
 movei #BLOOM_OUT,r17
 moveq #0,r19
.tile_row
 moveq #0,r20
.tile
 load (r17),r18
 ; Stable actual TOM pixel proof at grid (8,10), screen (68,84).
 movei #10,r0
 cmp r0,r19
 jr ne,.proof_tile_skip
 nop
 cmpq #8,r20
 jr ne,.proof_tile_skip
 nop
 movei #129296,r0
 add r16,r0
 store r0,(r15+48)
 loadw (r0),r0
 store r0,(r15+40)
.proof_tile_skip
 movei #102,r0
 mult r0,r18
 shrq #8,r18
 movei #10,r0
 cmp r0,r19
 jr ne,.proof_add_skip
 nop
 cmpq #8,r20
 jr ne,.proof_add_skip
 nop
 store r18,(r15+36)
.proof_add_skip
 cmpq #0,r18
 movei #.next_tile,r0
 jump eq,(r0)
 nop
 load (r15+16),r0
 addq #1,r0
 store r0,(r15+16)
 move r18,r0
 shlq #16,r0
 or r18,r0
 store r0,(r14+_BLIT_SRCD)
 store r0,(r14+_BLIT_SRCD+4)
 move r19,r0
 shlq #19,r0
 move r20,r1
 shlq #3,r1
 or r1,r0
 move r0,r21
 moveq #2,r22
.tile_pass
 store r21,(r14+_BLIT_A1_PIXEL)
 movei #8<<16|8,r0
 store r0,(r14+_BLIT_COUNT)
 movei #BLIT_DSTEN|BLIT_ADDDSEL|BLIT_UPDA1,r0
 store r0,(r14+_BLIT_CMD)
.wait_tile
 load (r14+$38),r0
 btst #0,r0
 jr eq,.wait_tile
 nop
 load (r15+20),r0
 addq #1,r0
 store r0,(r15+20)
 subq #1,r22
 movei #.tile_pass,r0
 jump ne,(r0)
 nop
.next_tile
 movei #10,r0
 cmp r0,r19
 jr ne,.proof_after_skip
 nop
 cmpq #8,r20
 jr ne,.proof_after_skip
 nop
 load (r15+48),r0
 loadw (r0),r0
 store r0,(r15+44)
 movei #BLOOM_GRID+488*4,r0
 load (r0),r0
 store r0,(r15+24)
.proof_after_skip
 addq #4,r17
 addq #1,r20
 movei #48,r0
 cmp r0,r20
 movei #.tile,r0
 jump ne,(r0)
 nop
 addq #1,r19
 moveq #25,r0
 cmp r0,r19
 movei #.tile_row,r0
 jump ne,(r0)
 nop
 load (r15+60),r0
 addq #1,r0
 bclr #0,r0
 store r0,(r15+60)
bloom_done:
 POPLR
 align 8
 ENDMODULE bloom

	include "bitmap_hud.js"
	include "frontend.js"
	include "frontdraw.js"
	include "recording.js"
 IF LANDSCAPE <> 0
	include	"plane_prep.js"
 ENDIF

	align	4
skip_modules


	movei	#$f02100,IRQ_FLAGADDR
	moveta	IRQ_FLAGADDR,IRQ_FLAGADDR.a

	movei	#1<<14|%11111<<9,r0	; clear all ints, REGPAGE = 1
	store	r0,(IRQ_FLAGADDR)
	nop
	nop

patch_fps		equ _patch_fps-MODrun_irq+MODstart_irq

	movei	#$00F14003,r0
	loadb	(r0),r0
	movei	#patch_fps,r1
	btst	#4,r0
	loadw	(r1),r0
	jr	eq,.no_fps_fix
	addq	#32,r0		; increase "MOVEQ"
	storew	r0,(r1)
.no_fps_fix:

	INITMODULE irq

	movei	#IRQ_STACK,IRQ_SP
	moveta	IRQ_SP,IRQ_SP.a
	movei	#stacktop,SP

	movei	#memzero,r4
	movei	#$180,r0
	movei	#start-$120,r1
	BL	(r4)

	movei	#memzero,r4
	movei	#ende,r0
	movei	#$200000-ende,r1
	BL	(r4)

;;; ------------------------------
	include <js/inc/videoinit.inc>
;;; ------------------------------
;;; patch aspect ration for different resolutions
;;; in case of NTSC mode
;;;

 IF NO_ASPECT_FIX = 0
patch_aspect	equ _fix_ntsc_aspect-MODrun_engine+MODstart_engine
patch_aspect2	equ _fix_ntsc_aspect-MODrun_engine+MODstart_engine

	movei	#20*50,r4
	movei	#$00F14003,r0
	loadb	(r0),r0
	movei	#patch_aspect,r1
	btst	#4,r0
	movei	#patch_aspect2,r2
	jr	eq,.patch_pal
	nop
	movei	#16*60,r4
	addq	#10,r4
 IF max_x = 640
	movei	#aspect_patch_ntsc,r0
	addq	#2,r1
	addq	#2,r2
	storew	r0,(r1)
	storew	r0,(r2)
 else
	movei	#(35<<10)|aspect_patch_ntsc<<5|2,r0 ; moveq #n,r2
	storew	r0,(r1)
	storew	r0,(r2)
 endif

.patch_pal
	movei	#IS_PAL,r3
	store	r4,(r3)
;;->	echo "aspect2: %Hpatch_aspect"
;;->	echo "aspect2: %Hpatch_aspect2"
 ENDIF
;;; ------------------------------

	movei	#$f00028,r0
	movei	#VID_MODE,r1
	storew	r1,(r0)

	movei	#$ffcf,r0
	movei	#$f00400,r1
	store	r0,(r1)
;;; ------------------------------
	movei	#logo_screen,r0
	movei	#logo,r1
	movei	#8*10/4,r2
cpy_logo:
	load	(r1),r3
	addq	#4,r1
	subq	#1,r2
	store	r3,(r0)
	jr	nz,cpy_logo
	addq	#4,r0

;;; ------------------------------
 IF  MOD = 1
	movei	#DSP_start,r0
	movei	#DSP_RAM,r1
	movei	#(DSP_end-DSP_start),r2
	nop
cpy_dsp:
	load	(r0),r3
	addq	#4,r0
	subq	#4,r2
	store	r3,(r1)
	jr	pl,cpy_dsp
	addq	#4,r1

	movei	#DSP_flag_replay_ON_OFF,r14
	movei	#song,r0
	store	r0,(r14+16)
	movei	#$120,r0
	store	r0,(r14+12)
	movei	#binPrecalcTable,r0
	store	r0,(r14+8)
	movei	#panning_table,r0
	store	r0,(r14+4)
	moveq	#0,r0
	store	r0,(r14)
 ENDIF
;;; ------------------------------

	movei	#254,r0
	movei	#$000088ff,r1
	movei	#TxtScreen,r2
	movei	#ASCII,r3
	movei	#InitTxtScreen,r4
	BL	(r4)

	movei	#PrintString_YX,r5
	movei	#info,r0
	moveq	#3,r1
	shlq	#16,r1
	BL	(r5)

	movei	#PrintString_YX,r5
	movei	#Hallo,r0
	moveq	#0,r1
	BL	(r5)

	movei	#ms,r0
	moveq	#2,r1
	shlq	#16,r1
	BL	(r5)

	movei	#screen0,r1
	moveta	r1,screen1.a
	movei	#screen1,r1
	moveta	r1,screen0.a

	movei	#$f14003,r0
	loadb	(r0),r0
	nop
	movei	#obl0,r10
	btst	#4,r0
	movei	#obl1,r11
	jr	eq,pal
	nop
	movei	#obl0_60hz,r10
	movei	#obl1_60hz,r11
pal:
	move	r10,r1
	addq	#32,r1
	addq	#32,r1
	moveta	r1,obl0.a
	addq	#32,r11
	addq	#32,r11
	moveta	r11,obl1.a

	moveq	#op_list>>8,r1
	shlq	#8,r1
	moveq	#31,r2
	shlq	#2,r2
	nop
.cpyobl:
	load	(r10),r3
	addqt	#4,r10
	subq	#1,r2
	store	r3,(r1)
	jr	pl,.cpyobl
	addqt	#4,r1

	movei	#$f00020,r0
	moveq	#op_list>>8,r1
	shlq	#16+8,r1
	store	r1,(r0)

	movei	#1<<14|%11111<<9|%01000<<4,r1
	store	r1,(IRQ_FLAGADDR)
	nop
	nop

 IF MOD = 1
	moveq	#0,r0
	bset	#14,r0
	movei	#$f1a100,r14
	store	r0,(r14)
	movei	#$f1b000,r0
	store	r0,(r14+$10)	; PC
	moveq	#1,r0
	store	r0,(r14+$14)	; GO
 ENDIF

	movei	#CAMERA_X,r15
	movei	#CAM_X,r0
	store	r0,(r15)			; camera x
	movei	#CAM_Y,r0
	store	r0,(r15+CAMERA_Y-CAMERA_X)	; camera y
	movei	#CAM_Z,r0
	store	r0,(r15+CAMERA_Z-CAMERA_X)	; camera z
	movei	#CAM_ANGLE*4,r0
	store	r0,(r15+CAMERA_ANGLE_Y-CAMERA_X); camera angle

	movei	#225,r0
	movei	#-68,r1
	movei	#-101,r2
	store	r0,(r15+LIGHT_X-CAMERA_X)
	store	r1,(r15+LIGHT_Y-CAMERA_X)
	store	r2,(r15+LIGHT_Z-CAMERA_X)

	movei	#USE_GOURAUD,r0
	moveq	#0,r1
	not	r1
	store	r1,(r0)
	addq	#4,r0
	moveq	#0,r1
	store	r1,(r0)

 IF LANDSCAPE <> 0
	MyINITMODULE planePrep
	MBL	planePrep
 ENDIF

	movei	#VID_PIT0,tmp1
	movei	#(26591-1)<<16|0,tmp0
	store	tmp0,(tmp1)

; Load native DSP mixer after RAM initialization.
 movei #pcm_code,r0
 movei #$f1b000,r1
 movei #(pcm_end-pcm_code)/4,r2
.pcmcopy
 load (r0),r3
 store r3,(r1)
 addq #4,r0
 addq #4,r1
 subq #1,r2
 jr ne,.pcmcopy
 nop
 movei #$f1a100,r14
 movei #$3e00,r0
 store r0,(r14)
 movei #$f1b000,r0
 store r0,(r14+16)
 moveq #1,r0
 store r0,(r14+20)
	moveq	#FPS-1,r0
	moveta	r0,vbl_counter.a

//->	moveq	#8,r0
//->	movei	#$0e00008,r1
//->	store 	r0,(r1)
//->	addq	#4,r1
//->	movei	#sea_tex_0,r0
//->	store	r0,(

****************
* main loop
main_loop:
//->	movei	#drawHex,r8
//->	movefa	screen0.a,r7
//->	movefa	vbl_counter.a,r0
//->	BL	(r8)

	movei	#$00F00058,r1
	moveq	#31,r0
	storew	r0,(r1)

	movei	#$00F00052,r2
	loadw	(r2),r0		; work time
	PUSH	r0

	moveq	#0,r0
	moveta	r0,VBLFlag.a
.wvbl:
	cmpq	#0,r0
	jr	eq,.wvbl
	movefa	VBLFlag.a,r0

	loadw	(r2),r0		; total frame time
	PUSH	r0

	moveq	#0,r1
	subq	#1,r1
	storew	r1,(r2)

	MyINITMODULE frontend
	MBL frontend
	MyINITMODULE recording
	MBL recording
	MyINITMODULE control
	MBL control
	MyINITMODULE handling
	MBL handling
	MyINITMODULE pose
	MBL pose
	MyINITMODULE view
	MBL view
	MyINITMODULE skybank
	MBL skybank
	MyINITMODULE engine
	MBL	engine
	MyINITMODULE postfx
	MBL postfx
	MyINITMODULE effects
	MBL effects
	MyINITMODULE bloom
	MBL bloom
	MyINITMODULE presentation
	MBL presentation
	MyINITMODULE frontdraw
	MBL frontdraw
	MyINITMODULE bitmap_hud
	MBL bitmap_hud

//->	movei	#$00F00052,r0
//->	loadw	(r0),r0
//->	neg	r0
//->	shlq	#16,r0
//->	shrq	#16,r0
//->	PUSH	r0



	POP r1
	POP r0
	movei	#main_loop,r0
	jump	(r0)
	nop

	include <js/inc/txtscr.inc>

printString::
	movei	#$e00004,r1
.loop
	loadb	(r0),r2
	cmpq	#0,r2
	addqt	#1,r0
	jump	eq,(LR)
	nop
	jr	.loop
	store	r2,(r1)

printHex::
	moveq	#$e,r1
	shlq	#20,r1
	jump	(LR)
	store	r0,(r1)

dumpMem:
	movei	#$e0000c,r1
	jump	(LR)
	store	r0,(r1)

****************
	align 4
txt_ptr	reg 7
minihex_screen_width	equ max_x
	include <js/inc/minihex.inc>
	unreg txt_ptr

;-----------------------------------------
;- Copy overlay routine
;-----------------------------------------
blitter		reg 14

	align 4
overlay::
	movei	#BLIT_A1_BASE,blitter
	nop
.wbl
	load (blitter+_BLIT_CMD),r3
	shrq #1,r3
	jr cc,.wbl
	nop

	store r0,(blitter)
	store r1,(blitter+_BLIT_A2_BASE)
	movei #BLIT_PITCH1|BLIT_PIXEL32|BLIT_WID3584|BLIT_XADDPHR,r0
	moveq #0,r1
	store r0,(blitter+_BLIT_A1_FLAGS)
	store r0,(blitter+_BLIT_A2_FLAGS)
	store r1,(blitter+_BLIT_A1_PIXEL)
	store r1,(blitter+_BLIT_A2_PIXEL)

	movei #BLIT_SRCEN|BLIT_LFU_REPLACE|BLIT_BUSHI,r1
	store r2,(blitter+_BLIT_COUNT)
	store r1,(blitter+_BLIT_CMD)

.wbl2
	shrq #1,r1
	jr cc,.wbl2
	load (blitter+_BLIT_CMD),r1
	jump	(LR)
	nop

	unreg	blitter

******************
* text-data
Hallo:		DC.B "HEXGL   CITYSCAPE   /   ATARI JAGUAR",0
ms:		DC.B "A/UP THRUST  B BRAKE  LEFT/RIGHT STEER",0
info:		dc.b "OPTION RESTART   PAUSE   C AUTOPILOT",0
	EVEN

	align 8
obl0:
	.ibytes "obl0_50.bin"
obl1:
	.ibytes "obl1_50.bin"

obl0_60hz:
	.ibytes "obl0_60.bin"

obl1_60hz:
	.ibytes "obl1_60.bin"

	align 4
logo:
	dc.l 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

	align 4
ASCII::
	.ibytes <font/light8x8.fnt>

	.align 8
	include <js/inc/memzero.inc>
	include <js/inc/memset.inc>
	include <js/inc/memcpy.inc>
world_list:
	include "../assets/model_list.inc"
	include "../assets/models.inc"
	include "sintab.inc"
 IF LANDSCAPE = 10
	include "plane2_new.inc"
 ENDIF
 IF LANDSCAPE = 1
	include "plane2.inc"
 ENDIF

 IF LANDSCAPE <> 0
	dphrase
obj_plane:
	dc.w	0		; visible
	dc.w	0,0,0		; position: x,y,z
	dc.w	0		; spare
	dc.w	0,0,0		; angle: a,b,c
	dc.l	0		; plane_points
	dc.l	plane_faces
	dc.l	plane_normals
	dc.l	plane_vnormals
	dc.l	plane_rotated
	dc.l	plane_normals_rotated
	dc.l	plane_vnormals_rotated
	dc.l	plane_projected
	dc.l	plane_visible

 IF TEXTURE <> 0
	.long
sea_tex_0:
	tex_info_shifted 1, 0,0,63,0,63,63
sea_tex_1:
	tex_info_shifted 1, 0,0,63,63,0,63

sea2_tex_0:
	tex_info_shifted 5, 0,0,63,0,63,63
sea2_tex_1:
	tex_info_shifted 5, 0,0,63,63,0,63

grass_tex_0:
	tex_info_shifted 3, 0,0,63,0,63,63
grass_tex_1:
	tex_info_shifted 3, 0,0,63,63,0,63
 ENDIF
 ENDIF
	align	8
texture:

	include "../assets/textures.inc"
	include "../assets/hud.inc"
	include "../assets/frontend.inc"
 align 4
effect_atlas:
 incbin "../assets/effects.bin"
 align 4
color_decode:
 incbin "../assets/color-decode.bin"
color_encode:
 incbin "../assets/color-encode.bin"
	IF MOD = 1
	align 8
DSP_start:
	ibytes "hively_player.bin"
DSP_end:
	align 8
song:
 if chip = 1
        .incbin "mod/chiprolled.hvl.streambits"
 endif
 if gone = 1
        .incbin "mod/gone.ahx.streambits"
 endif
     if galactic = 1
	.incbin "mod/galactic_emeralds.hvl.streambits"
     endif
	.long
binPrecalcTable:
	ibytes "AHX_FilterPrecalc.bin"
	.long
panning_table:
	ibytes "AHX_panning.bin"
	ENDIF

 IF 0
	echo "plane y:  %Hplane_y"
	echo "plane col:%Hplane_col"
	echo "plane n:  %Hplane_normals"
	echo "plane n#: %Dnnormals"
	echo "plane v:  %Hplane_vnormals"
	echo "plane pro:%Xplane_projected"
	echo "plane fcs:%Xplane_faces"
 ENDIF

	align 8
pcm_code:
	incbin "audio.bin"
pcm_end:
	align	32
ende:		equ *
	echo "ENDE : %Hende"

motion_ship_address:: EQU obj_ship
motion_booster_address:: EQU obj_booster
motion_camera_address:: EQU CAMERA_X
	end
