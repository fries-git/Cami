from flask import Flask, request, jsonify
import logging
import hash as h
from tinydb import TinyDB, Query

db = TinyDB('users.json')
app = Flask(__name__)

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)  # Only show errors

@app.post("/register")
def register():
    data = request.get_json()
    db.insert({'username': data.get("username"), 'password': h.hash(data.get("password"))})
    return "", 204

app.run()