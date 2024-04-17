import sys

registersbinary = {
    '00000': 'zero', '00001': 'ra', '00010': 'sp', '00011': 'gp', '00100': 'tp',
    '00101': 't0', '00110': 't1', '00111': 't2', '01000': 's0', '01001': 's1',
    '01010': 'a0', '01011': 'a1', '01100': 'a2', '01101': 'a3', '01110': 'a4',
    '01111': 'a5', '10000': 'a6', '10001': 'a7', '10010': 's2', '10011': 's3',
    '10100': 's4', '10101': 's5', '10110': 's6', '10111': 's7', '11000': 's8',
    '11001': 's9', '11010': 's10', '11011': 's11', '11100': 't3', '11101': 't4',
    '11110': 't5', '11111': 't6'
}

registers = {
    "zero": 0, "ra": 0, "sp": 256, "gp": 0, "tp": 0,
    "t0": 0, "t1": 0, "t2": 0, "s0": 0, "s1": 0,
    "a0": 0, "a1": 0, "a2": 0, "a3": 0, "a4": 0,
    "a5": 0, "a6": 0, "a7": 0, "s2": 0, "s3": 0,
    "s4": 0, "s5": 0, "s6": 0, "s7": 0, "s8": 0,
    "s9": 0, "s10": 0, "s11": 0, "t3": 0, "t4": 0,
    "t5": 0, "t6": 0
}

PC = 0b00000000000000000000000000000100

memory = [0] * 32
memory_index = 0

MAIN_CODE = {}
input_file = sys.argv[1]
output_file = sys.argv[2]

infile = open(input_file, "r")
data = infile.read()
infile.close()

def signed_magnitude_to_int(binary):
    if binary[0] == '0':
        return int(binary, 2)
    else:
        return -int(binary[1:], 2)

def ADD(rs1, rs2, rd):
    rd = rs1 + rs2
    return rd

def SUB(rs1, rs2, rd):
    rd = rs1 - rs2
    return rd

def SLL(rs1, rs2, rd):
    rd = str(rs1) + ('0'*rs2)
    rd = int(rd, 2)
    return rd

def XOR(bin1, bin2, rd):
    max_len = max(len(bin1), len(bin2))
    bin1 = bin1.zfill(max_len)
    bin2 = bin2.zfill(max_len)

    result = ''
    for i in range(max_len):
        result += '1' if bin1[i] != bin2[i] else '0'
    
    rd = result
    return rd

def SLT(rs1, rs2, rd):
    if rs1 < rs2:
        rd = 1
    else:
        rd = 0
    return rd

def SLTU(rs1, rs2, rd):
    if rs1 < 0: rs1 = -1 * rs1
    if rs2 < 0: rs2 = -1 * rs2
    
    if rs1 < rs2:
        rd = 1
    else:
        rd = 0
    return rd

def SRL(rs1,rs2,rd):
    rd = rs1 >> rs2
    return rd

def OR(rs1, rs2, rd):
    rd = rs1 | rs2
    return rd

def AND(rs1, rs2, rd):
    rd = rs1 & rs2
    return rd

def LW(rs1, imm, rd):
    global memory_index
    rd = rs1 + imm
    memory[memory_index] = imm
    memory_index += 1
    return rd

def ADDI(rs1, imm, rd):
    rd = rs1 + imm
    return rd

def SLTIU(rs1, imm, rd):
    if rs1 < imm:
        rd = 1
    else:
        rd = 0
    return rd

def JALR(rs1, imm, rd):
    rd = PC + 4
    PC = rs1 + imm
    return rd

def SW(rs1, rs2, imm):
    memory[rs1 + imm] = rs2
    return memory[rs1 + imm]


def bin32 (x):
    return '0b' + bin(x)[2:].zfill(32)

for i in data.split("\n"):
    if i != "":
        temp = i.split(" ")
        MAIN_CODE[PC] = temp
        PC += 0b00000000000000000000000000000100


for i in MAIN_CODE:
    print(bin(i), MAIN_CODE[i])

# access the key of the last element in the dictionary
last_key = list(MAIN_CODE.keys())[-1]

i = list(MAIN_CODE.keys())[0]

