def bindigits(n, bits):
    s = bin(n & int("1"*bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)
num = int(input('Enter integer (-128 to 127):'))

# Printing binary string of number
print(bin(num))
print(bin(num & 0b11111111))
print(bindigits(num,8))
print("EO3")

#Two's complement operation
num = ~ num + 1
print(bindigits(num,8))
print(num)

#shift left by 3
num = num << 3
print(bindigits(num,8))

#shift right by 2
num = num >> 2
print(bindigits(num,8))

# AND Mask
num = 0b10101010 & 0b00001111
print(bindigits(num,8))

#OR Mask
num = 0b10101010 | 0b00001111
print(bindigits(num,8))

#XOR Mask
num = 0b10101010 ^ 0b00001111
print(bindigits(num,8))
