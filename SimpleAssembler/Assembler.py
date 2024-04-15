import sys



def binary_string(number):                
    return bin(number)[2:]   




def Immediate(n,b):
   
    if n >=0:
        binary = bin(n)[2:]
    else:
        binary = bin(n & int("1" * (n.bit_length() + 1), 2))[2:]

   
    if len(binary) < b:
        if n >= 0:
            binary = '0' * (b - len(binary)) + binary
        else:                                                                       
            binary = '1' * (b - len(binary)) + binary
    elif len(binary) > b:
        binary = binary[-b:]
        
    return binary










    


r_type_instructions = {
    "add": {"opcode": "0110011", "rd": "", "funct3": "000", "rs1": "", "rs2": "", "funct7": "0000000"},
    "sub": {"opcode": "0110011", "rd": "", "funct3": "000", "rs1": "", "rs2": "", "funct7": "0100000"},
    "sll": {"opcode": "0110011", "rd": "", "funct3": "001", "rs1": "", "rs2": "", "funct7": "0000000"},
    "slt": {"opcode": "0110011", "rd": "", "funct3": "010", "rs1": "", "rs2": "", "funct7": "0000000"},
    "sltu": {"opcode": "0110011", "rd": "", "funct3": "011", "rs1": "", "rs2": "", "funct7": "0000000"},
    "xor": {"opcode": "0110011", "rd": "", "funct3": "100", "rs1": "", "rs2": "", "funct7": "0000000"},
    "srl": {"opcode": "0110011", "rd": "", "funct3": "101", "rs1": "", "rs2": "", "funct7": "0000000"},
    "or": {"opcode": "0110011", "rd": "", "funct3": "110", "rs1": "", "rs2": "", "funct7": "0000000"},
    "and": {"opcode": "0110011", "rd": "", "funct3": "111", "rs1": "", "rs2": "", "funct7": "0000000"}
}

i_type_instructions = {
    "lw": {"opcode": "0000011","rd": "", "funct3": "010", "rs1": "",  "imm": ""},
    "addi": {"opcode": "0010011","rd": "", "funct3": "000", "rs1": "",  "imm": ""},
    "sltiu": {"opcode": "0010011","rd": "", "funct3": "011", "rs1": "", "imm": ""},
    "jalr": {"opcode": "1100111","rd": "", "funct3": "000", "rs1": "",  "imm": ""}
}

s_type_instructions = {
    "sw": {"opcode": "0100011","imm":"", "funct3": "010","rs1":"","rs2":""},
}
b_type_instructions = {
    "beq": {"opcode": "1100011", "imm1": "", "funct3": "000", "rs1": "", "rs2": "", "imm2": ""},
    "bne": {"opcode": "1100011", "imm1": "", "funct3": "001", "rs1": "", "rs2": "", "imm2": ""},
    "blt": {"opcode": "1100011", "imm1": "", "funct3": "100", "rs1": "", "rs2": "", "imm2": ""},
    "bge": {"opcode": "1100011", "imm1": "", "funct3": "101", "rs1": "", "rs2": "", "imm2": ""},
    "bltu": {"opcode": "1100011", "imm1": "", "funct3": "110", "rs1": "", "rs2": "", "imm2": ""},
    "bgeu": {"opcode": "1100011", "imm1": "", "funct3": "111", "rs1": "", "rs2": "", "imm2": ""}
}

u_type_instructions = {
    "lui": {"opcode": "0110111","rd":"","imm":""},
    "auipc": {"opcode": "0010111","rd":"","imm":""},
}
j_type_instructions = {
    "jal": {"opcode": "1101111","rd":"","imm":""},
}




instruction_types=[r_type_instructions,i_type_instructions,s_type_instructions,b_type_instructions,u_type_instructions,j_type_instructions]








def get_get(line):
    s = ''
    for i in range(len(line)):
        if i == 0:
            if line[i] in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_":
                s += line[i]
            else:
                return None
                break
        else:
            if line[i] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz_":
                s += line[i]
                continue
            elif line[i] == ':':
                return s
                break
            else:
                return None
                break
    return None



