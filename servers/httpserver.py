from flask import Flask, request, Response, send_file
from flask_cors import CORS
from tinydb import TinyDB, Query
import uuid as u
import secrets
from waitress import serve
import time
from helperfuncs import validate, tokentoname
import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   
clients = []
import hashdef as h

db = TinyDB(os.path.join(BASE_DIR, "users.json"))

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
    tokendb = TinyDB(os.path.join(BASE_DIR, "tokens.json"))
    if len(result) == 0:
        if len(registername) >= 4 and len(registerpassword) >= 4:
            token = secrets.token_hex(32)
            unix_time = int(time.time())
            usernum = len(db) + 1
            tokendb.insert({"timestamp": unix_time, "token": token, "userid": uid})
            db.insert({'username': registername, 'password': registerpassword, 'usernum': usernum, 'bio': f'Hello! I am {registername}, and I have not yet setup my bio!', 'fries': 0, 'userid': uid})
            print(f"{registername} has registered an account! They are user number: {usernum}.")
            return token, 200
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

    tokendb = TinyDB(os.path.join(BASE_DIR, "tokens.json"))

    if result and result[0]["password"] == h.hash(password):
        userid = result[0]["userid"]
        tokendb.remove(Token.userid == userid)

        token = secrets.token_hex(32)
        unix_time = int(time.time())

        tokendb.insert({"timestamp": unix_time, "token": token, "userid": userid})
        print(f"{username} has just logged in!")
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
        print(f"{tokentoname(token)} has just updated their bio!")
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
        print(f"{userget} has just been queried.")
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
    return """Hey! This is Cami, and authentication program. Please, read <a href="https://github.com/fries-git/Cami/tree/main/docs">the documentation</a> for usage!""", 200

@app.post("/social")
def socialpost():
    data = request.get_json()

    body = data.get("body")
    token = data.get("token")
    uid = validate(token)
    unix_time = int(time.time())
    postid = str(u.uuid4())

    if not uid:
        return "Invalid token", 401

    postdb = TinyDB(os.path.join(BASE_DIR, "posts.json"))
    if len(body) >= 10 and len(body) <= 200:
        postdb.insert({"body": body, "timestamp": unix_time, "userid": uid, "postid": postid})
        print(f"{tokentoname(token)} has just made a new social post!")
        return postid, 200
    return "Body length is either too short or too long (10-200 characters)", 400

@app.get("/social")
def socialretrieve():
    count = int(request.args.get("count"))
    if request.args.get("offset"):
        offset = int(request.args.get("offset"))
    else:
        offset = 0

    if count:
        postdb = TinyDB(os.path.join(BASE_DIR, "posts.json"))
        results = postdb.all()[::-1][offset:offset + count]
        if results:
            print(f"Someone has just queried {count} posts with {offset} offset!")
            return results, 200
        else:
            return "No posts found", 204
    return "No count query", 400

@app.post("/logout")
def logout():
    Token = Query()
    data = request.get_json()
    token = data.get("token")
    if token:
        tokendb = TinyDB(os.path.join(BASE_DIR, "tokens.json"))
        tokendb.remove(Token.token == token)
        print(f"Goodbye {tokentoname(token)}! Come back soon!")
        return "Logged out", 200
    return "Token not found", 400

@app.get("/users")
def users():
    users = db.all()
    usernames = [user["username"] for user in users]

    return usernames, 200

@app.post("/setpfp")
def setpfp():
    token = request.form.get("token")
    image = request.files.get("image")

    img = Image.open(image)
    img = img.convert("RGB")

    width, height = img.size
    size = min(width, height)

    left = (width - size) // 2
    top = (height - size) // 2
    right = left + size
    bottom = top + size

    img = img.crop((left, top, right, bottom))
    img = img.resize((256, 256), Image.Resampling.LANCZOS)
    
    if token:
        if not image:
            return {"error": "No image uploaded"}, 400

        uid = validate(token)

        if not uid:
            return {"error": "Invalid token"}, 401

        os.makedirs(os.path.join(BASE_DIR, "uploads", "pfps"), exist_ok=True)
        path = os.path.join(BASE_DIR, "uploads", "pfps", f"{uid}.png")
        img.save(path)

        return {"message": "Uploaded!", "filename": f"{uid}.png"}, 201
    else:
        return "Missing token", 400
    
@app.get("/userpfp")
def getpfp():
    User = Query()
    userget = request.args.get("user")
    result = db.search(User.username == userget) or db.search(User.userid == userget)
    if result:
        userid = result[0]["userid"]
        path = os.path.join(BASE_DIR, "uploads", "pfps", f"{userid}.png")
        if not os.path.exists(path):
            path = os.path.join(BASE_DIR, "emptypfp.png")

        return send_file(path, mimetype="image/png")

    else:
        return "User not found", 404

portuse = 5613
print(f"Running on port {portuse}")

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=portuse)