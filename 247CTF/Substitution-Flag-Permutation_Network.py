import random
flag = "???"

rounds = 5
block_size = 8
sa = {
    0: 15, 
    1: 2, 
    2: 14, 
    3: 0, 
    4: 1, 
    5: 3, 
    6: 10, 
    7: 6, 
    8: 4, 
    9: 11, 
    10: 9, 
    11: 7, 
    12: 13, 
    13: 12, 
    14: 8, 
    15: 5
}
sb = {
    0: 12, 
    1: 8, 
    2: 13, 
    3: 6, 
    4: 9, 
    5: 1, 
    6: 11, 
    7: 14, 
    8: 5, 
    9: 10, 
    10: 3, 
    11: 4, 
    12: 0, 
    13: 15, 
    14: 7, 
    15: 2
}

sa_rev = {}
sb_rev = {}

for x, y in sa.items():
    sa_rev[y] = x
for x, y in sb.items():
    sb_rev[y] = x

key = [random.randrange(255), random.randrange(255)] * 4
to_bin = lambda x, n=block_size: format(x, "b").zfill(n)
to_int = lambda x: int(x, 2)
to_chr = lambda x: "".join([chr(i) for i in x])
to_ord = lambda x: [ord(i) for i in x]
bin_join = lambda x, n=int(block_size / 2): (str(x[0]).zfill(n) + str(x[1]).zfill(n))
bin_split = lambda x: (x[0 : int(block_size / 2)], x[int(block_size / 2) :])
str_split = lambda x: [x[i : i + block_size] for i in range(0, len(x), block_size)]
xor = lambda x, y: x ^ y

def s(a, b):
    return sa[a], sb[b]

perm = [5,2,3,1,6,0,7,4]
inv = [0] * 8

for i, x in enumerate(perm):
    inv[x] = i

def permutate(a, p=perm):
    return ''.join([a[i] for i in p])

def get_keys(k):
    return [
        k[i : i + int(block_size)] + k[0 : (i + block_size) - len(k)]
        for i in range(rounds)
    ]

def xor_arrays(state, k):
    return [xor(state[i], k[i]) for i in range(len(state))]

def encrypt(e):
    encrypted = []
    for i in e:
        a, b = bin_split(to_bin(ord(i)))
        tsa, tsb = sa[to_int(a)], sb[to_int(b)]
        pe = permutate(
            bin_join((to_bin(tsa, int(block_size / 2)), to_bin(tsb, int(block_size / 2))))
        )
        encrypted.append(to_int(pe))
    return encrypted

def r(p, k):
    keys = get_keys(k)
    state = str_split(p)
    for b in range(len(state)):
        for i in range(rounds):
            rk = xor_arrays(to_ord(state[b]), keys[i])
            state[b] = to_chr(encrypt(to_chr(rk)))
    return [ord(e) for es in state for e in es]

def decrypt(e):
    decrypted = ""
    for i in e:
        pe = permutate(to_bin(i), inv)
        a, b = bin_split(pe)
        tsa = to_int(a)
        tsb = to_int(b)
        a = sa_rev[tsa]
        b = sb_rev[tsb]
        decrypted += chr(to_int(bin_join([to_bin(a, 4), to_bin(b, 4)])))
    return decrypted

def reverse(enc, k):
    keys = get_keys(k)
    res = ""
    for i in range(0, len(enc), block_size):
        cur = to_chr(enc[i:i+8])
        for i in range(rounds):
            cur = to_ord(cur)
            cur = to_ord(decrypt(cur))
            cur = to_chr(xor_arrays(cur, keys[i]))
        res += cur
    return res

encrypted = [190, 245, 36, 15, 132, 103, 116, 14, 59, 38, 28, 203, 158, 245, 222, 157, 36, 100, 240, 206, 36, 205, 51, 206, 90, 212, 222, 245, 83, 14, 222, 206, 163, 38, 59, 157, 83, 203, 28, 27]
for i in range(255):
    for j in range(255):
        keys = [i, j] * 4
        res = reverse(encrypted, keys)
        assert(r(res, keys) == encrypted)
        if res.startswith("247CTF{"):
            print(res)
