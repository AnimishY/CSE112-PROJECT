from B2C import comp

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


def RtoConsole(commands):
        rdbin = commands[20:25]
        rs1bin = commands[12:17]
        rs2bin = commands[7:12]
        rdbin_index = regbin.index(rdbin)
        rs1bin_index = regbin.index(rs1bin)
        rs2bin_index = regbin.index(rs2bin)
        print("rd:", regnam[rdbin_index])
        print("rs1:", regnam[rs1bin_index])
        print("rs2:", regnam[rs2bin_index])
        return regnam[rdbin_index], regnam[rs1bin_index], regnam[rs2bin_index]


def ItoConsole(commands):
        rdbin = commands[20:25]
        rs1bin = commands[12:17]
        rdbin_index = regbin.index(rdbin)
        rs1bin_index = regbin.index(rs1bin)
        print("rd:", regnam[rdbin_index])
        print("rs1:", regnam[rs1bin_index])
        immbin = commands[0:12]
        print("imm:", comp(immbin))
        return regnam[rdbin_index], regnam[rs1bin_index], comp(immbin)


def StoConsole(commands):
        rdbin = commands[20:25]
        rs1bin = commands[12:17]
        rs2bin = commands[7:12]
        rdbin_index = regbin.index(rdbin)
        rs1bin_index = regbin.index(rs1bin)
        rs2bin_index = regbin.index(rs2bin)
        print("rd:", regnam[rdbin_index])
        print("rs1:", regnam[rs1bin_index])
        print("rs2:", regnam[rs2bin_index])
        immbin = commands[0:7] + commands[20:25]
        print("imm:", comp(immbin))
        return regnam[rdbin_index], regnam[rs1bin_index], regnam[rs2bin_index], comp(immbin)
        
def BtoConsole(commands):
        rs1bin = commands[12:17]
        rs2bin = commands[7:12]
        rs1bin_index = regbin.index(rs1bin)
        rs2bin_index = regbin.index(rs2bin)
        print("rs1:", regnam[rs1bin_index])
        print("rs2:", regnam[rs2bin_index])
        immbin = commands[0] + commands[24] + commands[1:7] + commands[20:24]
        print("imm:", comp(immbin))
        return regnam[rs1bin_index], regnam[rs2bin_index], comp(immbin)

        
def UtoConsole(commands):
        rd = commands[20:25]
        print("rd:", regnam[regbin.index(rd)])
        immbin = commands[0:20]
        print("imm:", comp(immbin))
        return regnam[regbin.index(rd)], comp(immbin)