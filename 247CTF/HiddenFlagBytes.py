import requests
url = "https://7ef136f2b5514302.247ctf.com/encrypt"
def encrypt(text):
    return bytes.fromhex(requests.get(f'{url}?plaintext={text.hex()}').text)

def xor(a, b):
    return b"".join([(x ^ y).to_bytes() for x,y in zip(a, b)])

base = b"a" * 16
encrypted_first_block = encrypt(base)[:16]
flag_length = len(r"247CTF{}") + 32
flag = "247CTF{"
alphabet = r"0123456789abcdefCTF{}"
for i in range(len(flag), flag_length):
    padding = 15 - (i % 16)
    text = base + b"a" * padding
    enc = encrypt(text)
    text += flag.encode()
    block_start_index = 16 + i + padding - 15
    assert block_start_index % 16 == 0
    plaintext_block_prefix = text[block_start_index:block_start_index + 15]
    encrypted = enc[block_start_index:block_start_index + 16]
    encrypted_xor = enc[block_start_index - 16:block_start_index]
    for char in alphabet:
        guess = plaintext_block_prefix + char.encode()
        plaintext_guess = base + xor(xor(guess, encrypted_xor), encrypted_first_block)
        enc_guess = encrypt(plaintext_guess)[16:32]
        if enc_guess == encrypted:
            flag += char
            break
    assert (len(flag) == (i + 1))
    print(flag)