output_file = open(output_file, "w")

while i <= last_key:
    print("PC: ", i, end=" ")
    if MAIN_CODE[i][0][25:32] == '0110011':
        print("R", end=" ")
        if MAIN_CODE[i][0][17:20] == '000':
            if MAIN_CODE[i][0][0:7] == '0000000':
                print("ADD")
                rs1 = MAIN_CODE[i][0][12:17]
                rs2 = MAIN_CODE[i][0][7:12]
                rd = MAIN_CODE[i][0][20:25]
                registers[registersbinary[rd]] = ADD(registers[registersbinary[rs1]], registers[registersbinary[rs2]], registers[registersbinary[rd]])
            elif MAIN_CODE[i][0][0:7] == '0100000':
                print("SUB")
                registers[registersbinary[rd]] = SUB(registers[registersbinary[rs1]], registers[registersbinary[rs2]], registers[registersbinary[rd]])
        elif MAIN_CODE[i][0][17:20] == '001':
            print("SLL")
            registers[registersbinary[rd]] = SLL(registers[registersbinary[rs1]], registers[registersbinary[rs2]], registers[registersbinary[rd]])
        elif MAIN_CODE[i][0][17:20] == '010':
            print("SLT")
            registers[registersbinary[rd]] = SLT(registers[registersbinary[rs1]], registers[registersbinary[rs2]], registers[registersbinary[rd]])
        elif MAIN_CODE[i][0][17:20] == '011':
            print("SLTU")
            registers[registersbinary[rd]] = SLTU(registers[registersbinary[rs1]], registers[registersbinary[rs2]], registers[registersbinary[rd]])
        elif MAIN_CODE[i][0][17:20] == '100':
            print("XOR")
            registers[registersbinary[rd]] = XOR(registers[registersbinary[rs1]], registers[registersbinary[rs2]], registers[registersbinary[rd]])
        elif MAIN_CODE[i][0][17:20] == '101':
            print("SRL")
            registers[registersbinary[rd]] = SRL(registers[registersbinary[rs1]], registers[registersbinary[rs2]], registers[registersbinary[rd]])
        elif MAIN_CODE[i][0][17:20] == '110':
            print("OR")
            registers[registersbinary[rd]] = OR(registers[registersbinary[rs1]], registers[registersbinary[rs2]], registers[registersbinary[rd]])
        elif MAIN_CODE[i][0][17:20] == '111':
            print("AND")
            registers[registersbinary[rd]] = AND(registers[registersbinary[rs1]], registers[registersbinary[rs2]], registers[registersbinary[rd]])
    elif MAIN_CODE[i][0][25:32] in ['0000011', '0010011', '0010011', '1100111']:
        print("I", end=" ")
        if MAIN_CODE[i][0][17:20] == '010' and MAIN_CODE[i][0][25:32] == '0000011':
            print("LW")
            rs1 = MAIN_CODE[i][0][12:17]
            imm = MAIN_CODE[i][0][0:12]
            rd = MAIN_CODE[i][0][20:25]
            registers[registersbinary[rd]] = LW(registers[registersbinary[rs1]], signed_magnitude_to_int(imm), registers[registersbinary[rd]])
        elif MAIN_CODE[i][0][17:20] == '000' and MAIN_CODE[i][0][25:32] == '0010011':
            print("ADDI")
            rs1 = MAIN_CODE[i][0][12:17]
            imm = MAIN_CODE[i][0][0:12]
            rd = MAIN_CODE[i][0][20:25]
            registers[registersbinary[rd]] = ADDI(registers[registersbinary[rs1]], signed_magnitude_to_int(imm), registers[registersbinary[rd]])
        elif MAIN_CODE[i][0][17:20] == '011' and MAIN_CODE[i][0][25:32] == '0010011':
            print("SLTIU")
            registers[registersbinary[rd]] = SLTIU(registers[registersbinary[rs1]], signed_magnitude_to_int(imm), registers[registersbinary[rd]])
        elif MAIN_CODE[i][0][17:20] == '000' and MAIN_CODE[i][0][25:32] == '1100111':
            print("JALR")
            
    elif MAIN_CODE[i][0][25:32] == '0100011':
        print("S", end=" ")
        print("SW")
        
    elif MAIN_CODE[i][0][25:32] == '1100011':
        print("B", end=" ")
        if MAIN_CODE[i][0][17:20] == '000':
            print("BEQ")
            rs1 = MAIN_CODE[i][0][12:17]
            rs2 = MAIN_CODE[i][0][7:12]
            imm = MAIN_CODE[i][0][0:7]
            if registers[registersbinary[rs1]] == registers[registersbinary[rs2]]:
                i = i + signed_magnitude_to_int(imm)
        elif MAIN_CODE[i][0][17:20] == '001':
            print("BNE")
            rs1 = MAIN_CODE[i][0][12:17]
            rs2 = MAIN_CODE[i][0][7:12]
            imm = MAIN_CODE[i][0][0:7]
            if registers[registersbinary[rs1]] != registers[registersbinary[rs2]]:
                i = i + signed_magnitude_to_int(imm)
        elif MAIN_CODE[i][0][17:20] == '100':
            print("BLT")
            rs1 = MAIN_CODE[i][0][12:17]
            rs2 = MAIN_CODE[i][0][7:12]
            imm = MAIN_CODE[i][0][0:7]
            if registers[registersbinary[rs1]] < registers[registersbinary[rs2]]:
                i = i + signed_magnitude_to_int(imm)
        elif MAIN_CODE[i][0][17:20] == '101':
            print("BGE")
            rs1 = MAIN_CODE[i][0][12:17]
            rs2 = MAIN_CODE[i][0][7:12]
            imm = MAIN_CODE[i][0][0:7]
            if registers[registersbinary[rs1]] >= registers[registersbinary[rs2]]:
                i = i + signed_magnitude_to_int(imm)
        elif MAIN_CODE[i][0][17:20] == '110':
            print("BLTU")
            rs1 = MAIN_CODE[i][0][12:17]
            rs2 = MAIN_CODE[i][0][7:12]
            imm = MAIN_CODE[i][0][0:7]
            if registers[registersbinary[rs1]] < registers[registersbinary[rs2]]:
                i = i + signed_magnitude_to_int(imm)
        elif MAIN_CODE[i][0][17:20] == '111':
            print("BGEU")
            rs1 = MAIN_CODE[i][0][12:17]
            rs2 = MAIN_CODE[i][0][7:12]
            imm = MAIN_CODE[i][0][0:7]
            if registers[registersbinary[rs1]] >= registers[registersbinary[rs2]]:
                i = i + signed_magnitude_to_int(imm)
    elif MAIN_CODE[i][0][25:32] in ['0110111', '0010111']:
        print("U")
    elif MAIN_CODE[i][0][25:32] == '1101111':
        print("J")
    else:
        print("Unknown")
    
    string1 = f"{bin32(i)} {bin32(registers['zero'])} {bin32(registers['ra'])} {bin32(registers['sp'])} {bin32(registers['gp'])} {bin32(registers['tp'])} {bin32(registers['t0'])} {bin32(registers['t1'])} {bin32(registers['t2'])} {bin32(registers['s0'])} {bin32(registers['s1'])} {bin32(registers['a0'])} {bin32(registers['a1'])} {bin32(registers['a2'])} {bin32(registers['a3'])} {bin32(registers['a4'])} {bin32(registers['a5'])} {bin32(registers['a6'])} {bin32(registers['a7'])} {bin32(registers['s2'])} {bin32(registers['s3'])} {bin32(registers['s4'])} {bin32(registers['s5'])} {bin32(registers['s6'])} {bin32(registers['s7'])} {bin32(registers['s8'])} {bin32(registers['s9'])} {bin32(registers['s10'])} {bin32(registers['s11'])} {bin32(registers['t3'])} {bin32(registers['t4'])} {bin32(registers['t5'])} {bin32(registers['t6'])}\n"
    output_file.write(string1)
    
    i += 0b00000000000000000000000000000100

memaddr = 0x00010000

for i in memory:
    string2 = f"{hex(memaddr)} {bin32(memory[i])}\n"
    output_file.write(string2)
    memaddr += 0x00000004

output_file.close()
print("Registers: ", registers)
print("Memory: ", memory)