register_encoding = {
    "x0": "00000",
    "zero": "00000",
    "r0": "00000",
    "x1": "00001",
    "ra": "00001",
    "r1": "00001",
    "x2": "00010",
    "sp": "00010",
    "r2": "00010",
    "x3": "00011",
    "gp": "00011",
    "r3": "00011",
    "x4": "00100",
    "tp": "00100",
    "r4": "00100",
    "x5": "00101",
    "t0": "00101",
    "r5": "00101",
    "x6": "00110",
    "t1": "00110",
    "r6": "00110",
    "x7": "00111",
    "t2": "00111",
    "r6": "00111",
    "x8":"01000",
    "r8":"01000",
    "s0":"01000",
    "fp":"01000",
    "x9":"01001",
    "r9":"01001",
    "s1":"01001",
    "r10": "01010",
    "x10":"01010",
    "a0":"01010",
    "x11": "01011",
    "a1": "01011",
    "r11": "01011",
    "x12": "01100",
    "a2": "01100",
    "r12": "01100",
    "x13": "01101",
    "a3": "01101",
    "r13": "01101",
    "x14": "01110",
    "a4": "01110",
    "r14": "01110",
    "x15": "01111",
    "a5": "01111",
    "r15": "01111",
    "x16": "10000",
    "a6": "10000",
    "r16": "10000",
    "x17": "10001",
    "a7": "10001",
    "x17": "10001",
    "x18": "10010",
    "s2": "10010",
    "r18": "10010",
    "x19": "10011",
    "s3": "10011",
    "r19": "10011",
    "x20": "10100",
    "s4": "10100",
    "r20": "10100",
    "x21": "10101",
    "s5": "10101",
    "r21": "10101",
    "x22": "10110",
    "s6": "10110",
    "r22": "10110",
    "x23": "10111",
    "s7": "10111",
    "r23": "10111",
    "x24": "11000",
    "s8": "11000",
    "r24": "11000",
    "x25": "11001",
    "s9": "11001",
    "r25": "11001",
    "x26": "11010",
    "s10": "11010",
    "r26": "11010",
    "x27": "11011",
    "s11": "11011",
    "r27": "11011",
    "x28": "11100",
    "t3": "11100",
    "r28": "11100",
    "x29": "11101",
    "t4": "11101",
    "r29": "11101",
    "x30": "11110",
    "t5": "11110",
    "r30": "11110",
    "x31": "11111",
    "t6": "11111",
    "r31": "11111"
}



ip=[]
with open("input.txt", 'r') as file:
    ip = [line.strip() for line in file]


ip = [line.split('#')[0].strip() for line in ip]
                        
    
def Ibinaryrep(decimal,totalbits):
    if decimal== 0:
        return '0'.zfill(totalbits)
    if decimal<0:
        decimal = abs(decimal)
        sign= '1'
    else:
        sign= '0'
    binary=''
    while decimal > 0:
        binary = str(decimal % 2) + binary
        decimal //= 2
    binary = sign + binary.zfill(totalbits - 1)
    return (binary)



