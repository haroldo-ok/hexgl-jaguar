; Center-sampled perspective depth query against the ACTUAL submitted triangles.
; r0/r1 screen center, r2 camera Z; return r0=1 if occluded, else 0.
; Conservative: skip near-plane/oversized polygons, source transparent booster,
; and the ship itself. Sprite edges are not individually depth tested.
fx_occluded:
 PUSHLR
 movei #FX_DEPTH,r15
 store r0,(r15)
 store r1,(r15+4)
 store r2,(r15+8)
 movei #tri_ptrs_ram,r19
.bucket
 load (r19),r17
.triangle
 cmpq #0,r17
 movei #.nextbucket,r0
 jump eq,(r0)
 nop
 load (r15+48),r0
 addq #1,r0
 store r0,(r15+48)
 move r17,r0
 addq #20,r0
 load (r0),r0
 loadw (r0),r0
 cmpq #2,r0
 movei #.next,r13
 jump cs,(r13)
 nop
 move r17,r3
 addq #8,r3
 load (r3),r0
 addq #4,r3
 load (r3),r1
 addq #4,r3
 load (r3),r2
 move r0,r4
 move r1,r6
 move r2,r8
 sharq #16,r4
 sharq #16,r6
 sharq #16,r8
 shlq #16,r0
 shlq #16,r1
 shlq #16,r2
 sharq #16,r0
 sharq #16,r1
 sharq #16,r2
 move r0,r5
 move r1,r7
 move r2,r9
 ; Reject extreme projections before signed-16 multiplier arithmetic.
 movei #2048,r12
 move r4,r0
 abs r0
 cmp r12,r0
 jump cc,(r13)
 nop
 move r5,r0
 abs r0
 cmp r12,r0
 jump cc,(r13)
 nop
 move r6,r0
 abs r0
 cmp r12,r0
 jump cc,(r13)
 nop
 move r7,r0
 abs r0
 cmp r12,r0
 jump cc,(r13)
 nop
 move r8,r0
 abs r0
 cmp r12,r0
 jump cc,(r13)
 nop
 move r9,r0
 abs r0
 cmp r12,r0
 jump cc,(r13)
 nop
 load (r15),r10
 load (r15+4),r11
 sub r10,r4
 sub r10,r6
 sub r10,r8
 sub r11,r5
 sub r11,r7
 sub r11,r9
 ; Three signed barycentric numerators, orientation-independent.
 move r6,r0
 imult r9,r0
 move r7,r3
 imult r8,r3
 sub r3,r0
 move r8,r1
 imult r5,r1
 move r9,r3
 imult r4,r3
 sub r3,r1
 move r4,r2
 imult r7,r2
 move r5,r3
 imult r6,r3
 sub r3,r2
 move r0,r3
 add r1,r3
 add r2,r3
 cmpq #0,r3
 jump eq,(r13)
 nop
 jr pl,.orientation
 nop
 neg r0
 neg r1
 neg r2
 neg r3
.orientation
 cmpq #0,r0
 jump mi,(r13)
 nop
 cmpq #0,r1
 jump mi,(r13)
 nop
 cmpq #0,r2
 jump mi,(r13)
 nop
 movei #16384,r4
.reduce
 cmp r4,r3
 jr cs,.weights
 nop
 shrq #1,r0
 shrq #1,r1
 shrq #1,r2
 shrq #1,r3
 jr .reduce
 nop
.weights
 store r0,(r15+20)
 store r1,(r15+24)
 store r2,(r15+28)
 store r3,(r15+32)
 move r17,r12
 movei #tri_array_ram+4,r0
 sub r0,r12
 shrq #1,r12 ; 24-byte draw records map to 12-byte vertex-Z records
 movei #TRI_DEPTH,r0
 add r0,r12
 moveq #0,r10
 moveq #20,r11
.zloop
 load (r12),r4
 cmpq #10,r4
 jump mi,(r13)
 nop
 jump eq,(r13)
 nop
 movei #32768,r0
 div r4,r0
 load (r15+r11),r4
 mult r0,r4
 add r4,r10
 addq #4,r12
 addq #4,r11
 moveq #20,r0
 addq #12,r0
 cmp r0,r11
 movei #.zloop,r0
 jump ne,(r0)
 nop
 load (r15+32),r3
 div r3,r10
 cmpq #0,r10
 jump eq,(r13)
 nop
 movei #32768,r0
 div r10,r0
 store r0,(r15+44)
 ; Publish one actual inside-triangle reciprocal-depth calculation (seqlocked).
 load (r15+124),r3
 addq #1,r3
 store r3,(r15+124)
 load (r15),r4
 store r4,(r15+64)
 load (r15+4),r4
 store r4,(r15+68)
 load (r15+8),r4
 store r4,(r15+72)
 store r0,(r15+76)
 move r17,r4
 addq #8,r4
 load (r4),r5
 store r5,(r15+80)
 addq #4,r4
 load (r4),r5
 store r5,(r15+84)
 addq #4,r4
 load (r4),r5
 store r5,(r15+88)
 subq #12,r12
 load (r12),r5
 store r5,(r15+92)
 addq #4,r12
 load (r12),r5
 store r5,(r15+96)
 addq #4,r12
 load (r12),r5
 store r5,(r15+100)
 load (r15+20),r4
 store r4,(r15+104)
 load (r15+24),r4
 store r4,(r15+108)
 load (r15+28),r4
 store r4,(r15+112)
 load (r15+32),r4
 store r4,(r15+116)
 store r17,(r15+120)
 addq #1,r3
 store r3,(r15+124)
 addq #8,r0 ; conservative bias for finite fixed-point barycentrics
 load (r15+8),r1
 cmp r0,r1
 jump cs,(r13)
 nop
 jump eq,(r13)
 nop
 load (r15+52),r0
 addq #1,r0
 store r0,(r15+52)
 store r17,(r15+56)
 moveq #1,r0
 POPLR
.next
 load (r17),r17
 movei #.triangle,r0
 jump (r0)
 nop
.nextbucket
 addq #4,r19
 movei #tri_ptrs_ram+4096,r0
 cmp r0,r19
 movei #.bucket,r0
 jump ne,(r0)
 nop
 moveq #0,r0
 POPLR
