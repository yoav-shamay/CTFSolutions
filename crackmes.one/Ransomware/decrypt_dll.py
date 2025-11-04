from hashlib import sha256

password = sha256("hackingisnotacrime".encode()).digest()
with open("dll_enc", "rb") as f:
    encrypted_data = f.read()
# type is ecb, last 64 bytes are from EVP_ENCRYPTFINAL_EX
from Crypto.Cipher import AES
cipher = AES.new(password, AES.MODE_ECB)
decrypted_data = cipher.decrypt(encrypted_data[:-64])
with open("libgen.dll", "wb") as f:
    f.write(decrypted_data)