def instruction(l,line_no,label,line):
    bintemp=''
    if l[0] in r_type_instructions.keys():
        temp = l[0]+" "
        op_lenght = len(temp)
        lin=line[op_lenght:]
        if(lin[0]==" "):
            f=open("output.txt","w")
            f.write(f"Invalid syntax for {temp} at line {line_no}")
            f.close()
            sys.exit()
        fun = lin.split(',')
        space_check=lin.split()
        if lin[0]==" ":
            f=open("output.txt","w")
            f.write(f"Invalid syntax for {temp} at line {line_no}")
            f.close()
            sys.exit()

        if len(fun)== 3 and len(space_check) == 1:
            try:
                registers=[reg.strip(",") for reg in l[1:]]
                bintemp+=r_type_instructions[l[0]]["funct7"]
                bintemp+=register_encoding[registers[0].split(",")[2]]                         
                bintemp+=register_encoding[registers[0].split(",")[1]]
                bintemp+=r_type_instructions[l[0]]["funct3"]
                bintemp+=register_encoding[registers[0].split(",")[0]] 
                bintemp+=r_type_instructions[l[0]]["opcode"]
                bintemp=bintemp+'\n'
            except:
                f=open("output.txt","w")
                f.write(f"Invalid register call for {temp} at line {line_no}")
                f.close()
                sys.exit()
        else:
            f=open("output.txt","w")
            f.write(f"Invalid syntax for {temp} at line {line_no}")
            f.close()
            sys.exit()
    
    elif l[0] in i_type_instructions.keys():
        temp = l[0]+" "
        op_lenght = len(temp)
        lin1=line[op_lenght:]
        if(lin1[0]==" "):
            f=open("output.txt","w")
            f.write(f"Invalid syntax for {temp} at line {line_no}")
            f.close()
            sys.exit()
        if l[0]=="lw":
            lin=line[3:]
            fun = lin.split(',')
            space_check=lin.split()
            if lin[0]==" ":
                f=open("output.txt","w")
                f.write(f"Invalid syntax for lw at line {line_no}")
                f.close()
                sys.exit()

            if len(fun)== 2 and len(space_check) == 1:
                tempnum=''
                for i in lin[1]:
                    if i in "0123456789":
                        tempnum=tempnum+i
                    else:
                        break
                if int(tempnum)>=-2048 and int(tempnum)<=2047:
                    try:
                        bintemp +=Immediate(int(l[1].split(",")[1].split("(")[0]),12)
                        bintemp +=register_encoding[l[1].split(",")[1].split("(")[1].strip(")")]   
                        bintemp +=i_type_instructions[l[0]]["funct3"]
                        bintemp +=register_encoding[l[1].split(",")[0]]   
                        bintemp +=i_type_instructions[l[0]]["opcode"]
                        bintemp=bintemp+'\n'
                    except:
                        f=open("output.txt","w")
                        f.write(f"Invalid syntax/register name for lw operator type at line {line_no}")
                        f.close()
                        sys.exit()
                else:
                    f=open("output.txt","w")
                    f.write(f"Illegal immediate value for lw at line {line_no}")
                    f.close()
                    sys.exit()


            else:
                f=open("output.txt","w")
                f.write(f"Invalid syntax for lw operator type at line {line_no}")
                f.close()
                sys.exit()

        else:
            temp = l[0]+" "
            op_lenght = len(temp)
            lin=line[op_lenght:]
            fun = lin.split(',')
            space_check=lin.split()
            if lin[0]==" ":
                f=open("output.txt","w")
                f.write(f"Invalid syntax for {temp} at line {line_no}")
                f.close()
                sys.exit()

            if len(fun)== 3 and len(space_check) == 1:
                if int(fun[2])>=-2048 and int(fun[2])<=2047:
                    try:
                        registers=[reg.strip(",") for reg in l[1:]]
                        bintemp +=Immediate(int(registers[0].split(",")[2]),12)
                        bintemp +=register_encoding[registers[0].split(",")[1]]
                        bintemp +=i_type_instructions[l[0]]["funct3"]
                        bintemp +=register_encoding[registers[0].split(",")[0]]
                        bintemp +=i_type_instructions[l[0]]["opcode"]
                        bintemp=bintemp+'\n'
                    except:
                        f=open("output.txt","w")
                        f.write(f"Invalid register name for {temp} at line {line_no}")
                        f.close()
                        sys.exit()

                else:
                    f=open("output.txt","w")
                    f.write(f"Illegal immediate value for {temp} at line {line_no}")
                    f.close()
                    sys.exit()

            else:
                f=open("output.txt","w")
                f.write(f"Invalid syntax for {temp} at line {line_no}")
                f.close()
                sys.exit()
        

        
    elif l[0] in s_type_instructions.keys():
        temp = l[0]+" "
        op_lenght = len(temp)
        lin1=line[op_lenght:]
        if(lin1[0]==" "):
            f=open("output.txt","w")
            f.write(f"Invalid syntax for {temp} at line {line_no}")
            f.close()
            sys.exit()
        lin = line[3:]
        fun = lin.split(',')
        space_check=lin.split()
        if lin[0]==" ":
            f=open("output.txt","w")
            f.write(f"Invalid syntax for sw at line {line_no}")
            f.close()
            sys.exit()

        if len(fun)== 2 and len(space_check) == 1:
            tempnum=''
            for i in lin[1]:
                if i in "0123456789":
                    tempnum=tempnum+i
                else:
                    break
            if int(tempnum)>=-2048 and int(tempnum)<=2047:
                try:
                    x=''
                    x=Immediate(int(l[1].split(",")[1].split("(")[0]),12)[::-1]
                    bintemp +=x[11:4:-1]
                    bintemp +=register_encoding[l[1].split(",")[0]]
                    bintemp +=register_encoding[l[1].split(",")[1].split("(")[1].strip(")")]
                    bintemp +=s_type_instructions[l[0]]["funct3"]
                    bintemp +=x[4:0:-1]
                    bintemp +=x[0]
                    bintemp +=s_type_instructions[l[0]]["opcode"]
                    bintemp=bintemp+'\n'
                except:
                    f=open("output.txt","w")
                    f.write(f"Invalid syntax/register name for sw operator type at line {line_no}")
                    f.close()
                    sys.exit()
            else:
                f=open("output.txt","w")
                f.write(f"Illegal immediate value for sw at line {line_no}")
                f.close()
                sys.exit()
        else:
            f=open("output.txt","w")
            f.write(f"Invalid syntax for sw operator type at line {line_no}")
            f.close()
            sys.exit()






    elif l[0] in b_type_instructions.keys():
        temp = l[0]+" "
        op_lenght = len(temp)
        lin=line[op_lenght:]
        if(lin[0]==" "):
            f=open("output.txt","w")
            f.write(f"Invalid syntax for {temp} at line {line_no}")
            f.close()
            sys.exit()
        fun = lin.split(',')
        if lin[0]==" ":
            f=open("output.txt","w")
            f.write(f"Invalid syntax for {temp} at line {line_no}")
            f.close()
            sys.exit()
        space_check=lin.split()
        if len(fun)== 3 and len(space_check) == 1:
            try:
                if int(fun[2])>=-4096 and int(fun[2])<=4095:
                    try: 
                        registers=[reg.strip(",") for reg in l[1:]]         
                        x=Immediate(int(registers[0].split(",")[2]),13)[::-1]     
                        bintemp+=x[12]
                        bintemp+=x[10:4:-1]
                        bintemp+=register_encoding[registers[0].split(",")[1]]
                        bintemp+=register_encoding[registers[0].split(",")[0]] 
                        bintemp +=b_type_instructions[l[0]]["funct3"]
                        bintemp+=x[4:0:-1]
                        bintemp+=x[11]
                        bintemp +=b_type_instructions[l[0]]["opcode"]
                        bintemp=bintemp+'\n'
                    except:
                        f=open("output.txt","w")
                        f.write(f"Invalid register call for {temp} at line {line_no}")
                        f.close()
                        sys.exit()
                else:
                    f=open("output.txt","w")
                    f.write(f"Illegal immediate value for {temp} at line {line_no}")
                    f.close()
                    sys.exit()
            except:     
                    try:
                        im = label[fun[2]]
                        registers=[reg.strip(",") for reg in l[1:]]        
                        x=Immediate(im,13)[::-1]    
                        bintemp+=x[12]
                        bintemp+=x[10:4:-1]
                        bintemp+=register_encoding[registers[0].split(",")[1]]
                        bintemp+=register_encoding[registers[0].split(",")[0]] 
                        bintemp +=b_type_instructions[l[0]]["funct3"]
                        bintemp+=x[4:0:-1]
                        bintemp+=x[11]
                        bintemp +=b_type_instructions[l[0]]["opcode"]
                        bintemp=bintemp+'\n'
                    except:
                        f=open("output.txt","w")
                        f.write(f"Invalid label value or illegal register name for {temp} at line {line_no}")
                        f.close()
                        sys.exit()

        else:
            f=open("output.txt","w")
            f.write(f"Invalid syntax for {temp} at line {line_no}")
            f.close()
            sys.exit()
                    


    elif l[0] in u_type_instructions.keys():
        temp = l[0]+" "
        op_lenght = len(temp)
        lin=line[op_lenght:]
        if lin[0]==" ":
            f=open("output.txt","w")
            f.write(f"Invalid syntax for {temp} at line {line_no}")
            f.close()
            sys.exit()

        fun = lin.split(',')
        space_check=lin.split()
        if len(fun)== 2 and len(space_check) == 1:
            if len(fun[1])>= -2147483648 or len(fun[1])<=2147483647:
                try:
                    registers=[operand.strip(",")for operand in l[1:]]
                    x=Immediate(int(registers[0].split(",")[1]),32)[::-1]
                    bintemp+=x[31:11:-1]
                    bintemp+=register_encoding[registers[0].split(",")[0]] 
                    bintemp +=u_type_instructions[l[0]]["opcode"]
                    bintemp=bintemp+'\n'
                except:
                    f=open("output.txt","w")
                    f.write(f"Invalid register call for {temp} at line {line_no}")
                    f.close()
                    sys.exit()

            else:
                f=open("output.txt","w")
                f.write(f"Illegal immediate value for {temp} at line {line_no}")
                f.close()
                sys.exit()

        else:
            f=open("output.txt","w")
            f.write(f"Invalid syntax for {temp} at line {line_no}")
            f.close()
            sys.exit()

    elif l[0] in j_type_instructions.keys():
        temp = l[0]+" "
        op_lenght = len(temp)
        lin1=line[op_lenght:]
        if(lin1[0]==" "):
            f=open("output.txt","w")
            f.write(f"Invalid syntax for {temp} at line {line_no}")
            f.close()
            sys.exit()
        lin=line[4:]
        fun = lin.split(',')
        space_check=lin.split()
        if lin[0]==" ":
            f=open("output.txt","w")
            f.write(f"Invalid syntax for jal at line {line_no}")
            f.close()
            sys.exit()

        if len(fun)== 2 and len(space_check) == 1:
            if len(fun[1])>= -1048576 or len(fun[1])<=1048575:
                try:
                    x=''
                    registers=[operand.strip(",")for operand in l[1:]]
                    x +=Immediate(int(registers[0].split(",")[1]),21)[::-1]
                    bintemp +=x[20]                                       
                    bintemp +=x[10:0:-1]                                  
                    bintemp +=x[11]
                    bintemp +=x[19:11:-1]  
                    bintemp+=register_encoding[registers[0].split(",")[0]] 
                    bintemp +=j_type_instructions[l[0]]["opcode"]
                    bintemp=bintemp+'\n'
                except:
                    f=open("output.txt","w")
                    f.write(f"Invalid register call for jal at line {line_no}")
                    f.close()
                    sys.exit()

            else:
                f=open("output.txt","w")
                f.write(f"Illegal immediate value for jal at line {line_no}")
                f.close()
                sys.exit()

        else:
            f=open("output.txt","w")
            f.write(f"Invalid syntax for jal at line {line_no}")
            f.close()
            sys.exit()
    f=open("output.txt",'a')
    f.write(bintemp)
    f.close()


        




    
 
