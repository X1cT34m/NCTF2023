#!/usr/local/bin/sage
from util import *
from secret import flag
from sage.all import *

def input2list(data):
    data = data.replace('[','')
    data = data.replace(']','')
    data = data.split(',')
    data = list(map(int,data))
    return data

def check(self,answer,bob_s):
    if answer == bob_s:
        print(flag)
    else:
        print(b'Oops,Something wrong?')

MENU = b"""
 Welcome to March 7th's Party!
/----------------------------\\
|          options           |
| [1]Play With Bob           |
| [2]Check Bob's Secret      |
| [3]Quit The Party          |
\\---------------------------/
"""
N,length = 128,2042
q = getPrime(int(length))
PRq.<a> = PolynomialRing(Zmod(q))
Rq = PRq.quotient(a^N - 1, 'x')  


if not proof_of_work():
    print('[!] Wrong!')
    quit()

print(("Before The Party begin,we need to check your key!"))
print(("N = {N}\nq = {q}\n"))

print('plz tell me your seed:')
seed = int(intput('>'))
print('plz tell me your public key:')
Eve_pk = input2list(intput('>'))
assert type(Eve_pk) == list
Eve_pk = Rq(Eve_pk)

alice = Party(N,q,seed)
alice.recv(Eve_pk)
print("Here are alice's answer:")
print( list(alice.pk) )
print( list(alice.w) )

print("Plz tell me the alice's secret,if you want to Enjoy the Party")
answer = input2list(intput('>'))
assert type(answer) == list

if answer == list(alice.s):
    bob = Party(N,q,randrange(0,q))
    print("Let's Enjoy The Party Now!")
    print(MENU)
    while True:
        choice = int(intput('>'))
        if choice == 1:
            print(  bob.send() ) 
        elif choice == 2:
            printd("Tell me Bob's secret,if you want to get the FLAG")
            answer = input2list(intput('>'))
            check(answer,list(bob.s))
        elif choice == 3:
            print("see you~")
            quit()
else:
    print("[!] Wrong!")