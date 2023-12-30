from pwn import *
import itertools
import string
import hashlib
from Crypto.Util.number import *
#context.log_level = 'debug'
import time
start = time.time()
#io = process(['python3','Padding.py'])
io = remote('8.222.191.182',11111)

def proof(io):
    io.recvuntil(b"XXXX+")
    suffix = io.recv(16).decode("utf8")
    io.recvuntil(b"== ")
    cipher = io.recvline().strip().decode("utf8")
    for i in itertools.product(string.ascii_letters+string.digits, repeat=4):
        x = "{}{}{}{}".format(i[0],i[1],i[2],i[3])
        proof=hashlib.sha256((x+suffix.format(i[0],i[1],i[2],i[3])).encode()).hexdigest()
        if proof == cipher:
            break
    print(x)
    io.sendlineafter(b"XXXX:",x.encode())

def send_payload(m):
	io.recvuntil(b'Try unlock:')
	io.sendline(m.hex().encode())
	return io.recvline()

def enc2text(X,Y,D_iv):
	box = [X,Y,X,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y]
	return xor(box,D_iv)

def search_TOP2(BIV,BC):
	#diff_box = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 81, 82, 83, 84, 85, 86, 80, 87, 10, 11, 12, 13, 14, 15, 89, 90, 91, 92, 93, 94, 88, 95]

	diff_box = [ord(b'N')^ord(b'C')]
	#diff_box = [85]
	#diff_box = [85]
	D_iv = bytearray(BIV)
	for k in range(0xff):
		times = 0
		for i in range(0,0xff,2):
			#check = bytearray(BIV)
			D_iv[14] = k
			D_iv[15] = i
			payload = bytes(D_iv)+BC
			result = send_payload(payload)
			if b'Bad key... do you even try?' in result:
				print(result)
				print(list(D_iv))
				times +=1
				break
		if times:break

	cache = D_iv[14]
	time = 0
	for diff in diff_box:
		D_iv[14] = cache^diff
		for i in range(0xff):
			D_iv[13] = i
			payload = bytes(D_iv)+BC
			result = send_payload(payload)
			if b'Bad key... do you even try?' in result:
				print(result,'test:',diff)
				result_diff = diff
				D_iv[13] = i^diff
				time += 1
				break
		if time==0:
			D_iv[15] ^= 1
			for i in range(0xff):
				D_iv[13] = i
				payload = bytes(D_iv)+BC
				result = send_payload(payload)
				if b'Bad key... do you even try?' in result:
					print(result,'test:',diff)
					result_diff = diff
					D_iv[13] = i^diff
					time += 1
					break
		#if time:break
	return D_iv,result_diff

