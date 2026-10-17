; Real RGB-domain alpha/additive composition; CrY chroma is NEVER summed.
; r0 source CrY, r1 destination CrY, r2 alpha 0..256, r3 0=over / 1=add.
; Returns r0 native CrY; scratch r1..r13. RGB555 quantization is explicit.
blend_rgb:
 moveq #0,r9
 moveq #0,r12
 movei #255,r8
 move r0,r6
 move r1,r7
 and r8,r6
 and r8,r7
 shrq #8,r0
 shrq #8,r1
 and r8,r0 ; source word also carries sprite alpha in its high half
 and r8,r1
 shlq #2,r0
 shlq #2,r1
 movei #color_decode,r4
 add r4,r0
 add r4,r1
 load (r0),r4
 load (r1),r5
.channel
 move r4,r10
 move r5,r11
 and r8,r10
 and r8,r11
 mult r6,r10
 mult r7,r11
 shrq #8,r10
 shrq #8,r11
 mult r2,r10
 cmpq #0,r3
 jr ne,.additive
 nop
 movei #256,r0
 sub r2,r0
 mult r0,r11
 add r11,r10
 shrq #8,r10
 jr .quantize
 nop
.additive
 shrq #8,r10
 add r11,r10
 sat8 r10
.quantize
 shrq #3,r10
 move r12,r13
 neg r13
 sh r13,r10
 or r10,r9
 shrq #8,r4
 shrq #8,r5
 addq #5,r12
 cmpq #15,r12
 movei #.channel,r0
 jump ne,(r0)
 nop
 shlq #1,r9
 movei #color_encode,r0
 add r9,r0
 loadw (r0),r0
 jump (LR)
 nop
