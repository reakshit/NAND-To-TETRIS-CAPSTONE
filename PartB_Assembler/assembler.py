"""Hack assembler (Nand to Tetris) - K=57 -> extra feature: symbols.txt
Usage: python assembler.py Prog.asm      -> Prog.hack + symbols.txt
"""
import sys, os

COMP = {
 '0':'0101010','1':'0111111','-1':'0111010','D':'0001100','A':'0110000',
 '!D':'0001101','!A':'0110001','-D':'0001111','-A':'0110011','D+1':'0011111',
 'A+1':'0110111','D-1':'0001110','A-1':'0110010','D+A':'0000010','D-A':'0010011',
 'A-D':'0000111','D&A':'0000000','D|A':'0010101',
 'M':'1110000','!M':'1110001','-M':'1110011','M+1':'1110111','M-1':'1110010',
 'D+M':'1000010','D-M':'1010011','M-D':'1000111','D&M':'1000000','D|M':'1010101'}
DEST = {'':'000','M':'001','D':'010','MD':'011','A':'100','AM':'101','AD':'110','AMD':'111'}
JUMP = {'':'000','JGT':'001','JEQ':'010','JGE':'011','JLT':'100','JNE':'101','JLE':'110','JMP':'111'}

def predefined():
    t = {'SP':0,'LCL':1,'ARG':2,'THIS':3,'THAT':4,'SCREEN':16384,'KBD':24576}
    for i in range(16): t['R%d' % i] = i
    return t

def clean(line):
    return line.split('//')[0].replace(' ', '').replace('\t', '').strip()

def assemble(src):
    symbols = predefined()
    lines = []                      # (source line number, instruction)
    # ---- first pass: labels ----
    rom = 0
    for n, raw in enumerate(src, 1):
        s = clean(raw)
        if not s: continue
        if s.startswith('('):
            name = s[1:-1]
            symbols[name] = rom     # label = address of next instruction
        else:
            lines.append((n, s)); rom += 1
    # ---- second pass: translate ----
    out, nxt = [], 16
    for n, s in lines:
        if s[0] == '@':
            v = s[1:]
            if v.isdigit(): addr = int(v)
            else:
                if v not in symbols:
                    symbols[v] = nxt; nxt += 1   # new variable
                addr = symbols[v]
            out.append(format(addr, '016b'))
        else:
            dest, comp, jump = '', s, ''
            if '=' in comp: dest, comp = comp.split('=', 1)
            if ';' in comp: comp, jump = comp.split(';', 1)
            out.append('111' + COMP[comp] + DEST[dest] + JUMP[jump])
    return out, symbols

def main():
    if len(sys.argv) != 2:
        sys.exit('Usage: python assembler.py Prog.asm')
    path = sys.argv[1]
    with open(path) as f: src = f.read().splitlines()
    out, symbols = assemble(src)
    base = os.path.splitext(path)[0]
    with open(base + '.hack', 'w') as f: f.write('\n'.join(out) + '\n')
    # extra feature (K mod 3 == 0): save labels & variables with addresses
    pre = predefined()
    with open(os.path.join(os.path.dirname(path) or '.', 'symbols.txt'), 'w') as f:
        for name, a in symbols.items():
            if name not in pre: f.write('%s = %d\n' % (name, a))
    print('Wrote %s.hack (%d instructions) and symbols.txt' % (base, len(out)))

if __name__ == '__main__':
    main()