def oracle_block(BIV,BC):
	D_iv,diff = search_TOP2(BIV,BC)
	for _ in range(12,1,-1):
		for i in range(0xff):
			D_iv[_] = i
			payload = bytes(D_iv)+BC
			result = send_payload(payload)
			if b'Bad key' in result:
				print(result)
				D_iv[_] = i^diff
				break
	
	#print(list(D_iv))
	#print(list(bytearray(BIV)))
	
	diff_box = {'0': [(48, 48), (49, 49), (50, 50), (51, 51), (52, 52), (53, 53), (54, 54), (55, 55), (56, 56), (57, 57), (97, 97), (98, 98), (99, 99), (100, 100), (101, 101), (102, 102)], '1': [(48, 49), (49, 48), (50, 51), (51, 50), (52, 53), (53, 52), (54, 55), (55, 54), (56, 57), (57, 56), (98, 99), (99, 98), (100, 101), (101, 100)], '2': [(48, 50), (49, 51), (50, 48), (51, 49), (52, 54), (53, 55), (54, 52), (55, 53), (97, 99), (99, 97), (100, 102), (102, 100)], '3': [(48, 51), (49, 50), (50, 49), (51, 48), (52, 55), (53, 54), (54, 53), (55, 52), (97, 98), (98, 97), (101, 102), (102, 101)], '4': [(48, 52), (49, 53), (50, 54), (51, 55), (52, 48), (53, 49), (54, 50), (55, 51), (97, 101), (98, 102), (101, 97), (102, 98)], '5': [(48, 53), (49, 52), (50, 55), (51, 54), (52, 49), (53, 48), (54, 51), (55, 50), (97, 100), (99, 102), (100, 97), (102, 99)], '6': [(48, 54), (49, 55), (50, 52), (51, 53), (52, 50), (53, 51), (54, 48), (55, 49), (98, 100), (99, 101), (100, 98), (101, 99)], '7': [(48, 55), (49, 54), (50, 53), (51, 52), (52, 51), (53, 50), (54, 49), (55, 48), (97, 102), (98, 101), (99, 100), (100, 99), (101, 98), (102, 97)], '8': [(48, 56), (49, 57), (56, 48), (57, 49)], '9': [(48, 57), (49, 56), (56, 49), (57, 48)], '81': [(48, 97), (50, 99), (51, 98), (52, 101), (53, 100), (55, 102), (97, 48), (98, 51), (99, 50), (100, 53), (101, 52), (102, 55)], '82': [(48, 98), (49, 99), (51, 97), (52, 102), (54, 100), (55, 101), (97, 51), (98, 48), (99, 49), (100, 54), (101, 55), (102, 52)], '83': [(48, 99), (49, 98), (50, 97), (53, 102), (54, 101), (55, 100), (97, 50), (98, 49), (99, 48), (100, 55), (101, 54), (102, 53)], '84': [(48, 100), (49, 101), (50, 102), (53, 97), (54, 98), (55, 99), (97, 53), (98, 54), (99, 55), (100, 48), (101, 49), (102, 50)], '85': [(48, 101), (49, 100), (51, 102), (52, 97), (54, 99), (55, 98), (97, 52), (98, 55), (99, 54), (100, 49), (101, 48), (102, 51)], '86': [(48, 102), (50, 100), (51, 101), (52, 98), (53, 99), (55, 97), (97, 55), (98, 52), (99, 53), (100, 50), (101, 51), (102, 48)], '80': [(49, 97), (50, 98), (51, 99), (52, 100), (53, 101), (54, 102), (97, 49), (98, 50), (99, 51), (100, 52), (101, 53), (102, 54)], '87': [(49, 102), (50, 101), (51, 100), (52, 99), (53, 98), (54, 97), (97, 54), (98, 53), (99, 52), (100, 51), (101, 50), (102, 49)], '10': [(50, 56), (51, 57), (56, 50), (57, 51)], '11': [(50, 57), (51, 56), (56, 51), (57, 50)], '12': [(52, 56), (53, 57), (56, 52), (57, 53)], '13': [(52, 57), (53, 56), (56, 53), (57, 52)], '14': [(54, 56), (55, 57), (56, 54), (57, 55)], '15': [(54, 57), (55, 56), (56, 55), (57, 54)], '89': [(56, 97), (97, 56)], '90': [(56, 98), (57, 99), (98, 56), (99, 57)], '91': [(56, 99), (57, 98), (98, 57), (99, 56)], '92': [(56, 100), (57, 101), (100, 56), (101, 57)], '93': [(56, 101), (57, 100), (100, 57), (101, 56)], '94': [(56, 102), (102, 56)], '88': [(57, 97), (97, 57)], '95': [(57, 102), (102, 57)]}
	print(diff)
	key = diff_box[str(diff)]
	key = [(ord('N'),(ord('C')))]
	print(key)
	text = []
	for (i,k) in key:
		text.append(xor(BIV,enc2text(i,k,D_iv)))
	return text


def attack(enc):
	block = [enc[16*i:16*(i+1)] for i in range(len(enc)//16)]
	for i in range(1,len(block)):
		result = oracle_block(block[i-1],block[i])
		print(result)
		break

proof(io)
io.recvuntil(b'key:')
enc = bytes.fromhex(io.recvline()[:-1].decode())
attack(enc)
end = time.time()
print(end - start)

