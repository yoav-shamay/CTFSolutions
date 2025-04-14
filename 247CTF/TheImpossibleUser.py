text = "impossible_flag_user"
import requests
url = "https://61909e0044644788.247ctf.com/"
def encrypt(text):
    return bytes.fromhex(requests.get(url+"encrypt?user="+text.encode().hex()).text)
start = encrypt(text[:16])[:16]
end = encrypt(text[16:])
res = start + end
print(requests.get(url+"get_flag?user="+res.hex()).text)
