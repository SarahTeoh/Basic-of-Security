import itertools

# Encryption key
key = '23456789ABCD'

# Convert plaintext input from a Hex to binary 
pt_hexinput = input("Enter The CipherText in Hex(16 digits):\n")
try:
    (int(pt_hexinput, 16)) 
except:
    print ("That is an invalid hex value")
if len(pt_hexinput) == 16:    
        pass
else: raise ValueError('error')
pt_bininput=bin(int(pt_hexinput, 16))[2:].zfill(64)
pt= []
#pt.append(0)
for digit in str(pt_bininput):
    pt.append(int(digit))

# Separate to upper and lower bytes
left = pt[:32]　
right = pt[32:]

#Permutation Function
def permu(perm):
    p=    [perm[15], perm[6],  perm[19], perm[20], 
           perm[28], perm[11], perm[27], perm[16], 
           perm[0],  perm[14], perm[22], perm[25], 
           perm[4],  perm[17], perm[30], perm[9], 
           perm[1],  perm[7],  perm[23], perm[13], 
           perm[31], perm[26], perm[2],  perm[8], 
           perm[18], perm[12], perm[29], perm[5], 
           perm[21], perm[10], perm[3],  perm[24]]
    return (p)

#Expand right side from 32 bits to 48 bits
def extend(ex):
    EX =    [ex[31], ex[0],  ex[1],  ex[2],  ex[3],  ex[4], 
             ex[3],  ex[4],  ex[5],  ex[6],  ex[7],  ex[8], 
             ex[7],  ex[8],  ex[9],  ex[10], ex[11], ex[12], 
             ex[11], ex[12], ex[13], ex[14], ex[15], ex[16], 
             ex[15], ex[16], ex[17], ex[18], ex[19], ex[20], 
             ex[19], ex[20], ex[21], ex[22], ex[23], ex[24], 
             ex[23], ex[24], ex[25], ex[26], ex[27], ex[28], 
             ex[27], ex[28], ex[29], ex[30], ex[31], ex[0]]
    return (EX)

#S-Boxes
def S_Boxes():
    S1 =    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
             [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
             [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
             [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]]
    S2 =    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
             [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
             [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
             [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]]
    S3 =    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
             [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
             [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
             [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]]
    S4 =    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
             [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
             [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
             [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]]
    S5 =    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
             [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
             [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
             [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]]
    S6 =    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
             [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
             [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
             [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]]
    S7 =    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
             [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
             [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
             [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]]
    S8 =    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
             [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
             [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
             [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
    return [S1, S2, S3, S4, S5, S6, S7, S8]

# Expand lower bytes to 48 bits
ex = extend(right)

# Convert hex key into binary
sub_key = bin(int(key, 16))[2:].zfill(48)
subkey = []
for digit in str(sub_key):
    subkey.append(int(digit))

# XOR with upper bytes
new = []
for i in range(48):
    new.append(ex[i] ^ subkey[i])  
new= list(map(str, new))
print("XOR result : ", format(new))

# Input to S boxes and permutation
temp=0
temp1=[]
s_box = S_Boxes()
y=0

for x in range (0,48,6):
    temp = s_box[y][int(''.join(new[x]+new[x+5]),2)][int(''.join(new[x+1:x+5]),2)]
    if y < 8: 
        y+=1
    temp=(bin(int(temp))[2:].zfill(4))
    temp1.append([int(i) for i in str(temp)])

temp1 = list(itertools.chain(*temp1))
print("F Function output ",format(temp1))
temp1=permu(temp1)
print("Output of permutation function ",format(temp1))

new_left = []
for i in range(32):
    new_left.append(left[i] ^ temp1[i])
print("XOR Results with left:", new_left)

final = right+new_left
print("Final: ", final)
final_binary_string = "".join(str(bit) for bit in final)
print(final_binary_string)
