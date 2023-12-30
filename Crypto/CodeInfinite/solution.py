from sage.all import *
from pwn import *
from gmpy2 import invert
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long,long_to_bytes
context(log_level = 'debug')
'''
PR.<a,b> = PolynomialRing(ZZ)
fs = []

Points = [(1504506045507279311346465773007772381512657984660547838789,4130578488225601501046056663631811064903654176857402074305),(5456905820281037859191198823390307260694730874414431398113,1453400382002547044807491448625262356474889271722046728491),(3369157190983746749932999294786837203985061363351766479528,5420818021877363417659329892069605959140325330921339586332),(1570225709466522856398929258259165219330193412683012975450,3674471623793502486481847125571931939478634329517055334651)]
for (x,y) in Points:
    f = x^3 + a*x + b - y^2
    fs.append(f)
    print(f)
I = Ideal(fs)
I.groebner_basis()
'''

# Finite field prime
p = 0xfffffffffffffffffffffffffffffffeffffffffffffffff
# Create a finite field of order p
FF = GF(p)
a = p - 3
# Curve parameters for the curve equation: y^2 = x^3 + a*x +b

# Define NIST 192-P
b192 = 0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1
n192 = 0xffffffffffffffffffffffff99def836146bc9b1b4d22831
P192 = EllipticCurve([FF(a), FF(b192)])

# small parts have kgv of 197 bits
#   0 : 2^63 * 3 * 5 * 17 * 257 * 641 * 65537 * 274177    * 6700417 * 67280421310721
# 170 : 73 * 35897 * 145069 * 188563 * 296041             * 749323 * 6286019 * 62798669238999524504299
# print_curves()

# get flag pub key
r = remote('115.159.221.202',int(11112))

r.recvline()
r.recvline()
res = r.recvline().decode()
res = res.replace('The secret is ','')

r.recvuntil(b"Alice's public key is (")
x = int(r.recvuntil(b",", drop=True).decode())
y = int(r.recvuntil(b")", drop=True).decode())
A = P192(x, y)


enc = bytes.fromhex(res)

# Find private key
mods = []
vals = []

for b in [0, 170]:
    E = EllipticCurve([FF(a), FF(b)])
    G = E.gens()[0]
    factors = sage.rings.factorint.factor_trial_division(G.order(), 300000)
    G *= factors[-1][0]

    r.sendlineafter(b"Give me your pub key's x : \n", str(G.xy()[0]).encode())
    r.sendlineafter(b"Give me your pub key's y : \n", str(G.xy()[1]).encode())
    r.recvuntil(b"(")
    x = int(r.recvuntil(b",", drop=True).decode())
    y = int(r.recvuntil(b")", drop=True).decode())
    H = E(x, y)

    # get dlog
    tmp = G.order()
    mods.append(tmp)
    vals.append(G.discrete_log(H,tmp))

r.close()
pk = CRT_list(vals, mods)
print(pk, A)

key = long_to_bytes(pk)[:16]
Cipher = AES.new(key,AES.MODE_ECB)
flag = Cipher.decrypt(enc)

print(flag)