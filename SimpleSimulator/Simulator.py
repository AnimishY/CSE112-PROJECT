import sys
from B2C import comp
from TP import RtoConsole, ItoConsole, StoConsole, BtoConsole, UtoConsole

# Define memory as a dictionary
memory = []

outputfile = sys.argv[2]
file=open(outputfile, "w")

def add(reg1, reg2, reg3):
    reg1 = reg2 + reg3
    if reg1 > 65536:
        reg1 = reg1 % 65535
    return reg1

def lw(reg1, reg2, imm):
    address = reg2 + (imm & 0xFFF)
    if address in memory:
        reg1 = memory[address]
    else:
        reg1 = 0
    return reg1

def sw(reg1, reg2, imm):
    address = reg2 + (imm & 0xFFF)
    memory[address] = reg1


def sub(reg1, reg2, reg3):
    reg1 = reg2 - reg3
    if reg1 < 0:
        reg1 = reg1 + 65535
    return reg1

def sll(reg1, reg2, reg3):
    reg1 = reg2 << reg3
    return reg1

def slt(reg1, reg2, reg3):
    if reg2 < reg3:
        reg1 = 1
    else:
        reg1 = 0
    return reg1

def sltu(reg1, reg2, reg3):
    if reg2 < reg3:
        reg1 = 1
    else:
        reg1 = 0
    return reg1

def xor(reg1, reg2, reg3):
    reg1 = reg2 ^ reg3
    return reg1

def srl(reg1, reg2, reg3):
    reg1 = reg2 >> reg3
    return reg1

def or_(reg1, reg2, reg3):
    reg1 = reg2 | reg3
    return reg1

def and_(reg1, reg2, reg3):
    reg1 = reg2 & reg3
    return reg1

def lw(reg1, reg2, imm):
    reg1 = reg2 + (imm & 0xFFF)
    return reg1

def sext(imm):
    if imm & (1 << 11):
        return imm | (0xFFFFF000 & (1 << 11))
    else:
        return imm

def addi(reg1, reg2, imm):
    sexted_imm = sext(imm)
    reg1 = reg2 + sexted_imm
    return reg1

# def addi(reg1, reg2, imm):
#     reg1 = reg2 + imm
#     return reg1

def sltiu(reg1, reg2, imm):
    if reg2 < imm:
        reg1 = 1
    else:
        reg1 = 0
    return reg1

def jalr(reg1, reg2, imm):
    imm = comp(imm)
    pc = reg2 + (imm << 1)
    pc = (pc & 0xFFFFFFFE)  # make the LSB=0 for PC

    # store(link) the return address in (rd)
    reg1 = (pc + 4) & 0xFFFFFFFF  # rd = PC + 4

    return reg1

def sw(reg1, reg2, imm):
    reg1 = reg2 + (imm & 0xFFF)
    return reg1

def beq(reg1, reg2, imm):
    imm = comp(imm)
    if reg1 == reg2:
        return imm
    else:
        return 0
    
def bne(reg1, reg2, imm):
    imm = comp(imm)
    if reg1 != reg2:
        return imm
    else:
        return 0
    
def blt(reg1, reg2, imm):
    imm = comp(imm)
    if reg1 < reg2:
        return imm
    else:
        return 0
    
def bge(reg1, reg2, imm):
    imm = comp(imm)
    if reg1 >= reg2:
        return imm
    else:
        return 0
    
def bltu(reg1, reg2, imm):
    imm = comp(imm)
    if reg1 < reg2:
        return imm
    else:
        return 0
    
def bgeu(reg1, reg2, imm):
    imm = comp(imm)
    if reg1 >= reg2:
        return imm
    else:
        return 0
    
def lui(reg1, imm):
    reg1 = imm << 12
    return reg1

def auipc(reg1, imm):
    reg1 = reg1 + (imm << 12)
    return reg1

def jal(reg1, imm):
    imm = comp(imm)
    pc = (imm << 1) + reg1
    pc = (pc & 0xFFFFFFFE)  # make the LSB=0 for PC

    # store(link) the return address in (rd)
    reg1 = (pc + 4) & 0xFFFFFFFF  # rd = PC + 4

    return reg1



inputfile = sys.argv[1]
outputfile = sys.argv[2]

regnam = ['zero', 'ra', 'sp', 'gp', 'tp',
          't0', 't1', 't2', 's0', 'fp',
          's1', 'a0', 'a1', 'a2', 'a3',
          'a4', 'a5', 'a6', 'a7', 's2',
          's3', 's4', 's5', 's6', 's7',
          's8', 's9', 's10', 's11', 't3',
          't4', 't5', 't6']
