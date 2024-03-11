import re
# dictionary with assembly command : [opode, opcode type, func 3, func 7]
# if invalid then "inv"
opcode = {
    'add': ['0110011', 'R', '000', '0000000'],
    'sub': ['0110011', 'R', '000', '0100000'],
    'sll': ['0110011', 'R', '001', '0000000'],
    'slt': ['0110011', 'R', '010', '0000000'],
    'sltu': ['0110011', 'R', '011', '0000000'],
    'xor': ['0110011', 'R', '100', '0000000'],
    'srl': ['0110011', 'R', '101', '0000000'],
    'or': ['0110011', 'R', '110', '0000000'],
    'and': ['0110011', 'R', '111', '0000000'],
    'lw': ['0000011', 'I', '010', 'inv'],
    'addi': ['0010011', 'I', '000', 'inv'],
    'sltiu': ['0010011', 'I', '011', 'inv'],
    'jalr': ['1100111', 'I', '000', 'inv'],
    'sw': ['0100011', 'S', '010', 'inv'],
    'beq': ['1100011', 'B', '000', 'inv'],
    'bne': ['1100011', 'B', '001', 'inv'],
    'blt': ['1100011', 'B', '100', 'inv'],
    'bge': ['1100011', 'B', '101', 'inv'],
    'bltu': ['1100011', 'B', '110', 'inv'],
    'bgeu': ['1100011', 'B', '111', 'inv'],
    'lui': ['0110111', 'U', 'inv', 'inv'],
    'auipc': ['0010111', 'U', 'inv', 'inv'],
    'jal': ['1101111', 'J', 'inv', 'inv'],
    'hlt': ['1111111', 'C', 'inv', 'inv'],
    'mul': ['0000000', 'C', 'inv', 'inv'],
    'rst': ['0000001', 'C', 'inv', 'inv'],
    'rvrs': ['0000010', 'C', 'inv', 'inv']
}

#register adresses in format ABI : binary adress
registers = {
    'zero': '00000', # hard wired to 0
    'ra': '00001', # return address
    'sp': '00010', # stack pointer
    'gp': '00011', # global pointer
    'tp': '00100', # thread pointer
    't0': '00101', # temporary
    't1': '00110', # temporaries
    't2': '00111', # temporaries
    's0': '01000', # saved register / frame pointer
    'fp': '01000', # saved register / frame pointer
    's1': '01001', # saved register
    'a0': '01010', # return value
    'a1': '01011', # return value
    'a2': '01100', # argument
    'a3': '01101', # argument
    'a4': '01110', # argument
    'a5': '01111', # argument
    'a6': '10000', # argument
    'a7': '10001', # argument 
    's2': '10010', # saved register
    's3': '10011', # saved register
    's4': '10100', # saved register
    's5': '10101', # saved register
    's6': '10110', # saved register
    's7': '10111', # saved register
    's8': '11000', # saved register
    's9': '11001', # saved register
    's10': '11010', # saved register
    's11': '11011', # saved register
    't3': '11100', # temporaries
    't4': '11101', # temporaries
    't5': '11110', # temporaries
    't6': '11111', # temporaries
}

