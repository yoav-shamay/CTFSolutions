from pwn import *
from sage.all import *
from Crypto.Util.number import long_to_bytes
from string import ascii_letters, digits


conn = remote("saturn.picoctf.net", 53175)
conn.recvuntil("anger = ")
enc = int(conn.recvline().strip())
conn.recvuntil("envy = ")
e = 65537
d = int(conn.recvline().strip())
divisible_by_thing = e * d - 1 # divisible by (p-1)(q-1)
factors = factor(divisible_by_thing)
factor_list = list(factors)
act_factor_list = []
for fact, amt in factor_list:
    for i in range(amt):
        act_factor_list.append(fact)
print(len(act_factor_list)) # might need luck to be small
subsets = 3 ** len(act_factor_list)
for i in range(subsets):
    p_minus_1 = 1
    q_minus_1 = 1
    cpy = i
    cur = 0
    while cpy > 0:
        if cpy % 3 == 1:
            p_minus_1 *= act_factor_list[cur]
        elif cpy % 3 == 2:
            q_minus_1 *= act_factor_list[cur]
        cur += 1
        cpy //= 3
    if pow(e, -1, p_minus_1 * q_minus_1) == d:
        p = p_minus_1 + 1
        q = q_minus_1 + 1
        if is_prime(p) and is_prime(q):
            n = p * q
            dec = pow(enc, d, n)
            dec_bytes = long_to_bytes(dec)
            if len(dec_bytes) == 16 and all(chr(x) in (ascii_letters + digits) for x in dec_bytes):
                conn.sendline(long_to_bytes(dec))
                conn.interactive()
    if i % 100000 == 0:
        print(i, "/", subsets) # progress indicator