regbin = ['00000', '00001', '00010', '00011', '00100',
          '00101', '00110', '00111', '01000', '01000',
          '01001', '01010', '01011', '01100', '01101',
          '01110', '01111', '10000', '10001', '10010',
          '10011', '10100', '10101', '10110', '10111',
          '11000', '11001', '11010', '11011', '11100',
          '11101', '11110', '11111']

zero = 0
ra = 0
sp = 0
gp = 0
tp = 0
t0 = 0
t1 = 0
t2 = 0
s0 = 0
s1 = 65536
a0 = 0
a1 = 0
a2 = 0
a3 = 0
a4 = 0
a5 = 0
a6 = 0
a7 = 0
s2 = 0
s3 = 0
s4 = 0
s5 = 0
s6 = 0
s7 = 0
s8 = 0
s9 = 0
s10 = 0
s11 = 0
t3 = 0
t4 = 0
t5 = 0
t6 = 0


with open(inputfile, 'r') as f:
    data = f.readlines()

data = [i.strip() for i in data]
commands = []

for i in data:
    if i.startswith(' ') == False:
        commands.append(i)

print(commands)

opcodes = []
for i in commands:
    opcodes.append(i[25:32])
print(opcodes)

cmdlen = len(commands)
count = 0

PROGRAM_COUNTER = 0b00000000000000000000000000000000


