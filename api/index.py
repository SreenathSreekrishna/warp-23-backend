from flask import Flask,jsonify,request
from flask_cors import cross_origin
from hashlib import sha512
import sqlite3

db = sqlite3.connect('api/db.sqlite3')
cur = db.cursor()

app = Flask(__name__)
SECRET_PHRASE = "b48e0f65127134eff3b3771b38b07a5806ae41c8a0a073f96f61f1368456b0136c914b4393f3e0c86e77214b5c028aef072052c47cbad6b5fcd96be4b10e0cbc"

@app.route('/')
@cross_origin()
def index():
    return jsonify({"ip":request.remote_addr})


@app.route('/verify', methods=['POST'])
@cross_origin()
def verify():
    cs = request.form.get('callsign')
    p = request.form.get('phrase')
    p = sha512(p.encode()).hexdigest()
    if p != SECRET_PHRASE:
        return jsonify({"auth":False})
    print('secret authed')
    r = cur.execute('SELECT * FROM users WHERE callSign=?', (cs, )).fetchall()
    if not r:
        return jsonify({"auth":False})
    return jsonify({"auth":True, "info":r[0]})
