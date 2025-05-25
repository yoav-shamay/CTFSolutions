import math
import hashlib
import sys
from tqdm import tqdm
import functools
import numpy as np
ITERS = int(2e7)
VERIF_KEY = "96cc5f3b460732b442814fd33cf8537c"
ENCRYPTED_FLAG = bytes.fromhex("42cbbce1487b443de1acf4834baed794f4bbd0dfe7d7086e788af7922b")
mod = 10 ** 10000
sys.set_int_max_str_digits(10000)

def mat_mul(a, b):
    n = len(a)
    m = len(b[0])
    mid = len(b)
    res = [[0 for i in range(m)] for i in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(mid):
                res[i][j] += a[i][k] * b[k][j]
            res[i][j] %= mod
    return res

def mat_pow(a, exp):
    if exp == 0:
        l = len(a)
        id = [[0 for i in range(l)] for i in range(l)]
        for i in range(l):
            id[i][i] = 1
        return id
    r = mat_pow(a, exp // 2)
    r = mat_mul(r, r)
    if exp % 2 == 1:
        r = mat_mul(r, a)
    return r

# This will overflow the stack, it will need to be significantly optimized in order to get the answer :)
@functools.cache
def m_func(i):
    start = [[1],[2],[3],[4]]
    matrix = [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [55692, -9549, 301, 21]]
    exponent = i - 3
    matrix_exp = mat_pow(matrix, exponent)
    res = mat_mul(matrix_exp, start)
    return res[3][0]


# Decrypt the flag
def decrypt_flag(sol):
    sol = sol % (10**10000)
    sol = str(sol)
    sol_md5 = hashlib.md5(sol.encode()).hexdigest()

    if sol_md5 != VERIF_KEY:
        print("Incorrect solution")
        sys.exit(1)

    key = hashlib.sha256(sol.encode()).digest()
    flag = bytearray([char ^ key[i] for i, char in enumerate(ENCRYPTED_FLAG)]).decode()

    print(flag)

if __name__ == "__main__":
    sol = m_func(ITERS)
    decrypt_flag(sol)
