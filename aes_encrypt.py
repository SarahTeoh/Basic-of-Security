import numpy as np
from itertools import chain

Sbox = [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]
       
# Yield successive n-sized chunks from lst.
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Rotate shift a list by n
def rotate(l, n):
    return l[n:] + l[:n]

def AddRoundKey(ori, key):
	e = []
	for i in range(len(ori)):
		e.append(hex(ori[i] ^ key[i]))
		
	return e

def SubBytes(e_list):
	f = []
	for e in e_list:
		row = int(e[2:3], 16)
		column = int(e[-1], 16)
		f.append(hex(Sbox[16 * row + column]))
	return f

def ShiftRows(f_list):
	g = list(chunks(f_list, 4))
	for i in range(len(g)):
		g[i] = rotate(g[i], i)

	return g

def generateT2T3(g):
	T2 = [0] * 16
	T3 = [0] * 16
	for i in range(4):
		for j in range(4):
			A = g[i + 4 * j]
			if A * 2 <= 255:
				T2[i + 4 * j] = A * 2 
			else:
				T2[i + 4 * j] = (A * 2) ^ 283

			T3[i + 4 * j] = A ^ T2[i + 4 * j]

	return T2, T3

def MixColumns(g):
	T2, T3 = generateT2T3(g)
	h = [0] * 16
	for i in range(4):
		for j in range(4):
			h[i] = T2[i] ^  T3[i + 4] ^ g[i + 4 * 2] ^ g[i + 4 * 3]
			h[i + 4] = g[i] ^ T2[i + 4] ^ T3[i + 4 * 2] ^ g[i ^ 4 * 3]
			h[i + 4 * 2] = g[i] ^ g[i ^ 4] ^ T2[i + 4 * 2] ^ T3[i + 4 * 3]
			h[i + 4 * 3] = T3[i] ^ g[i ^ 4] ^ g[i + 4 * 2] ^ T2[i + 4 * 3]

	return h


plaintext = list('u427824h@ecs.osa')

text_input = [0] * 16
for i in range(4):
	for j in range(4):
		text_input[4 * i + j] = ord(plaintext[4 * j + i])
"""
text_input = list(chunks(plaintext, 4))
text_input = list(map(list, zip(*text_input)))
#text_input = np.array([ord(char) for char in list(plaintext)])
"""
print("text_input: ", text_input)

key_string = '01 23 45 67 89 AB CD EF EF CD AB 89 67 45 23 01'.split()
"""
key = list(chunks(key_string, 4))
key = list(map(list, zip(*key)))
for keys in key:
	for num in keys:
		num = int(num, 16)

"""
key = [0]*16
for i in range(4):
	for j in range(4):
		key[4 * i + j] = int(key_string[4 * j + i], 16)
print("key: ", key)


e = AddRoundKey(text_input, key)
print("e: ", e)

f = SubBytes(e)
print("f: ", f)

g = ShiftRows(f)
g = list(chain(*g)) # Flatten multiple lists into one list
g = [int(num, 16) for num in g] 
print("g: ", g)

h = MixColumns(g)
print("h: ", h)

encrypted = [chr(dec) for dec in h]

print("Encrypted: ", encrypted)
