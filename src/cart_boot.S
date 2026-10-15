/* 68000 direct-cartridge entry for emulators with BIOS disabled.
 * Retail BIOS still uses the unchanged encrypted GPU loader at ROM offset 0.
 * Linked at $900000 in otherwise unused ROM. No emulator-specific RAM patches.
 */
    .text
    .global _start
_start:
    move.w #0x2700,%sr
    move.l #0x200000,%sp
    moveq #0,%d0
    move.l %d0,0xf02114
    move.l %d0,0xf1a114
    move.l #0x23e00,0xf1a100
    move.l #0x7e00,0xf02100
    move.w #0,0xf0004e
    move.l #4,4
    move.l %d0,0xf00020
    /* Same 68K interrupt-acknowledgement loop as the retail GPU loader. */
    lea irq_stub(%pc),%a0
    lea 0x110,%a1
    moveq #((irq_end-irq_stub)/2)-1,%d0
1:  move.w (%a0)+,(%a1)+
    dbra %d0,1b
    move.l #0x110,0x100
    /* BS94 payload: destination and length follow signature at $80040c. */
    lea 0x800410,%a0
    movea.l (%a0)+,%a1
    move.l (%a0)+,%d0
    move.l %a1,%d1
2:  move.l (%a0)+,(%a1)+
    subq.l #4,%d0
    bne.s 2b
    move.l %d1,0xf02110
    move.l #1,0xf02114
    jmp 0x110
    .balign 4
irq_stub:
    lea 0xf000e0,%a0
3:  move.w 2(%a0),%d0
    lsl.w #8,%d0
    swap %d0
    move.l %d0,(%a0)
    stop #0x2000
    bra.s 3b
irq_end:
