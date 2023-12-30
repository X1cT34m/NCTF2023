from Crypto.Util.number import *
from typing import List
from functools import reduce
from operator import add
from collections import Counter

__ep = [31,  0,  1,  2,  3,  4,
		 3,  4,  5,  6,  7,  8,
		 7,  8,  9, 10, 11, 12,
		11, 12, 13, 14, 15, 16,
		15, 16, 17, 18, 19, 20,
		19, 20, 21, 22, 23, 24,
		23, 24, 25, 26, 27, 28,
		27, 28, 29, 30, 31,  0
]

__P_inv = [8, 16, 22, 30, 12, 27, 1, 17, 
			23, 15, 29, 5, 25, 19, 9, 0, 
			7, 13, 24, 2, 3, 28, 10, 18, 
			31, 11, 21, 6, 4, 26, 14, 20
]

__s_box = [

	[
		[14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
		[ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
		[ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
		[15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]
	],


	[
		[15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
		[ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
		[ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
		[13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9]
	],


	[
		[10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
		[13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
		[13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
		[ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]
	],


	[
		[ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
		[13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
		[10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
		[ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]
	],


	[
		[ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
		[14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
		[ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
		[11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3]
	],


	[
		[12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
		[10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
		[ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
		[ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13]
	],


	[
		[ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
		[13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
		[ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
		[ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12]
	],


	[
		[13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
		[ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
		[ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
		[ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11]
	]
]

def S_box(data: List[int],index) -> List[int]:
    output = []
    row = data[0] * 2 + data[5]
    col = reduce(add, [data[j] * (2 ** (4 - j)) for j in range(1, 5)])
    output += [int(x) for x in format(__s_box[index][row][col], '04b')]
    return output

def P_inv(data: List[int]) -> List[int]:
	return [data[x] for x in __P_inv]

def EP(data: List[int]) -> List[int]:
    return [data[x] for x in __ep]

def bytes2bits(bytes):
	result = reduce(add, [list(map(int, bin(byte)[2:].zfill(8))) for byte in bytes])
	return result

def bits2bytes(bits):
	result = ''
	for i in bits:result += str(i) 
	return long_to_bytes(int(result,2))

def num2bits(num):
	result = list(map(int, bin(num)[2:].zfill(6)))
	return result

def bits2num(bits):
	result = ''.join([str(i) for i in bits])
	return eval('0b'+result)


def bit2list8(bits):
	assert len(bits) == 32
	result = []
	#print(bits)
	for i in range(8):
		tmp = [str(i) for i in bits[4*i:4*(i+1)]]
		tmp = eval('0b'+''.join(tmp))
		result.append(tmp)
	return result

def out_inv(cipher):
    cipher = [cipher[x] for x in[57,  49, 41, 33, 25, 17, 9, 1,
                                59,  51, 43, 35, 27, 19, 11, 3,
                                61,  53, 45, 37, 29, 21, 13, 5,
                                63,  55, 47, 39, 31, 23, 15, 7,
                                56,  48, 40, 32, 24, 16, 8, 0,
                                58,  50, 42, 34, 26, 18, 10, 2,
                                60,  52, 44, 36, 28, 20, 12, 4,
                                62,  54, 46, 38, 30, 22, 14, 6]]
    return cipher

def Get_Out_Diff(c1,c2):
	L1 = bytes_to_long(c1[:4])
	L2 = bytes_to_long(c2[:4])
	Out_Diff = hex(L1^L2)
	return Out_Diff

def guess_keys(input1,input2,output_diff):
	input1 = EP(bytes2bits(input1))
	input2 = EP(bytes2bits(input2))
	keys = []
	output_diff = bit2list8(output_diff)
	#print(input1[0:])
	for i in range(8):
		for guess_key in range(64):
			guess_key = num2bits(guess_key)
			xor_result1 = [a ^ b for a, b in zip(input1[6*i:6*(i+1)], guess_key)]
			xor_result2 = [a ^ b for a, b in zip(input2[6*i:6*(i+1)], guess_key)]

			substituted1 = S_box(xor_result1,i)
			substituted2 = S_box(xor_result2,i)

			if bits2num(substituted1)^bits2num(substituted2) == output_diff[i]:
				keys.append((bits2num(guess_key),i))

	return keys




form_diff = ['0x202', '0x8002', '0x8200', '0x8202', '0x800002', '0x800200', '0x800202', '0x808000', '0x808002', '0x808200', '0x808202']


enc1=['e392ac8bb916a1c4', '20a10deb74576ae9', 'd186e0fc220a67f9', '17ce709d69048488', 'a2f945212d4684da']
enc2=['d6f79f862e21cbc7', '2185586bf0fd7ef8', '39c735debc3793bb', 'e3fa91b0b26e358d', '4be9f65d2d85ae9d']

result = []

for _ in range(5):
	for i in form_diff:
		diff1 = i
		round0 = bytes.fromhex(enc1[_])
		round1 = bytes.fromhex(enc2[_])

		round0 = bits2bytes(out_inv(bytes2bits(round0)))
		round1 = bits2bytes(out_inv(bytes2bits(round1)))

		out_diffs = (Get_Out_Diff(round0,round1))
		output_diff = long_to_bytes(eval(out_diffs)^eval(diff1))
		output_diff = P_inv(bytes2bits(output_diff))
		result += (guess_keys(round0[4:],round1[4:],output_diff))
		#print(len(result))

print(Counter(result))


#key = [i , 41 , 6 , 62 , 14  , 44 , 25 , 62]