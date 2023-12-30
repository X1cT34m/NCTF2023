from operator import add
from typing import List
from functools import reduce
from gmpy2 import *
from Crypto.Util.number import long_to_bytes,bytes_to_long
from copy import copy
from DES import *

ROTATIONS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

__pc1 = [56, 48, 40, 32, 24, 16,  8,
	  0, 57, 49, 41, 33, 25, 17,
	  9,  1, 58, 50, 42, 34, 26,
	 18, 10,  2, 59, 51, 43, 35,
	 62, 54, 46, 38, 30, 22, 14,
	  6, 61, 53, 45, 37, 29, 21,
	 13,  5, 60, 52, 44, 36, 28,
	 20, 12,  4, 27, 19, 11,  3
]
__pc2 = [
	13, 16, 10, 23,  0,  4,
	 2, 27, 14,  5, 20,  9,
	22, 18, 11,  3, 25,  7,
	15,  6, 26, 19, 12,  1,
	40, 51, 30, 36, 46, 54,
	29, 39, 50, 44, 32, 47,
	43, 48, 38, 55, 33, 52,
	45, 41, 49, 35, 28, 31
]


__pc2_inv = [
	4, 23, 6, 15, 5, 9, 19, 
	17, 11, 2, 14, 22, 0, 8, 
	18, 1, 13, 21, 10, 12, 3, 
	16, 20, 7, 46, 30, 26, 47, 
	34, 40, 45, 27, 38, 31, 24, 
	43, 36, 33, 42, 28, 35, 37, 
	44, 32, 25, 41, 29, 39
]

def PC_1(key: List[int]) -> List[int]:
    return [key[x] for x in __pc1]

def PC_2(key: List[int]) -> List[int]:
    return [key[x] for x in __pc2]

def PC_2_inv(key: List[int]) -> List[int]:
    return [key[x] for x in __pc2_inv]


def get_sub_key(key: List[int]) -> List[List[int]]:
    key = PC_1(key)
    L, R = key[:28], key[28:]

    sub_keys = []

    for i in range(16):
        for j in range(ROTATIONS[i]):
            L.append(L.pop(0))
            R.append(R.pop(0))

        combined = L + R
        if i == 15:test = combined
        sub_key = PC_2(combined)
        sub_keys.append(sub_key)
    return sub_keys,test

def bytes2bits(bytes):
	result = reduce(add, [list(map(int, bin(byte)[2:].zfill(8))) for byte in bytes])
	return result

def recover(key):
	L,R = key[:28], key[28:]
	sub_keys = []
	ROTATIONS_inv = ROTATIONS[::-1]
	sub_keys.append(PC_2(L+R))
	for i in range(15):
		for j in range(ROTATIONS_inv[i]):
			L.insert(0,L.pop(-1))
			R.insert(0,R.pop(-1))
		combined = L + R
		sub_key = PC_2(combined)
		sub_keys.append(sub_key)
	return sub_keys[::-1]

def explore(orin_key):
	orin_key = PC_2_inv(orin_key)
	keys = []
	for k in range(256):
		key = copy(orin_key)
		k = bin(k)[2:].zfill(8)
		key.insert(8,int(k[0]))
		key.insert(17,int(k[1]))
		key.insert(21,int(k[2]))
		key.insert(24,int(k[3]))
		key.insert(34,int(k[4]))
		key.insert(37,int(k[5]))
		key.insert(42,int(k[6]))
		key.insert(53,int(k[7]))
		keys.append(recover(key))
	return keys

def key2keys(key):
	result = []
	for i in key:
		result += [int(i) for i in bin(i)[2:].zfill(6)]
	return result
f = open('data.txt','w')

for i in range(256):
	key = [i , 41 , 6 , 62 , 14  , 44 , 25 , 62]
	key2keys(key)

	from operator import add

	result = explore(key2keys(key))
	enc1=['e392ac8bb916a1c4', '20a10deb74576ae9', 'd186e0fc220a67f9', '17ce709d69048488', 'a2f945212d4684da']
	#enc2=['d6f79f862e21cbc7', '2185586bf0fd7ef8', '39c735debc3793bb', 'e3fa91b0b26e358d', '4be9f65d2d85ae9d']

	for tmp_key in result:
		flag = b''
		for ct in enc1:
			ct = bytes.fromhex(ct)
			ct = bytes2bits(ct)
			pt = decrypt(ct,tmp_key)
			flag +=bits2bytes(pt)
			break
		f.write(str(flag)+'\n')
	#break
f.close()
	