for i in range(0, cmdlen):
    count += 1
    print(count)
    if opcodes[i] == '0110011':
        print("R type")
        if commands[i][17:20] == '000' and commands[i][0:7] == '0000000':
            print("add")
            operands = RtoConsole(commands[i])
            globals()[operands[0]] = add(globals()[operands[0]], globals()[operands[1]], globals()[operands[2]])

        elif commands[i][17:20] == '000' and commands[i][0:7] == '0100000':
            print("sub")
            operands = RtoConsole(commands[i])
            sub(globals()[operands[0]], globals()[operands[1]], globals()[operands[2]])
            
        elif commands[i][17:20] == '001' and commands[i][0:7] == '0000000':
            print("sll")
            operands = RtoConsole(commands[i])
            sll(globals()[operands[0]], globals()[operands[1]], globals()[operands[2]])
        elif commands[i][17:20] == '010' and commands[i][0:7] == '0000000':
            print("slt")
            operands = RtoConsole(commands[i])
            slt(globals()[operands[0]], globals()[operands[1]], globals()[operands[2]])
        elif commands[i][17:20] == '011' and commands[i][0:7] == '0000000':
            print("sltu")
            operands = RtoConsole(commands[i])
            sltu(globals()[operands[0]], globals()[operands[1]], globals()[operands[2]])
        elif commands[i][17:20] == '100' and commands[i][0:7] == '0000000':
            print("xor")
            operands = RtoConsole(commands[i])
            xor(globals()[operands[0]], globals()[operands[1]], globals()[operands[2]])
        elif commands[i][17:20] == '101' and commands[i][0:7] == '0000000':
            print("srl")
            operands = RtoConsole(commands[i])
            srl(globals()[operands[0]], globals()[operands[1]], globals()[operands[2]])
        elif commands[i][17:20] == '110' and commands[i][0:7] == '0000000':
            print("or")
            operands = RtoConsole(commands[i])
            or_(globals()[operands[0]], globals()[operands[1]], globals()[operands[2]])
        elif commands[i][17:20] == '111' and commands[i][0:7] == '0000000':
            print("and")
            operands = RtoConsole(commands[i])
            and_(globals()[operands[0]], globals()[operands[1]], globals()[operands[2]])
    elif opcodes[i] == '0000011' and commands[i][17:20] == '010':
        print("I type")
        print('lw')
        operands = ItoConsole(commands[i])
        lw(globals()[operands[0]], globals()[operands[1]], operands[2])
    elif opcodes[i] == '0010011' and commands[i][17:20] == '000':
        print("I type")
        print('addi')
        operands = ItoConsole(commands[i])
        globals()[operands[0]] = addi(globals()[operands[0]], globals()[operands[1]], operands[2])
    elif opcodes[i] == '0010011' and commands[i][17:20] == '011':
        print("I type")
        print('sltiu')
        operands = ItoConsole(commands[i])
        sltiu(globals()[operands[0]], globals()[operands[1]], operands[2])
    elif opcodes[i] == '1100111' and commands[i][17:20] == '000':
        print("I type")
        print('jalr')
        operands = ItoConsole(commands[i])
        jalr(globals()[operands[0]], globals()[operands[1]], operands[2])
    elif opcodes[i] == '0100011' and commands[i][17:20] == '010':
        print("S Type")
        print('sw')
        operands = StoConsole(commands[i])
        sw(globals()[operands[0]], globals()[operands[1]],globals()[operands[2]])
    elif opcodes[i] == '1100011':
        print("B Type")
        if commands[i][17:20] == '000':
            print('beq')
            operands = BtoConsole(commands[i])
            beq(globals()[operands[0]], globals()[operands[1]],[operands[2]])
        elif commands[i][17:20] == '001':
            print('bne')
            operands = BtoConsole(commands[i])            
            bne(globals()[operands[0]], globals()[operands[1]],[operands[2]])
        elif commands[i][17:20] == '100':
            print('blt')
            operands = BtoConsole(commands[i])
            blt(globals()[operands[0]], globals()[operands[1]],[operands[2]])
        elif commands[i][17:20] == '101':
            print('bge')
            operands = BtoConsole(commands[i])
            bge(globals()[operands[0]], globals()[operands[1]],[operands[2]])
        elif commands[i][17:20] == '110':
            print('bltu')
            operands = BtoConsole(commands[i])
            bltu(globals()[operands[0]], globals()[operands[1]],[operands[2]])
        elif commands[i][17:20] == '111':
            print('bgeu')
            operands = BtoConsole(commands[i])
            bgeu(globals()[operands[0]], globals()[operands[1]],[operands[2]])

    elif opcodes[i] == '0110111':
        print("U Type")
        print('lui')
        operands = UtoConsole(commands[i])
    elif opcodes[i] == '0010111':
        print("U Type")
        print('auipc')
        operands = UtoConsole(commands[i])
    elif opcodes[i] == '1101111':
        print("J Type")
        print('jal')
        immbin = commands[i][0] + commands[i][12:20] + \
            commands[i][11] + commands[i][1:11]
        print("imm:", comp(immbin))

    if commands[i] == "00000000000000000000000001100011":
        print("PC:", bin(PROGRAM_COUNTER)[
              0:2]+bin(PROGRAM_COUNTER)[2:].zfill(32))
        break
    else:
        PROGRAM_COUNTER += 0b00000000000000000000000000000100
        print("PC:", bin(PROGRAM_COUNTER)[
              0:2]+bin(PROGRAM_COUNTER)[2:].zfill(32))

    print("Program Counter, zero, ra, sp, gp, tp, t1, t2, s0,  s1, a0, a1, a2, a3, a4, a5, a6, a7, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, t3, t4, t5, t6")
    print(PROGRAM_COUNTER, " ", zero, " ", ra, " ", sp, " ", gp, " ", tp, " ", t0, " ", t1, " ", t2, " ", s0, " ", s1, " ", a0, " ", a1, " ", a2, " ", a3, " ", a4, " ", a5, " ", a6, " ", a7, " ", s2, " ", s3, " ", s4, " ", s5, " ", s6, " ", s7, " ", s8, " ", s9, " ", s10, " ", s11, " ", t3, " ", t4, " ", t5, " ", t6)   
    print("=====================================")
    linetowrite = bin(PROGRAM_COUNTER).zfill(32) + " " + bin(zero).zfill(32) + " " + bin(ra).zfill(32) + " " + bin(sp).zfill(32) + " " + bin(gp).zfill(32) + " " + bin(tp).zfill(32) + " " + bin(t0).zfill(32) + " " + bin(t1).zfill(32) + " " + bin(t2).zfill(32) + " " + bin(s0).zfill(32) + " " + bin(s1).zfill(32) + " " + bin(a0).zfill(32) + " " + bin(a1).zfill(32) + " " + bin(a2).zfill(32) + " " + bin(a3).zfill(32) + " " + bin(a4).zfill(32) + " " + bin(a5).zfill(32) + " " + bin(a6).zfill(32) + " " + bin(a7).zfill(32) + " " + bin(s2).zfill(32) + " " + bin(s3).zfill(32) + " " + bin(s4).zfill(32) + " " + bin(s5).zfill(32) + " " + bin(s6).zfill(32) + " " + bin(s7).zfill(32) + " " + bin(s8).zfill(32) + " " + bin(s9).zfill(32) + " " + bin(s10).zfill(32) + " " + bin(s11).zfill(32) + " " + bin(t3).zfill(32) + " " + bin(t4).zfill(32) + " " + bin(t5).zfill(32) + " " + bin(t6).zfill(32)
    linetowrite = bin(PROGRAM_COUNTER)[0:2]+bin(PROGRAM_COUNTER)[2:].zfill(32) + " " + bin(zero)[0:2]+bin(zero)[2:].zfill(32) + " " + bin(ra)[0:2]+bin(ra)[2:].zfill(32) + " " + bin(sp)[0:2]+bin(sp)[2:].zfill(32) + " " + bin(gp)[0:2]+bin(gp)[2:].zfill(32) + " " + bin(tp)[0:2]+bin(tp)[2:].zfill(32) + " " + bin(t0)[0:2]+bin(t0)[2:].zfill(32) + " " + bin(t1)[0:2]+bin(t1)[2:].zfill(32) + " " + bin(t2)[0:2]+bin(t2)[2:].zfill(32) + " " + bin(s0)[0:2]+bin(s0)[2:].zfill(32) + " " + bin(s1)[0:2]+bin(s1)[2:].zfill(32) + " " + bin(a0)[0:2]+bin(a0)[2:].zfill(32) + " " + bin(a1)[0:2]+bin(a1)[2:].zfill(32) + " " + bin(a2)[0:2]+bin(a2)[2:].zfill(32) + " " + bin(a3)[0:2]+bin(a3)[2:].zfill(32) + " " + bin(a4)[0:2]+bin(a4)[2:].zfill(32) + " " + bin(a5)[0:2]+bin(a5)[2:].zfill(32) + " " + bin(a6)[0:2]+bin(a6)[2:].zfill(32) + " " + bin(a7)[0:2]+bin(a7)[2:].zfill(32) + " " + bin(s2)[0:2]+bin(s2)[2:].zfill(32) + " " + bin(s3)[0:2]+bin(s3)[2:].zfill(32) + " " + bin(s4)[0:2]+bin(s4)[2:].zfill(32) + " " + bin(s5)[0:2]+bin(s5)[2:].zfill(32) + " " + bin(s6)[0:2]+bin(s6)[2:].zfill(32) + " " + bin(s7)[0:2]+bin(s7)[2:].zfill(32) + " " + bin(s8)[0:2]+bin(s8)[2:].zfill(32) + " " + bin(s9)[0:2]+bin(s9)[2:].zfill(32) + " " + bin(s10)[0:2]+bin(s10)[2:].zfill(32) + " " + bin(s11)[0:2]+bin(s11)[2:].zfill(32) + " " + bin(t3)[0:2]+bin(t3)[2:].zfill(32) + " " + bin(t4)[0:2]+bin(t4)[2:].zfill(32) + " " + bin(t5)[0:2]+bin(t5)[2:].zfill(32) + " " + bin(t6)[0:2]+bin(t6)[2:].zfill(32)
    file.write(linetowrite)
    file.write("\n")
             
