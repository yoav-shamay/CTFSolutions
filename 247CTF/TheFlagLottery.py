from pwn import *
import random
import time
while True:
    conn = remote("401b6aff80cddc34.247ctf.com", 50410)
    conn.recvline()
    t = int(time.time())
    secret = random.Random()
    secret.seed(t - 2) # offset is found by simply looking at difference between server numbers and my guessed numbers
    res = (str(secret.random())[:len("0.864928232014")])
    conn.sendline(res)
    l = conn.recvline()
    if l.startswith(b"Nope!"):
        print(l, res)
        conn.close()
        continue
    conn.interactive()
