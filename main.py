from flask import Flask, request
from flask_cors import CORS
from tinydb import TinyDB, Query
import uuid as u
import secrets
from waitress import serve
import time
import random
from helperfuncs import validate

import hashdef as h

# All in order of when made

db = TinyDB('users.json')

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
    tokendb = TinyDB("tokens.json")
    if len(result) == 0:
        if len(registername) >= 4 and len(registerpassword) >= 4:
            token = secrets.token_hex(32)
            unix_time = int(time.time())
            tokendb.insert({"timestamp": unix_time, "token": token, "userid": uid})
            db.insert({'username': registername, 'password': registerpassword, 'usernum': len(db) + 1, 'bio': 'yo yo yo what it do homie', 'fries': 0, 'userid': uid})
            return token, 201
        else:
            return "Password/Username too short (4 char minimum)", 403
    else:
        return "Username already in use.", 409

@app.post("/login")
def login():
    User = Query()
    Token = Query()
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    result = db.search(User.username == username)

    tokendb = TinyDB("tokens.json")

    if result and result[0]["password"] == h.hash(password):
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
    if len(newbio) <= 200:
        User = Query()
        db.update({"bio": newbio}, User.userid == userid)
        return newbio, 200
    else:
        return "Bio too long > (200 chars)", 422

@app.get("/user")
def user():
    User = Query()
    userget = request.args.get("user")
    result = db.search(User.username == userget) or db.search(User.userid == userget)
    if result:
        userobj = {"username":result[0]["username"], "userid":result[0]["userid"], "bio": result[0]["bio"], "usernum": result[0]["usernum"], "fries": result[0]["fries"]}
        return userobj, 200
    else:
        return "User not found", 404

@app.post("/changepass")
def changepass():
    data = request.get_json()
    User = Query()

    oldpass = h.hash(data.get("oldpass"))
    newpass = h.hash(data.get("newpass"))
    token = request.args.get("token")

    validation = validate(token)

    if validation:
        result = db.search(User.password == oldpass)

        if result:
            if len(data.get("newpass")) >= 4:
                db.update({"password": newpass}, User.password == oldpass)
                return "", 200
            else:
                return "Password too short (4 char minimum)", 403
        else:
            return "Old password incorrect", 403
    else:
        return "Invalid token", 401

@app.get("/")
def home():
    return """Hey! Read <a href="https://github.com/fries-git/Cami/tree/main/docs">the documentation</a> for usage!""", 200

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5613)
