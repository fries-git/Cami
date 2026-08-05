from flask import Flask, request, jsonify
import logging
import hash as h
from tinydb import TinyDB, Query
import uuid as u

db = TinyDB('users.json')
app = Flask(__name__)

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)  # Only show errors

@app.post("/register")
def register():
    data = request.get_json()
    User = Query()
    registername = data.get("username")
    registerpassword = h.hash(data.get("password"))
    result = db.search(User.username == registername)
    uid = str(u.uuid4())
    if len(result) == 0:
        db.insert({'username': data.get("username"), 'password': registerpassword, 'usernum': len(db) + 1, 'bio': 'yo yo yo what it do homie', 'fries': 0, 'userid': uid})
        return uid, 201
    else:
        return "", 409

@app.post("/login")
def login():
    User = Query()
    data = request.get_json()

    loginname = data.get("username")
    loginpassword = h.hash(data.get("password"))

    result = db.search((User.username == loginname) & (User.password == loginpassword))

    if result:
        userid = result[0]["userid"]
        return userid, 200
    else:
        return "", 404

@app.post("/updatebio")
def updatebio():
    User = Query()
    data = request.get_json()
    uid = data.get("uid")
    newbio = data.get("newbio")
    result = db.search((User.userid == uid))
    print(result)

    if result:
        db.update(
            {"bio": newbio},
            User.userid == uid
        )
        return newbio, 200
    else:
        return "", 404

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

    
app.run()