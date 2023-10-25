from flask import Flask,jsonify,request
from flask_cors import cross_origin

app = Flask(__name__)

@app.route('/')
@cross_origin()
def index():
    return jsonify({"ip":request.remote_addr})