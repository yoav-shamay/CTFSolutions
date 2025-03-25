import requests
import urllib.parse
import base64
from functools import cache

BLOCK_SIZE = 16

@cache
def test_padding(ciphertext):
    url = f"https://c574849affcad56d.247ctf.com/get_flag?password={urllib.parse.quote_plus(base64.b64encode(ciphertext))}"
    #print(url)
    out = requests.get(url).text
    if "Something went wrong!" in out:
        return False
    return True

def xor_bytes(a, b):
    res = b""
    for i, j in zip(a, b):
        res += int.to_bytes(i ^ j)
    return res


# Assumes padding in prefix bytes, flip for most cases
def decrypt_block(ciphertext_block):
    plaintext = b"a" * 16
    for i in range(BLOCK_SIZE):
        required = int.to_bytes(i + 1) * 16
        possiblities = []
        for j in range(256):
            plaintext = plaintext[:i] + j.to_bytes() + plaintext[(i + 1):]
            if test_padding(xor_bytes(plaintext, required) + ciphertext_block):
                possiblities.append(int.to_bytes(j))
                if i != 0:
                    break
        assert(len(possiblities) > 0)
        if len(possiblities) > 1:
            new_possibilities = []
            plaintext = plaintext[:(i + 1)] + b'b' + plaintext[(i + 2):]
            for poss in possiblities:
                plaintext = plaintext[:i] + poss + plaintext[(i + 1):]
                if test_padding(xor_bytes(plaintext, required) + ciphertext_block):
                    new_possibilities.append(int.to_bytes(j))
            assert len(new_possibilities) == 1
            possiblities = new_possibilities
        plaintext = plaintext[:i] + possiblities[0] + plaintext[(i + 1):]
        print(repr(plaintext))
    return plaintext

# For the specific padding of the challenge. In a real case match for details (padding in every block / only last, padding as prefix / suffix)
def create_blocks(text):
    blocks = []
    padding = 16 - (len(text) % 16)
    first_block_length = 16 - padding
    blocks.append(padding.to_bytes() * padding + text[:first_block_length])
    for i in range(first_block_length, len(text), 16):
        blocks.append(text[i:])
    return blocks

# First 16 bytes are IV.
def encrypt(blocks):
    ciphertext_blocks = []
    ciphertext_blocks.append(b"a" * 16)
    for block in blocks[::-1]:
        decrypted = decrypt_block(ciphertext_blocks[-1])
        xor = xor_bytes(decrypted, block)
        ciphertext_blocks.append(xor)
    ciphertext_blocks = ciphertext_blocks[::-1]
    ciphertext = b"".join(ciphertext_blocks)
    return ciphertext


requested_text = b"secret_admin_password"
blocks = create_blocks(requested_text)
print(blocks)
ciphertext = encrypt(blocks)
url = f"https://c574849affcad56d.247ctf.com/get_flag?password={urllib.parse.quote_plus(base64.b64encode(ciphertext))}"
print(url)
