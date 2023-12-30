from sage.all import *
from Crypto.Util.number import getPrime
import random
from pwn import *

from time import time
from random import randint

def orthoLattice(b,x0):
    m=b.length()
    M=Matrix(ZZ,m,m)
 
    for i in range(1,m):
        M[i,i]=1
    M[1:m,0]=-b[1:m]*inverse_mod(b[0],x0)
    M[0,0]=x0
 
    for i in range(1,m):
        M[i,0]=mod(M[i,0],x0)
 
    return M
 
def allones(v):
    if len([vj for vj in v if vj in [0,1]])==len(v):
      return v
    if len([vj for vj in v if vj in [0,-1]])==len(v):
      return -v
    return None
 
def recoverBinary(M5):
    lv=[allones(vi) for vi in M5 if allones(vi)]
    n=M5.nrows()
    for v in lv:
        for i in range(n):
            nv=allones(M5[i]-v)
            if nv and nv not in lv:
                lv.append(nv)
            nv=allones(M5[i]+v)
            if nv and nv not in lv:
                lv.append(nv)
    return Matrix(lv)
 
def allpmones(v):
    return len([vj for vj in v if vj in [-1,0,1]])==len(v)
 

def kernelLLL(M):
    n=M.nrows()
    m=M.ncols()
    if m<2*n: return M.right_kernel().matrix()
    K=2^(m//2)*M.height()
  
    MB=Matrix(ZZ,m+n,m)
    MB[:n]=K*M
    MB[n:]=identity_matrix(m)
  
    MB2=MB.T.LLL().T
  
    assert MB2[:n,:m-n]==0
    Ke=MB2[n:,:m-n].T
 
    return Ke
 
# This is the Nguyen-Stern attack, based on BKZ in the second step
def NSattack(n,m,p,b):
    M=orthoLattice(b,p)
 
    t=cputime()
    M2=M.LLL()
    MOrtho=M2[:m-n]

    t2=cputime()
    ke=kernelLLL(MOrtho)
    print('step 1 over')
    if n>170: return
 
    beta=2
    tbk=cputime()
    while beta<n:
        if beta==2:
            M5=ke.LLL()
        else:
            M5=M5.BKZ(block_size=beta)

        if len([True for v in M5 if allpmones(v)])==n: break
 
        if beta==2:
            beta=10
        else:
            beta+=10

    print('step 2 over')
    t2=cputime()
    MB=recoverBinary(M5)
    print('step 3 over')
    TMP = (Matrix(Zmod(p),MB).T)
    alpha = sorted(TMP.solve_right(b))
    return (alpha)


def p2l(pol):
    pol = str(list(pol)).encode()
    return pol

def recv2list(res):
    res = res.decode()
    print(res)
    res = res.replace('[','')
    res = res.replace(']','')
    res = res.split(',')
    res = list(map(int,res))
    return res

context(log_level = 'debug')
io = remote('8.222.191.182',int(11110))
start = time()
N = 128
io.recvuntil(b'q = ')
q = int(io.recvline())

io.sendlineafter(b'>',b'1')
PRq.<a> = PolynomialRing(Zmod(q))
Rq = PRq.quotient(a^N - 1, 'x')

Eve_e = [0 for i in range(N)]
Eve_e[0] = 1
Eve_e[1] = int(q // 8) + 1
Eve_pk = 2*Rq(Eve_e)

print(Eve_pk)
io.sendlineafter(b'>',p2l(Eve_pk))

io.recvuntil(b'answer:\n')
io.recvline()
alice_w = recv2list(io.recvline())

alice_s = alice_w[1:] + alice_w[:1]
io.sendlineafter(b'>',str(alice_s).encode())
#part1 end
h = []
io.sendlineafter(b'>',b'1')
h += eval(io.recvline())
io.sendlineafter(b'>',b'1')
h += eval(io.recvline())

#print(len(h))
#io.close()
h = vector(h)
#print(h)
alpha = NSattack(128,256,q,h)
alpha = Rq(alpha)
alpha_inv = 1/alpha

h_ = list(map(int,h))
h_ = Rq(h_[128:])

x = list(h_*alpha_inv)
print(x)

io.sendlineafter(b'>',b'2')
io.sendline( str(x).encode() )
end = time()
print(end-start)
io.interactive()