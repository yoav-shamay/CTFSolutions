
def gen_key(file_content):
    res = [0] * 32
    buf1 = [0] * 256
    buf2 = [0] * 256
    buf3 = [0] * 256
    i = 0
    length = len(file_content)
    while i < len(file_content):
        next_index = i
        if file_content[i] == 1:
            next_index = len(file_content)
            if i + 2 < length:
                buf1[file_content[i + 1]] = file_content[i + 2]
                next_index = i + 3
        elif file_content[i] == 2:
            next_index = len(file_content)
            if i + 2 < length:
                buf2[file_content[i + 1]] = file_content[i + 2]
                next_index = i + 3
        elif file_content[i] == 3:
            next_index = len(file_content)
            if i + 2 < length:
                b = file_content[i + 1]
                if (b & 1) == 0:
                    buf3[b] = buf1[b] + file_content[i + 2]
                else:
                    buf3[b] = buf1[b] - file_content[i + 2]
                next_index = i + 3
        elif file_content[i] == 4:
            next_index = length
            if i + 1 < length:
                b = file_content[i + 1]
                res[b] = buf3[b] ^ buf2[b & 3]
                next_index = i + 2
        elif file_content[i] == 5:
            return bytes(res)
        else:
            assert (False)
        i = next_index


def gen_key_2(key):
    res = [0] * 256
    for i in range(256):
        res[i] = i
    j = 0
    for i in range(256):
        j = (res[i] + j + key[i % len(key)]) % 256
        res[i], res[j] = res[j], res[i]
    return bytes(res)


def decrypt(text, key):
    j = 0
    k = 0
    out = [0] * len(text)
    key = list(key)
    for i in range(len(text)):
        j = (j + 1) % 256
        k = (key[j] + k) % 256
        key[j], key[k] = key[k], key[j]
        out[i] = text[i] ^ key[(key[j] + key[k]) % 256]
    return bytes(out)


with open("anonymous", "rb") as f:
    file_content = f.read()
key = gen_key(file_content)
print(key)
key = gen_key_2(key)
with open("file1_enc", "rb") as f:
    enc_file = f.read()
dec = decrypt(enc_file, key)
with open("dec_file", "wb") as f:
    f.write(dec)
