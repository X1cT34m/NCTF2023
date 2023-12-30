from sage.all import *
import os
import random
import string
from hashlib import sha256

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

def proof_of_work():
    random.seed(os.urandom(8))
    proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(20)])
    _hexdigest = sha256(proof.encode()).hexdigest()
    print(f"[+] sha256(XXXX+{proof[4:]}) == {_hexdigest}")
    x = input(prompt=b'[+] Plz tell me XXXX: ').encode()
    if len(x) != 4 or sha256(x+proof[4:].encode()).hexdigest() != _hexdigest:
        return False
    return True