# Sage
from Crypto.Util.number import *
from secret import flag
class NTRU:
    def __init__(self, N, p, q, d):
        self.debug = False

        assert q > (6*d+1)*p
        assert is_prime(N)
        assert gcd(N, q) == 1 and gcd(p, q) == 1
        self.N = N
        self.p = p
        self.q = q
        self.d = d
      
        self.R_  = PolynomialRing(ZZ,'x')
        self.Rp_ = PolynomialRing(Zmod(p),'xp')
        self.Rq_ = PolynomialRing(Zmod(q),'xq')
        x = self.R_.gen()
        xp = self.Rp_.gen()
        xq = self.Rq_.gen()
        self.R  = self.R_.quotient(x^N - 1, 'y')
        self.Rp = self.Rp_.quotient(xp^N - 1, 'yp')
        self.Rq = self.Rq_.quotient(xq^N - 1, 'yq')

        self.RpOrder = self.p^self.N - self.p
        self.RqOrder = self.q^self.N - self.q
        self.sk, self.pk = self.keyGen()

    def T(self, d1, d2):
        assert self.N >= d1+d2
        t = [1]*d1 + [-1]*d2 + [0]*(self.N-d1-d2)
        shuffle(t)
        return self.R(t)

    def lift(self, fx):
        mod = Integer(fx.base_ring()(-1)) + 1
        return self.R([Integer(x)-mod if x > mod//2 else x for x in list(fx)])

    def keyGen(self):
        fx = self.T(self.d+1, self.d)
        gx = self.T(self.d, self.d)

        Fp = self.Rp(list(fx)) ^ (-1)                         
        assert pow(self.Rp(list(fx)), self.RpOrder-1) == Fp 
        assert self.Rp(list(fx)) * Fp == 1                
        
        Fq = pow(self.Rq(list(fx)), self.RqOrder - 1)   
        assert self.Rq(list(fx)) * Fq == 1              
        
        hx = Fq * self.Rq(list(gx))

        sk = (fx, gx, Fp, Fq, hx)
        pk = hx
        return sk, pk

    def getKey(self):
        ssk = (
              self.R_(list(self.sk[0])),   
              self.R_(list(self.sk[1]))   
            )
        spk = self.Rq_(list(self.pk)) 
        return ssk, spk
     
    def pad(self,msg):
        pad_length = self.N - len(msg)
        msg += [-1 for _ in range(pad_length)]
        return msg
    
    def encode(self,msg):
        result = []
        for i in msg:
            result += [int(_) for _ in bin(i)[2:].zfill(8)]
        if len(result) < self.N:result = self.pad(result)
        result = self.R(result)
        return result


    def encrypt(self, m):
        m = self.encode(m)
        assert self.pk != None
        hx = self.pk
        mx = self.R(m)
        mx = self.Rp(list(mx))            
        mx = self.Rq(list(mx))   

        rx = self.T(self.d, self.d)
        rx = self.Rq(list(rx))
        
        e = self.p * rx * hx + mx
        return list(e)

if __name__ == '__main__':
    ntru = NTRU(N=509, p=3, q=512, d=3)
    assert len(flag) == 42
    sk, pk = ntru.getKey()
    print("fx = " , sk[0].list())
    print("gx = " , sk[1].list())
    print("hx = " , pk.list())

    e = ntru.encrypt(flag)
    print(f'e={e}')