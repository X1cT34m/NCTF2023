#!/usr/local/bin/python

from os import urandom
from secret import secret
from util import *

if not proof_of_work():
    print("[!] Wrong!")
    quit()

flag = 'NCTF{'+secret+'}'

secret = secret.encode()
key = bytes2bits(urandom(8))
key_ = get_sub_key(key)
lenth = len(secret)
block = [secret[8 * i : 8 * (i+1)] for i in range(lenth//8)]

enc1 = []
enc2 = []

for i in block:
	i = bytes2bits(i)
	ct0 = encrypt(i,key_)
	ct1 = encrypt(i,key_,1)
	enc1.append(bits2bytes(ct0).hex())
	enc2.append(bits2bytes(ct1).hex())

print(f'enc1={enc1}')
print(f'enc2={enc2}')