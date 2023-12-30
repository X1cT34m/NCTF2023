#!/usr/local/bin/sage
import random
from sever import *
from secret import flag
from Crypto.Util.number import getPrime

class Party():
    def __init__(self,N,q,seed=None):
        self.N = N
        self.q = q
        PRq.<a> = PolynomialRing(Zmod(q))
        self.Rq = PRq.quotient(a^N - 1, 'x')
        self.q_length = q.bit_length()
        self.a = self.Derive_a(seed)
        self.s = self.Sample_s()
        self.e = self.Sample_e()
        self.pk = self.a * self.s + 2*self.e

    def sig(self,y):
        b = random.choice([0, 1])
        if b:
            return int(not(y >= -floor(self.q/4) + 1 and y <= floor(self.q/4) + 1))
        else:
            return int(not(y >= -floor(self.q/4) and y <= floor(self.q/4)))
    
    def Mod2(self,x):
        self.key = []
        self.w = []
        for i in range(self.N):
            if x[i] >(self.q-1)/2:
                x[i] = (x[i]-(self.q-1))
            self.w.append(self.sig(x[i]))
            self.key.append(((x[i]+self.w[i]*(self.q-1)/2)%self.q)%2)

    def Mod2_(self,x,w):
        self.key = []
        for i in range(self.N):
            if x[i] >(self.q-1)/2:
                x[i] = (x[i]-(self.q-1))
            self.key.append(((x[i]+self.w[i]*(self.q-1)/2)%self.q)%2)

    def Derive_a(self,seed):
        a = []
        if seed == None:
              self.g = random.Random()
        else: self.g = random.Random(seed)
        base = pow(2,self.q_length - log(self.N,2))
        nonce = self.g.randint(0,base)
        for _ in range(self.N):
            nonce += self.g.randint(0,base)
            a.append(nonce)
        return self.Rq(a)

    def Sample_s(self):
        s = []
        for _ in range(self.N):
            if random.random() < 0.5:
                s.append(1)
            else:
                s.append(0)
        return self.Rq(s)

    def Sample_e(self):
        e = [random.randrange(int(0),int(2)) for _ in range(self.N)]
        return self.Rq(e)

    def recv(self,pk,w=None):
        pk = self.Rq(pk)
        x = list(map(int,(pk*self.s).list()))
        if w:
            self.Mod2_(x,w)
        else:
            self.Mod2(x)
    def send(self):
        self.s = self.Sample_s()
        return list(self.a*self.s)


def rcv2list(data):
    data = data.decode()
    data = data.replace('[','')
    data = data.replace(']','')
    data = data.split(',')
    data = list(map(int,data))
    return data


MENU = b"""
 Welcome to March 7th's Party!
/----------------------------\\
|          options           |
| [1]Play With Bob           |
| [2]Check Bob's Secret      |
| [3]Quit The Party          |
\\---------------------------/
"""




class test(Task):
    def check(self,answer,bob_s):
        if answer == bob_s:
            self.send(flag)
        else:
            self.send(b'Oops,Something wrong?')

    def handle(self):
        if not self.proof_of_work():
            self.send(b'[!] Wrong!')
            return
        signal.signal(signal.SIGALRM, self.timeout_handler)
        signal.alarm(320)
        N,length = 128,2042
        q = getPrime(length)
        PRq.<a> = PolynomialRing(Zmod(q))
        Rq = PRq.quotient(a^N - 1, 'x')  
        self.send((f"Before The Party begin,we need to check your key!").encode())
        self.send((f"N = {N}\nq = {q}\n").encode())

        self.send(b'plz tell me your seed:')
        seed = int(self.recv())
        self.send(b'plz tell me your public key:')
        Eve_pk = rcv2list(self.recv())
        assert type(Eve_pk) == list
        Eve_pk = Rq(Eve_pk)

        alice = Party(N,q,seed)
        alice.recv(Eve_pk)
        self.send(b"Here are alice's answer:")
        self.send(  str(list(alice.pk)).encode()  )
        self.send(  str(list(alice.w)).encode()  )

        self.send(b"Plz tell me the alice's secret,if you want to Enjoy the Party")
        answer = rcv2list(self.recv())
        assert type(answer) == list

        if answer == list(alice.s):
            bob = Party(N,q,randrange(0,q))
            self.send(b"Let's Enjoy The Party Now!")
            self.send(MENU)
            while True:
                choice = int(self.recv())
                if choice == 1:
                    self.send(  str(bob.send()).encode()  ) 
                elif choice == 2:
                    self.send((f"Tell me Bob's secret,if you want to get the FLAG").encode())
                    answer = rcv2list(self.recv())
                    self.check(answer,list(bob.s))
                elif choice == 3:
                    self.send(b"see you~")
                    quit()
        else:
            self.send(b"[!] Wrong!")


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 11110
    server = ForkedServer((HOST, PORT), test)
    server.allow_reuse_address = True
    print(HOST, PORT)
    server.serve_forever()