# function to find opcode
def find_opcode(asmcmd):
    opcude_list = {
    'add': ['0110011', 'R', '000', '0000000'],
    'sub': ['0110011', 'R', '000', '0100000'],
    'sll': ['0110011', 'R', '001', '0000000'],
    'slt': ['0110011', 'R', '010', '0000000'],
    'sltu': ['0110011', 'R', '011', '0000000'],
    'xor': ['0110011', 'R', '100', '0000000'],
    'srl': ['0110011', 'R', '101', '0000000'],
    'or': ['0110011', 'R', '110', '0000000'],
    'and': ['0110011', 'R', '111', '0000000'],
    'lw': ['0000011', 'I', '010', 'inv'],
    'addi': ['0010011', 'I', '000', 'inv'],
    'sltiu': ['0010011', 'I', '011', 'inv'],
    'jalr': ['1100111', 'I', '000', 'inv'],
    'sw': ['0100011', 'S', '010', 'inv'],
    'beq': ['1100011', 'B', '000', 'inv'],
    'bne': ['1100011', 'B', '001', 'inv'],
    'blt': ['1100011', 'B', '100', 'inv'],
    'bge': ['1100011', 'B', '101', 'inv'],
    'bltu': ['1100011', 'B', '110', 'inv'],
    'bgeu': ['1100011', 'B', '111', 'inv'],
    'lui': ['0110111', 'U', 'inv', 'inv'],
    'auipc': ['0010111', 'U', 'inv', 'inv'],
    'jal': ['1101111', 'J', 'inv', 'inv'],
    'hlt': ['1111111', 'C', 'inv', 'inv'],
    'mul': ['0000000', 'C', 'inv', 'inv'],
    'rst': ['0000001', 'C', 'inv', 'inv'],
    'rvrs': ['0000010', 'C', 'inv', 'inv']
}

    if asmcmd in opcude_list:
        return opcude_list[asmcmd][0]

# function to find opcode info
def find_info(asmcmd):
    opcude_list = {
    'add': ['0110011', 'R', '000', '0000000'],
    'sub': ['0110011', 'R', '000', '0100000'],
    'sll': ['0110011', 'R', '001', '0000000'],
    'slt': ['0110011', 'R', '010', '0000000'],
    'sltu': ['0110011', 'R', '011', '0000000'],
    'xor': ['0110011', 'R', '100', '0000000'],
    'srl': ['0110011', 'R', '101', '0000000'],
    'or': ['0110011', 'R', '110', '0000000'],
    'and': ['0110011', 'R', '111', '0000000'],
    'lw': ['0000011', 'I', '010', 'inv'],
    'addi': ['0010011', 'I', '000', 'inv'],
    'sltiu': ['0010011', 'I', '011', 'inv'],
    'jalr': ['1100111', 'I', '000', 'inv'],
    'sw': ['0100011', 'S', '010', 'inv'],
    'beq': ['1100011', 'B', '000', 'inv'],
    'bne': ['1100011', 'B', '001', 'inv'],
    'blt': ['1100011', 'B', '100', 'inv'],
    'bge': ['1100011', 'B', '101', 'inv'],
    'bltu': ['1100011', 'B', '110', 'inv'],
    'bgeu': ['1100011', 'B', '111', 'inv'],
    'lui': ['0110111', 'U', 'inv', 'inv'],
    'auipc': ['0010111', 'U', 'inv', 'inv'],
    'jal': ['1101111', 'J', 'inv', 'inv'],
    'hlt': ['1111111', 'C', 'inv', 'inv'],
    'mul': ['0000000', 'C', 'inv', 'inv'],
    'rst': ['0000001', 'C', 'inv', 'inv'],
    'rvrs': ['0000010', 'C', 'inv', 'inv']
}

    if asmcmd in opcude_list:
        return opcude_list[asmcmd]

#function to find register using AIB    
def find_reg(reg):
    registers = {
        'zero': '00000', # hard wired to 0
        'ra': '00001', # return address
        'sp': '00010', # stack pointer
        'gp': '00011', # global pointer
        'tp': '00100', # thread pointer
        't0': '00101', # temporary
        't1': '00110', # temporaries
        't2': '00111', # temporaries
        's0': '01000', # saved register / frame pointer
        'fp': '01000', # saved register / frame pointer
        's1': '01001', # saved register
        'a0': '01010', # return value
        'a1': '01011', # return value
        'a2': '01100', # argument
        'a3': '01101', # argument
        'a4': '01110', # argument
        'a5': '01111', # argument
        'a6': '10000', # argument
        'a7': '10001', # argument 
        's2': '10010', # saved register
        's3': '10011', # saved register
        's4': '10100', # saved register
        's5': '10101', # saved register
        's6': '10110', # saved register
        's7': '10111', # saved register
        's8': '11000', # saved register
        's9': '11001', # saved register
        's10': '11010', # saved register
        's11': '11011', # saved register
        't3': '11100', # temporaries
        't4': '11101', # temporaries
        't5': '11110', # temporaries
        't6': '11111', # temporaries
    }
    if reg in registers:
        return registers[reg]

