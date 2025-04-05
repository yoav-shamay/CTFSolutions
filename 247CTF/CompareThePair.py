import hashlib
import os
import urllib.parse
def verify(s):
    n = s.find("e")
    if n == -1 or n == 0:
        return False
    return s[:n] == ("0" * n) and s[n + 1:].isdigit()

salt = b"f789bbc328a3d1a3"
while True:
    s = os.urandom(5)
    if verify(hashlib.md5(salt + s).hexdigest()):
        print(urllib.parse.quote_plus(s))
        print(hashlib.md5(salt + s).hexdigest())
        break
