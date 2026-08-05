from flask import Flask, request
from flask_cors import CORS
from tinydb import TinyDB, Query
import uuid as u
import secrets
from waitress import serve
import time
import random

import hashdef as h

db = TinyDB('users.json')
tokendb = TinyDB("tokens.json")
app = Flask(__name__)
CORS(app)

@app.post("/register")
def register():
    data = request.get_json()
    User = Query()
    registername = data.get("username")
    password = data.get("password")
    registerpassword = h.hash(password)
    result = db.search(User.username == registername)
    uid = str(u.uuid4())
    
    if len(result) == 0:
        if len(registername) >= 4 and len(registerpassword) >= 4:
            db.insert({'username': registername, 'password': registerpassword, 'usernum': len(db) + 1, 'bio': 'yo yo yo what it do homie', 'fries': 0, 'cigarettes': 0, 'userid': uid})
            return uid, 201
        else:
            return "Password/Username too short (4 char minimum)"
    else:
        return "", 409

@app.post("/login")
def login():
    User = Query()
    Token = Query()
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    result = db.search(User.username == username)

    if result and h.hash(password):
        userid = result[0]["userid"]
        tokendb.remove(Token.userid == userid)

        token = secrets.token_hex(32)
        unix_time = int(time.time())

        tokendb.insert({"timestamp": unix_time, "token": token, "userid": userid})
        return token, 200

    return "Username/Password invalid", 401

@app.post("/updatebio")
def updatebio():
    data = request.get_json()

    token = data.get("token")
    userid = validate(token)

    if not userid:
        return "Invalid token", 401

    newbio = data.get("newbio")

    User = Query()
    db.update(
        {"bio": newbio},
        User.userid == userid
    )

    return newbio, 200

@app.post("/validate")
def validate(token):
    Token = Query()
    result = tokendb.search(Token.token == token)

    if result:
        return result[0]["userid"]

    return None

@app.post("/getuser")
def getuser():
    User = Query()
    data = request.get_json()
    userget = data.get("user")
    result = db.search(User.username == userget)
    if result:
        userobj = {"bio": result[0]["bio"], "usernum": result[0]["usernum"], "fries": result[0]["fries"]}
        return userobj, 200
    else:
        return "", 404

@app.post("/smoke")
def smoke():
    Token = Query()
    data = request.get_json()
    token = data.get("token")
    result = tokendb.search(Token.token == token)
    if result:
        uid = validate(token)
        if uid:
            User = Query()
            result = db.search(User.userid == uid)
            rand = random.randint(1, random.randint(1, 3))
            smokesleft = result[0]["cigarettes"]
            if smokesleft > 0:
                if rand == 1:
                    return "You start coughing like crazy", 200
                elif rand == 2:
                    return "Huh. Aight.", 200
                elif rand == 3:
                    return "Man. Awesome", 200
            else:
                return "No smokes :(", 404
        else:
            return "", 404
    else:
        return "", 404

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)