#function to find function 7   
def find_fn7(asmcmd):
    opcude_list = {
    'add': ['0110011', 'R', '000', '0000000'],
    'sub': ['0110011', 'R', '000', '0100000'],
    'sll': ['0110011', 'R', '001', '0000000'],
    'slt': ['0110011', 'R', '010', '0000000'],
    'sltu': ['0110011', 'R', '011', '0000000'],
    'xor': ['0110011', 'R', '100', '0000000'],
    'srl': ['0110011', 'R', '101', '0000000'],
    'or': ['0110011', 'R', '110', '0000000'],
    'and': ['0110011', 'R', '111', '0000000'],
}

    if asmcmd in opcude_list:
        return opcude_list[asmcmd][3]

#function to find function 3    
def find_fn3(asmcmd):
        opcude_list = {
        'add': ['0110011', 'R', '000', '0000000'],
        'sub': ['0110011', 'R', '000', '0100000'],
        'sll': ['0110011', 'R', '001', '0000000'],
        'slt': ['0110011', 'R', '010', '0000000'],
        'sltu': ['0110011', 'R', '011', '0000000'],
        'xor': ['0110011', 'R', '100', '0000000'],
        'srl': ['0110011', 'R', '101', '0000000'],
        'or': ['0110011', 'R', '110', '0000000'],
        'and': ['0110011', 'R', '111', '0000000'],
        'lw': ['0000011', 'I', '010', 'inv'],
        'addi': ['0010011', 'I', '000', 'inv'],
        'sltiu': ['0010011', 'I', '011', 'inv'],
        'jalr': ['1100111', 'I', '000', 'inv'],
        'sw': ['0100011', 'S', '010', 'inv'],
        'beq': ['1100011', 'B', '000', 'inv'],
        'bne': ['1100011', 'B', '001', 'inv'],
        'blt': ['1100011', 'B', '100', 'inv'],
        'bge': ['1100011', 'B', '101', 'inv'],
        'bltu': ['1100011', 'B', '110', 'inv'],
        'bgeu': ['1100011', 'B', '111', 'inv'],
        }
    
        if asmcmd in opcude_list:
            return opcude_list[asmcmd][2]

#function to calculate binary 2's complement string from decimal string     
def imm(n, num_bits):
    n = int(n)
    if n < 0:
       
        binary_repr = bin(n & ((1 << num_bits) - 1))[2:]
    else:
        
        binary_repr = bin(n)[2:].zfill(num_bits)

    return str(binary_repr)

#function to throw error in case of incorrect use of halt
def halterror(halt, l1):
    count=0
    for i in range(len(l1)):
        if l1[i]==halt:
            count+=1
    if count>1:
        file=open('binary.txt','w')
        file.write("error: More than one virtual halt")
        file.close()
        return True
    elif count==1:
        if l1[len(l1)-1]!=halt:
            file=open('binary.txt','w')
            file.write("error: Halt not last instruction")
            file.close()
            return True
    elif count==0:
        file=open('binary.txt','w')
        file.write("error: No virtual halt found")
        file.close()
        return True
    return False
        
    
def error_check(list):
    oplist = ['add','sub','sll','slt','sltu','xor','srl','or','and','lw',
              'addi','sltiu','jalr','sw','beq','bne','blt', 'bge','bltu',
              'bgeu','lui','auipc','jal', 'mul','rst','rvrs','halt']
    reglist = ['zero','ra','sp','gp','tp','t0','t1','t2','s0','fp','s1','a0','a1',
                'a2','a3','a4','a5','a6','a7','s2','s3','s4','s5','s6','s7','s8',
                's9','s10','s11','t3','t4','t5','t6']
    if list[0] not in oplist:
            file=open('binary.txt','w')
            file.write("error: incorrect specification in ",i)
            file.close()
            return True
    for i in list:
        if " " in i:
            file=open('binary.txt','w')
            file.write("error: incorrect specification in ",i)
            file.close()
            return True
        if (i not in oplist) and type(i)!=int and ("(" not in i) and i not in reglist:
            file=open('binary.txt','w')
            file.write("error: incorrect specification in ",i)
            file.close()
            return True
    return False

