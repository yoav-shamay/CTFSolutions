import requests
import base64
import json
url = "https://08e607f01d74873f.247ctf.com/encrypt"
next_iv = b"?"
session_cookie = ""
def encrypt(text):
    assert len(text) <= 32
    global next_iv, session_cookie
    resp = requests.get(f'{url}?plaintext={text.hex()}', cookies={"session": session_cookie})
    if "Too Predictable" in resp.text:
        assert False
    res = bytes.fromhex(resp.text)
    next_iv = res[-16:]
    # verify next iv from session
    sess = resp.cookies["session"]
    session_cookie = sess
    payload = (sess.split('.')[0])
    while len(payload) % 4 != 0:
        payload += "="
    payload_json = (base64.b64decode(payload))
    payload_object = json.loads(payload_json.decode())
    iv = base64.b64decode(payload_object["IV"][" b"])
    assert iv == next_iv
    return res

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))
encrypt(b"a") # initialize IV

base = b"a" * 16
encrypted_first_block = encrypt(xor(base, next_iv))[:16]
flag_length = 32
flag = ""
alphabet = r"0123456789abcdef"
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
        plaintext_guess = xor(base, next_iv) + xor(xor(guess, encrypted_xor), encrypted_first_block)
        enc_guess = encrypt(plaintext_guess)
        assert enc_guess[:16] == encrypted_first_block
        if enc_guess[16:32] == encrypted:
            flag += char
            break
    assert (len(flag) == (i + 1))
    print(flag)
