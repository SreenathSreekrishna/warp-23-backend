from flask import Flask,jsonify,request,make_response
from flask_cors import cross_origin,CORS
from hashlib import sha512
import sqlite3

db = sqlite3.connect('api/db.sqlite3')
cur = db.cursor()

app = Flask(__name__)
CORS(
    app,
    allow_headers="*",
    supports_credentials=True,
    expose_headers=[
        "tokens",
        "Set-Cookie",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Credentials",
    ],
)

SECRET_PHRASE = "b48e0f65127134eff3b3771b38b07a5806ae41c8a0a073f96f61f1368456b0136c914b4393f3e0c86e77214b5c028aef072052c47cbad6b5fcd96be4b10e0cbc"

@app.route('/')
def index():
    return jsonify({"ip":request.remote_addr})

def cors_allow(thing):
    response = make_response(thing)
    response.headers["Access-Control-Allow-Origin"] = "http://cosmoshield.neevsahay.com"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@app.route('/verify', methods=['POST'])
def verify():
    cookie = request.cookies.get('id')
    print('my delicious cookie is',cookie)
    if cookie:
        all = cur.execute('SELECT * FROM users').fetchall()
        for row in all:
            hash = sha512((row[1] + SECRET_PHRASE).encode()).hexdigest()
            print(hash, cookie)
            if hash == cookie:
                return cors_allow(jsonify({"auth":True, "info":row, "cookieHash":cookie}))
        return jsonify({"auth":False})
    cs = request.form.get('callsign')
    p = request.form.get('phrase')
    p = sha512(p.encode()).hexdigest()
    if p != SECRET_PHRASE:
        return jsonify({"auth":False})
    r = cur.execute('SELECT * FROM users WHERE callSign=?', (cs, )).fetchall()
    print(r)
    if not r:
        return jsonify({"auth":False})
    return cors_allow(jsonify({"auth":True, "info":r[0], "cookieHash":sha512((r[0][1]+SECRET_PHRASE).encode()).hexdigest()}))
