def SLL(rd, rs1, rs2):
    rd = rs1 << rs2
    return rd

rs1 = 1
rs2 = 16

print(SLL(rs1, rs1, rs2)) 