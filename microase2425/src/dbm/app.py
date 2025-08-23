from flask import Flask, request, make_response, jsonify
import threading, time, os
from pymongo import MongoClient

client = MongoClient("db", 27017, maxPoolSize=50)
db = client["mydatabase"]

app = Flask(__name__, instance_relative_config=True)

@app.route('/getAll')
def getLogs():
    res = []
    all = list(db.collection.find({}))
    for element in all:
        res.append({'timestamp': element["timestamp"], 'op': element["op"], 'args': element["args"], 'res': element["res"]})
    return make_response(jsonify(res), 200)

@app.route('/notify', methods=['POST'])
def addLog():
    payload = request.json
    db.collection.insert_one(payload)
    return make_response(jsonify('ok'),200)

@app.route('/crash')
def crash():
    def close():
        time.sleep(1)
        os._exit(0)
    thread = threading.Thread(target=close)
    thread.start()
    ret = str(request.host) + " crashed"
    return make_response(jsonify(s=ret), 200)

def create_app():
    return app

