; Native pose, camera and text presentation, separate GPU overlay.
 MODULE pose,MODend_irq
 PUSHLR
 movei #GAME,r14
 load (r14+112),r19
 load (r14+4),r0
 cmpq #0,r0
 jr ne,.ready
 nop
 movei #motion_reset,r0
 BL (r0)
.ready
pose_camera:
 movei #motion_update,r0
 BL (r0)
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
 addq #4,r0
 movei #PHYS+24,r2
 load (r2),r2
 sharq #8,r2
 movei #2044,r3
 and r3,r2
 storew r2,(r0)
 addq #2,r0
 storew r18,(r0)
 addq #2,r0
 movei #MOTION,r15
 load (r15),r1
 sharq #8,r1
 movei #2044,r2
 and r2,r1
 storew r1,(r0)
 movei #obj_booster+2,r0
 storew r21,(r0)
 addq #2,r0
 storew r24,(r0)
 addq #2,r0
 storew r22,(r0)
 addq #4,r0
 movei #PHYS+24,r2
 load (r2),r2
 sharq #8,r2
 movei #2044,r3
 and r3,r2
 storew r2,(r0)
 addq #2,r0
 storew r18,(r0)
 addq #2,r0
 storew r1,(r0)
 ; Native telemetry records the angles actually written to both objects.
 move r1,r2
 shlq #16,r2
 or r1,r2
 store r2,(r15+60)
 movei #SinTab,r15
 load (r15+r23),r0
 move r0,r1
 shrq #16,r1
 movei #MOTION+4,r2
 load (r2),r2
 shrq #8,r2
 movei #160,r3
 add r3,r2
 movei #MOTION,r15
 store r2,(r15+44)
 imult r2,r0
 imult r2,r1
 sharq #15,r0
 sharq #15,r1
 add r0,r21
 sub r1,r22
 load (r15+8),r24
 sharq #8,r24
 store r21,(r15+48)
 store r24,(r15+52)
 store r22,(r15+56)
 movei #CAMERA_X,r15
 store r21,(r15)
 store r24,(r15+4)
 store r22,(r15+8)
 store r23,(r15+12)
 ; Look toward a point 40 native units ahead, rather than a horizontal camera.
 movei #pose_pitch,r0
 BL (r0)
 movei #MOTION+64,r0
 load (r0),r1
 addq #1,r1
 store r1,(r0)
 ; HUD routines use the DRAM backing strings, never GPU-local LOADB.
 movei #draw_race_hud,r0
 BL (r0)
 POPLR


pose_pitch:
 PUSHLR
 movei #GAME,r14
 load (r14+8),r0
 cmpq #1,r0
 movei #.done,r1
 jump ne,(r1)
 nop
 load (r14+52),r0
 cmpq #0,r0
 movei #.done,r1
 jump ne,(r1)
 nop
 movei #MOTION,r15
 load (r15+52),r0
 load (r14+20),r1
 sharq #8,r1
 sub r1,r0
 shlq #8,r0
 load (r15+44),r1
 movei #40,r2
 add r2,r1
 div r1,r0
 movei #128,r1
 cmp r1,r0
 jr cs,.angle
 nop
 move r1,r0
.angle
 shlq #2,r0
 movei #atan_slope-MODrun_control+MODstart_control,r1
 add r0,r1
 load (r1),r0
 movei #PHYS,r15
 store r0,(r15+52)
 load (r15+48),r1
 movei #MOTION+40,r2
 load (r2),r2
 movei #smooth_component,r3
 BL (r3)
 store r0,(r15+48)
.done
 POPLR

 include "motion.inc"
 include "race_hud.inc"
 align 8
 ENDMODULE pose
