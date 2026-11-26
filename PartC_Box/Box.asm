// Box.asm  -  K = 57
// Box starts at row 57, 20 rows tall, 32 pixels (2 words) wide, left edge.
// Key pressed -> black box; key released -> box cleared.
// First word address = SCREEN + 32*57 = 16384 + 1824 = 18208

(LOOP)
    @KBD
    D=M
    @PRESSED
    D;JNE           // key down -> colour = -1
    @color
    M=0             // no key -> white
    @DRAW
    0;JMP
(PRESSED)
    @color
    M=-1            // black
(DRAW)
    @1824           // 32*57
    D=A
    @SCREEN
    D=D+A
    @addr
    M=D             // addr = first word of row 57
    @20
    D=A
    @rows
    M=D             // 20 rows to draw
(ROW)
    @color
    D=M
    @addr
    A=M
    M=D             // left word  (pixels 0-15)
    A=A+1
    M=D             // right word (pixels 16-31)
    @32
    D=A
    @addr
    M=D+M           // next row
    @rows
    MD=M-1
    @ROW
    D;JGT
    @LOOP
    0;JMP
