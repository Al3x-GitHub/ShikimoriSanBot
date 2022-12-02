import os
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
   return 'Hello, World!'

os.system("git clone https://Al3x-GitHub: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@github.com/Al3x-GitHub/ShikimoriSanBot okk && cd okk && pip3 install -U -r requirements.txt && nohup python3 -m Shikimori &")
