#!/usr/local/bin/python
import random
import string
from os import urandom
from secret import secret
from Crypto.Cipher import AES
from hashlib import sha1,sha256

def proof_of_work():
    random.seed(urandom(8))
    proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(20)])
    _hexdigest = sha256(proof.encode()).hexdigest()
    print(f"[+] sha256(XXXX+{proof[4:]}) == {_hexdigest}")
    x = input('[+] Plz tell me XXXX: ').encode()
    if len(x) != 4 or sha256(x+proof[4:].encode()).hexdigest() != _hexdigest:
        return False
    return True

N = 16

def count_blocks(length):return (length) // N + 1

def find_repeat_tail(message):
    Y = message[-1]
    message_len = len(message)
    for i in range(len(message)-1, -1, -1):
        if message[i] != Y:
            X = message[i]
            message_len = i
            break
    return message_len, X, Y

def padding(msg):
    msg_lenth = len(msg)
    block_count = count_blocks(msg_lenth)
    result_lenth = block_count * N
    X = msg[(block_count-2)*N]
    Y = msg[(block_count-2)*N+1]
    msg += bytes([X])
    if len(msg)%16 == 0:result_lenth += N
    if X==Y:
        Y = Y^1
    padded = msg.ljust(result_lenth , bytes([Y]))
    return padded

def unpad(msg):
    msg_length, X, Y = find_repeat_tail(msg)
    block_count = count_blocks(msg_length)
    _X = msg[(block_count-2)*N]
    _Y = msg[(block_count-2)*N+1]
    if (Y != _Y and Y != _Y^1) or (X != _X):
        raise ValueError("Incorrect Padding")
    return msg[:msg_length]

def chal():
    key = urandom(16)
    iv = urandom(16)
    flag = ('NCTF{'+sha1(secret).hexdigest()+'}').encode()
    tmp = AES.new(key,AES.MODE_CBC,iv)
    enc = tmp.encrypt(padding(iv+flag))
    print(f"""
*******************************
It look like Padding Oracle,
But it looks a bit different?
Any way...Let's Play Game!
Here are your encrypted key:{enc.hex()}
*******************************
""")

    while True:
        enc = input("Try unlock:")
        enc = bytes.fromhex(enc)
        iv = enc[:16]
        cipher = AES.new(key,AES.MODE_CBC,iv)
        try:
            message = unpad(cipher.decrypt(enc[16:]))
            if message == flag:
                print("Hey you unlock me! At least you know how to use the key")
            else:
                print("Bad key... do you even try?")
        except ValueError:
            print("Don't put that weirdo in me!")
        except Exception:
            print("What? Are you trying to unlock me with a lock pick?")

if __name__ == "__main__":
    if not proof_of_work():
        print("[!] Wrong!")
        quit()
    chal()