def assemble2(input_file, output_file, binary_code):
    with open(input_file, 'r') as file:
        assembly_code = file.readlines()

    for line_number, line in enumerate(assembly_code, start=1):
        line = line.strip()
        
        if ":" in line:
            line = line[line.index(':')+2 :]

        command_list = []
        asmcmd, operands = line.split()
        operands = operands.split(",")
        operands = [i.replace(" ", "") for i in operands]
        command_list.append(asmcmd)
        command_list.extend(operands)
        if error_check(command_list):
            return
        
        asmcmd_info = find_info(asmcmd) # check for valid opcode
        if asmcmd_info is None:
            error_message = f"Invalid opcode '{asmcmd}' at line {line_number}"
            with open(output_file, 'w') as file:
                file.write(error_message)
                file.close()
            return


        opcode = asmcmd_info[0]
        asmcmd_type = asmcmd_info[1]
        
        if asmcmd_type == 'R':
            bin = find_fn7(asmcmd) + find_reg(command_list[3]) + find_reg(command_list[2]) + find_fn3(asmcmd) + find_reg(command_list[1]) + opcode
            binary_code.append(bin)

        elif line == "beq zero,zero,0x00000000":
            bin = t = imm(command_list[3], 10)
            bin = '00000000' + find_reg(command_list[2]) + find_reg(command_list[1]) + find_fn3(asmcmd) + '0000' + opcode
            binary_code.append(bin)
            return
        
        elif asmcmd == 'halt':
            binary_code.append('000000000000000000' + find_fn3('beq') + '0000' + opcode)
            return
        
        elif asmcmd_type == 'I':
            if asmcmd == 'lw':
                n = ''
                x=''
                for i in command_list[2]:
                    if i != '(':
                        n += i
                    else:
                        break
                for i in command_list[2][command_list[2].index("(")+1:]:
                    if i != ")":
                        x+=i
                    else:
                        break
                bin = imm(n, 12) + find_reg(x) + find_fn3(asmcmd) + find_reg(command_list[1]) + opcode
                binary_code.append(bin)
            else:
                bin = imm(command_list[3], 12) + find_reg(command_list[2]) + find_fn3(asmcmd) + find_reg(command_list[1]) + opcode
                binary_code.append(bin)

        elif asmcmd_type == 'S':
            n = ''
            x=''
            for i in command_list[2]:
                if i != '(':
                    n += i
                else:
                    break
            for i in command_list[2][command_list[2].index("(")+1:]:
                if i != ")":
                    x+=i
                else:
                    break
            t=imm(n,12)
            bin = t[0:8] + find_reg(command_list[1]) +  find_reg(x) + find_fn3(asmcmd) + t[8:13] + opcode
            binary_code.append(bin)

        elif asmcmd_type == 'B':
            t = imm(command_list[3], 10)
            bin = '00' + t[0:7] + find_reg(command_list[2]) + find_reg(command_list[1]) + find_fn3(asmcmd) + t[7:11] + opcode
            binary_code.append(bin)

        elif asmcmd_type == 'U':
            bin = imm(command_list[2], 20) + find_reg(command_list[1]) + opcode
            binary_code.append(bin)

        elif asmcmd_type == 'J':
            t = imm(command_list[2], 20)
            bin = t[10:-1:-1] + t[11] + t[19:11:-1] + find_reg(command_list[1]) + opcode
            binary_code.append(bin)

def assemble(assembly_file, binary_file):
    binary_code = []
    assemble2('assembly_code.txt', 'binary.txt', binary_code)
    if halterror('00000000000000000000000001100011', binary_code) == True:
            return
    with open('binary.txt', 'w') as file:
        for code in binary_code:
            if ':' in code:
                file.write(code)
            else:
                file.write(code + '\n')
        
# Test the assembler
assemble('assembly_code.txt', 'binary.txt')