file.write(bin(PROGRAM_COUNTER)[0:2]+bin(PROGRAM_COUNTER)[2:].zfill(32) + " " + bin(zero)[0:2]+bin(zero)[2:].zfill(32) + " " + bin(ra)[0:2]+bin(ra)[2:].zfill(32) + " " + bin(sp)[0:2]+bin(sp)[2:].zfill(32) + " " + bin(gp)[0:2]+bin(gp)[2:].zfill(32) + " " + bin(tp)[0:2]+bin(tp)[2:].zfill(32) + " " + bin(t0)[0:2]+bin(t0)[2:].zfill(32) + " " + bin(t1)[0:2]+bin(t1)[2:].zfill(32) + " " + bin(t2)[0:2]+bin(t2)[2:].zfill(32) + " " + bin(s0)[0:2]+bin(s0)[2:].zfill(32) + " " + bin(s1)[0:2]+bin(s1)[2:].zfill(32) + " " + bin(a0)[0:2]+bin(a0)[2:].zfill(32) + " " + bin(a1)[0:2]+bin(a1)[2:].zfill(32) + " " + bin(a2)[0:2]+bin(a2)[2:].zfill(32) + " " + bin(a3)[0:2]+bin(a3)[2:].zfill(32) + " " + bin(a4)[0:2]+bin(a4)[2:].zfill(32) + " " + bin(a5)[0:2]+bin(a5)[2:].zfill(32) + " " + bin(a6)[0:2]+bin(a6)[2:].zfill(32) + " " + bin(a7)[0:2]+bin(a7)[2:].zfill(32) + " " + bin(s2)[0:2]+bin(s2)[2:].zfill(32) + " " + bin(s3)[0:2]+bin(s3)[2:].zfill(32) + " " + bin(s4)[0:2]+bin(s4)[2:].zfill(32) + " " + bin(s5)[0:2]+bin(s5)[2:].zfill(32) + " " + bin(s6)[0:2]+bin(s6)[2:].zfill(32) + " " + bin(s7)[0:2]+bin(s7)[2:].zfill(32) + " " + bin(s8)[0:2]+bin(s8)[2:].zfill(32) + " " + bin(s9)[0:2]+bin(s9)[2:].zfill(32) + " " + bin(s10)[0:2]+bin(s10)[2:].zfill(32) + " " + bin(s11)[0:2]+bin(s11)[2:].zfill(32) + " " + bin(t3)[0:2]+bin(t3)[2:].zfill(32) + " " + bin(t4)[0:2]+bin(t4)[2:].zfill(32) + " " + bin(t5)[0:2]+bin(t5)[2:].zfill(32) + " " + bin(t6)[0:2]+bin(t6)[2:].zfill(32))     
file.close()                 