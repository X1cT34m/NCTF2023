#!/usr/local/bin/python

from util import *
from secret import flag,a,b,p
from random import randrange
from Crypto.Cipher import AES
from Crypto.Util.number import getPrime,bytes_to_long,long_to_bytes

if not proof_of_work():
	print("[!] Wrong!")
	quit()

while True:
	try:
		curve = Curve(a,b,p)
		g = randrange(1,p)
		G = Point(g,curve.find_y(g),curve)
		PK = randrange(1,p)
		pub = PK * G
		break
	except:
		continue

key = long_to_bytes(PK)[:16]
Cipher = AES.new(key,AES.MODE_ECB)
enc = Cipher.encrypt(flag)

print(f"""
=============================================
The secret is {enc.hex()} 
Alice's public key is {pub}
Now send over yours !
""")
for i in range(4):
	your_pub_key_x = int(input(f"Give me your pub key's x : \n"))
	your_pub_key_y = int(input(f"Give me your pub key's y : \n"))
	your_pub_key = Point(your_pub_key_x,your_pub_key_y,curve)
	shared_key = your_pub_key * PK
	print(f"The shared key is\n {shared_key}")
