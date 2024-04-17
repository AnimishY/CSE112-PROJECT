def binconvertint(s):
    o = 0
    s = s[::-1]
    for i in range(len(s)):
        o += (2**i)*int(s[i])
    return o

def add_one_to_binary(binary):
    return bin(int(binary, 2) + 1)[2:]


def comp(s):
    if s[0] == '0':
        return binconvertint(s[1:])  # Changed from s[1:len(s)] to s[1:]
    flipped = ''.join(['1' if bit == '0' else '0' for bit in s])
    return -binconvertint(add_one_to_binary(flipped))

print(bin(196))