label=dict() 
v_halt="beq zero,zero,0" 
count_halt=0 

line_no=0
pointer=0
for line in ip:
    line_no = line_no+1 
    if len(line)==0:
        continue
    else:
        pointer = pointer + 1
        l=line.split()
        m=l[0]
        cc=0
        for i in instruction_types:
            if m in i:
                if line==v_halt:
                    count_halt=count_halt+1
                break
        else:
            d = get_get(line)
            if d in label:
                g=open("output.txt","w")
                g.write(f"Error in Line {line_no} ,Duplicate Label" )
                g.close()
                sys.exit()
                break
            elif d == None:
                g=open("output.txt","w")
                g.write(f"Error in Line {line_no} ,Invalid Syntax" )
                g.close()
                sys.exit()
                break
            else:
                gray = len(d) + 1
                ld = line[gray:]
                if len(ld) == 0:
                    label[d] = (pointer)*4
                    continue
                else:
                    ld = ld.strip()
                    if ld==v_halt:
                        count_halt=count_halt+1
                    label[d] = (pointer-1)*4
                    continue

if count_halt==0:
    f=open("output.txt","w") 
    f.write("Error:No Virtual Halt in Program")
    f.close()
    sys.exit()

       
line_no=0
for line in ip:
    line_no = line_no+1 
    if len(line)==0:
        continue
    else:
        l=line.split()
        m=l[0]
        for i in instruction_types:
            if m in i:
                instruction(l,line_no,label,line)
                break
        else:
            d = get_get(line)
            if d == None:
                continue
            else:
                gray = len(d) + 1
                lin = line[gray:]
                if len(lin) == 0:
                    continue
                else:
                    lin = lin.strip()
                    l=lin.split()
                    instruction(l,line_no,label,line)
                    continue