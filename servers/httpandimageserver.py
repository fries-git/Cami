from flask import Flask, request, send_file, render_template
from flask_cors import CORS
from tinydb import TinyDB, Query
import uuid as u
import secrets
from waitress import serve
import time
from helperfuncs import *
import os
from PIL import Image, ImageSequence
import json
import logger
import math
from mp32ogg import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   
clients = []
import hashdef as h

app = Flask(__name__)
CORS(app)



@app.post("/register")
def registerpath():
    data = request.get_json()
    User = Query()
    registername = data.get("username")
    password = data.get("password")
    registerpassword = h.hash(password)
    result = search(User.username == registername)
    uid = str(u.uuid4())
    if len(result) == 0:
        if 4 <= len(registername) <= 32 and 4 <= len(password) <= 32:
            return(register(uid, registername, registerpassword))
        else:
            return makejsonerror("Password/Username too short or long (4 char minimum, 32 char maximum.)"), 403
    else:
        return makejsonerror("Username already in use."), 409

@app.post("/login")
def loginpath():
    User = Query()
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    result = search(User.username == username)

    if result and result[0]["password"] == h.hash(password):
        return makejsonsuccess(login(result, username)) , 200

    return makejsonerror("Username/Password does not exist"), 404

@app.post("/updatebio")
def updatebiopath():
    data = request.get_json()

    token = data.get("token")
    userid = validate(token)

    if not userid:
        return makejsonerror("Invalid token"), 401

    newbio = data.get("newbio")
    if len(newbio) <= 200:
        edit_user_param(validate(token), "bio", newbio)
        logger.success(f"{tokentoname(token)} has just updated their bio!")
        return makejsonsuccess(newbio), 200
    else:
        return makejsonerror("Bio too long > (200 chars)"), 422

@app.get("/user/<name>")
def userpath(name):
    User = Query()
    path = os.path.join(BASE_DIR, "dbs", "userdata", "users.json")
    result = search(User.username == name) or search(User.userid == name)
    if result:
        userobj = {"username":result[0]["username"], "displayname":result[0]["displayname"], "avatardeco":result[0]["avatardeco"], "userid":result[0]["userid"], "bio": result[0]["bio"], "usernum": result[0]["usernum"], "fries": result[0]["fries"]}
        logger.info(f"{name} has just been queried.")
        return makejsonsuccess(userobj), 200
    else:
        return makejsonerror("User not found"), 404

@app.post("/changename")
def changenamepath():
    data = request.get_json()
    User = Query()

    username = data.get("username")
    token = request.args.get("token")

    validation = validate(token)

    if not validation:
        return makejsonerror("Invalid token"), 401

    if not username or len(username) < 4:
        return makejsonerror("Username too short (4 char minimum)"), 403

    if search(User.username == username):
        return makejsonerror("Username already taken"), 409

    if not search(User.userid == validation):
        return makejsonerror("User not found"), 404

    edit_user_param(validate(token), "username", username)
    return makejsonsuccess(f"Updated username. Hello {username}!"), 200

@app.post("/changedisplay")
def changedisplaypath():
    data = request.get_json()
    User = Query()

    name = data.get("displayname")
    token = data.get("token")

    validation = validate(token)

    if not validation:
        return makejsonerror("Invalid token"), 401

    if not name or len(name) < 4:
        return makejsonerror("New displayname too short (4 char minimum)"), 403

    if not search(User.userid == validation):
        return makejsonerror("User not found"), 404

    edit_user_param(validate(token), "displayname", name)
    return makejsonsuccess(name), 200, 200

@app.post("/changepass")
def changepasspath():
    data = request.get_json()
    User = Query()

    oldpass = h.hash(data.get("oldpass"))
    newpass = h.hash(data.get("newpass"))
    token = request.args.get("token")
    
    validation = validate(token)

    if validation:
        result = search(User.password == oldpass)

        if result:
            if len(data.get("newpass")) >= 4:
                update({"password": newpass}, User.password == oldpass)
                return makejsonsuccess("Updated password."), 200
            else:
                return makejsonerror("Password too short (4 char minimum)"), 403
        else:
            return makejsonerror("Old password incorrect"), 403
    else:
        return makejsonerror("Invalid token"), 401

@app.get("/")
def homepath():
    db = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "users.json"))
    usercount = len(db)
    db.close()
    return render_template("main.html", usercount=usercount), 200    

@app.post("/social")
def socialpostpath():
    data = request.get_json()

    body = data.get("message")
    token = data.get("token")
    uid = validate(token)
    unix_time = int(time.time())
    postid = str(u.uuid4())

    if not uid:
        return makejsonerror("Invalid token"), 401

    postdb = TinyDB(os.path.join(BASE_DIR, "dbs", "social", "posts.json"))
    if len(body) >= 10 and len(body) <= 200:
        data = {"message": body, "timestamp": unix_time, "userid": uid, "username": tokentoname(token), "postid": postid}
        postdb.insert(data)
        logger.success(f"{tokentoname(token)} has just made a new social post!")
        postdb.close()
        return makejsonsuccess(data), 200
    return makejsonerror("Body length is either too short or too long (10-200 characters)"), 400

@app.get("/social")
def socialretrievepath():
    count = int(request.args.get("count"))
    if request.args.get("offset"):
        offset = int(request.args.get("offset"))
    else:
        offset = 0

    if count:
        postdb = TinyDB(os.path.join(BASE_DIR, "dbs", "social", "posts.json"))
        results = postdb.all()[::-1][offset:offset + count]
        if results:
            logger.info(f"Someone has just queried {count} posts with {offset} offset!")
            postdb.close()
            return makejsonsuccess(results), 200
        else:
            postdb.close()
            return makejsonerror("No posts found"), 204
    postdb.close()
    return "No count query", 400

@app.get("/search/message/<query>")
def searchmsgpath(query):
    return socialsearch(query, "message"),200

@app.get("/search/userid/<query>")
def searchuseridpath(query):
    return socialsearch(query, "userid"),200

@app.get("/search/username/<query>")
def searchusernamepath(query):
    query = usernametoid(query)
    return socialsearch(query, "userid"),200

@app.get("/search/postid/<query>")
def searchpostidpath(query):
    return socialsearch(query, "postid"),200

@app.post("/logout")
def logoutpath():
    Token = Query()
    data = request.get_json()
    token = data.get("token")
    if token:
        tokendb = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "tokens.json"))
        tokendb.remove(Token.token == token)
        logger.info(f"Goodbye {tokentoname(token)}! Come back soon!")
        tokendb.close()
        return makejsonsuccess("Logged out"), 200
    tokendb.close()
    return makejsonerror("Token not found"), 400

@app.post("/transferfries")
def transferfriespath():
    try:
        data = request.get_json()

        token = data.get("token")
        name = data.get("recipientname")
        recipientid = usernametoid(name)
        print(recipientid)
        count = data.get("count")

        userid = validate(token)

        searchresp1 = search(Query().userid == userid)[0]
        userfries = searchresp1["fries"]

        searchresp2 = search(Query().userid == recipientid)[0]
        recipfries = searchresp2["fries"]
        try:
            if userfries >= count:
                edit_user_param(recipientid, "fries", recipfries + count)
                edit_user_param(userid, "fries", userfries - count)
        except Exception as e:
            edit_user_param(recipientid, "fries", recipfries)
            edit_user_param(userid, "fries", userfries)
            logger.error(e)
            return makejsonerror("Fries transfer error. Unknown error."), 500
        
    except Exception as e:
        logger.error(e)
        return makejsonerror("Internal server error"), 500

    return makejsonsuccess(f"{count} fries transfered to {name}.")

@app.get("/users")
def userspath():
    db = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "users.json"))
    users = db.all()
    usernames = [user["username"] for user in users]
    db.close()
    return makejsonsuccess(usernames), 200

@app.post("/setpfp")
def setpfppath():
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
    img = img.resize((128, 128), Image.Resampling.LANCZOS)
    
    if token:
        if not image:
            return makejsonerror("No image uploaded"), 400

        uid = validate(token)

        if not uid:
            return makejsonerror("Invalid token"), 401

        os.makedirs(os.path.join(BASE_DIR, "uploads", "pfps"), exist_ok=True)
        path = os.path.join(BASE_DIR, "uploads", "pfps", f"{uid}.png")
        img.save(path)

        return makejsonsuccess("Uploaded"), 201
    else:
        return makejsonerror("Missing token"), 400
    
@app.get("/userpfp/<username>")
def getpfppath(username):
    User = Query()

    result = search((User.username == username) | (User.userid == username))

    if result:
        userid = result[0]["userid"]

        path = os.path.join(BASE_DIR, "uploads", "pfps", f"{userid}.png")

        if os.path.exists(path):
            return send_file(path, mimetype="image/png")

        emptypfp = os.path.join(BASE_DIR, "templates", "emptypfp.png")
        return send_file(emptypfp, mimetype="image/png")

    return makejsonerror("User doesn't exist."), 404

@app.get("/pfpdeco/<filename>")
def getimagepath(filename):
    path = os.path.join(BASE_DIR, "uploads", "avatardecos", f"{filename}.png")

    if os.path.exists(path):
        return send_file(path, mimetype="image/png")

    return makejsonerror("Image doesn't exist"), 404

@app.post("/pfpdeco/<filename>")
def setimagepath(filename):
    data = request.get_json()
    token = data.get("token")
    userid = validate(token)
    path = os.path.join(BASE_DIR, "uploads", "avatardecos", f"{filename}.png")
    if os.path.exists(path):
        userfries = searchparam(userid, "fries", False, 0)
        decorcost = 5

        try:
            if userfries >= decorcost:
                edit_user_param(userid, "fries", userfries - decorcost)
                if validate(token):
                    edit_user_param(userid, "avatardeco", filename)
                    return makejsonsuccess(str(filename))
                else:
                    return makejsonerror("Invalid Token"), 200
            else:
                return makejsonerror("Haha broke bitch"), 404
        except Exception as e:
            edit_user_param(userid, "fries", userfries)
            logger.error(e)
            return makejsonerror("Internal server error"), 500
    else:
        return makejsonerror("Decor does not exist"), 404

@app.post("/daily")
def dailypath():
    cooldown = 86400
    try:
        data = request.get_json()
        token = data.get("token")
        userid = validate(token)
        timestamp = searchparam(userid, "dailytimestamp", True, 0)
        if time.time() - timestamp >= cooldown:
            try:
                fries = searchparam(userid, "fries", False, 0   )
                edit_user_param(userid, "dailytimestamp", time.time())
                edit_user_param(userid, "fries", fries + 10)
                return makejsonsuccess(f"Daily claimed! {fries} -> {fries + 10}"), 200
            except Exception as e:
                return makejsonerror(str(e)), 400
        else:
            return makejsonerror(f"You must wait {math.floor(cooldown - (time.time() - timestamp))} seconds.")
    except Exception as e:
        return makejsonerror(str(e))

@app.post("/uploadmusic")
def uploadsong():
    token = request.form.get("token")
    song = request.files.get("song")
    filename = request.form.get("filename")
    if validate(token):
        if not song:
            return makejsonerror("No song uploaded"), 400

        try:
            userid = validate(token)
            mp3path = os.path.join(BASE_DIR, "uploads", "musicstorage", filename)      
            oggpath = os.path.splitext(mp3path)[0] + ".ogg"

        except Exception as e:
            logger.error(e)
            return makejsonerror("Invalid or incomplete song"), 400
        
        song.save(mp3path)
        mp3toogg(mp3path, oggpath, "3")
        logger.success(f"{useridtoname(userid)} just uploaded: {filename} at: {time.time()}")
        os.remove(mp3path)      
        return makejsonsuccess(filename), 200

@app.post("/uploadimage")
def uploadimage():
    token = request.form.get("token")
    image = request.files.get("image")
    filename = request.form.get("filename")

    if validate(token):
        if not image:
            return makejsonerror("No image uploaded"), 400

        try:
            img = Image.open(image)
            img.load()
        except (Exception) as e:
            return makejsonerror("Invalid or incomplete image"), 400
        
        img_format = (str(img.format)).lower()
        if img_format == "gif":
            pass
        else:
            img = img.convert("RGBA")

        width, height = img.size
        
        targetmax = 300
        mult = max(width, height) / targetmax

        new_size = (
            max(1, int(width / mult)),
            max(1, int(height / mult))
        )

        uid = validate(token)

        if not uid:
            return makejsonerror("Invalid token"), 401
        
        if img_format == "gif":
            frames = []
            durations = []

            for frame in ImageSequence.Iterator(img):
                duration = frame.info.get("duration", img.info.get("duration", 100))

                frame = frame.convert("RGBA")
                frame = frame.resize(new_size, Image.Resampling.LANCZOS)
                frame = frame.convert("P", palette=Image.Palette.ADAPTIVE)

                frames.append(frame)
                durations.append(duration)

            path = os.path.join(BASE_DIR,"uploads","imagestorage",f"{filename}.gif")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if os.path.exists(path):
                return makejsonerror("File already exists"), 409
            frames[0].save(path,format="GIF",save_all=True,append_images=frames[1:],duration=durations,loop=img.info.get("loop", 0),disposal=2,optimize=True)
            return makejsonsuccess(f"https://images.barfpile.dev/gif/{filename}.png"), 201
        else:
            img = img.resize((int(width / mult), int(height / mult)), Image.Resampling.LANCZOS)
            try:
                os.makedirs(os.path.join(BASE_DIR, "uploads", "imagestorage"), exist_ok=True)
            except FileExistsError:
                return makejsonerror("File already exists"), 409
            path = os.path.join(BASE_DIR, "uploads", "imagestorage", f"{filename}.png")
            if os.path.exists(path):
                return makejsonerror("File already exists"), 409
            img.save(path)
            return makejsonsuccess(f"https://images.barfpile.dev/image/{filename}.png"), 201
    else:
        return "Missing/Invalid token", 400
    return "Unhandled Error", 400

@app.get("/song/<filename>")
def song(filename):
    filepath = os.path.join(BASE_DIR, "uploads", "musicstorage", f"{filename}.ogg")

    if os.path.exists(filepath):
        return send_file(filepath)

    return makejsonerror("Song doesn't exist"), 404

@app.get("/image/<filename>")
def image(filename):

    png_path = os.path.join(
        BASE_DIR, "uploads", "imagestorage", f"{filename}.png"
    )
    gif_path = os.path.join(
        BASE_DIR, "uploads", "imagestorage", f"{filename}.gif"
    )

    if os.path.exists(png_path):
        logger.info(f"Someone has queried: {filename}.png")
        return send_file(png_path, mimetype="image/png")
    if os.path.exists(gif_path):
        logger.info(f"Someone has queried: {filename}.gif")
        return send_file(gif_path, mimetype="gif/png")

    return makejsonerror("Image doesn't exist"), 404

@app.get("/gif/<filename>.gif")
def get_gif(filename):

    path = os.path.join(BASE_DIR,"uploads","imagestorage",f"{filename}.gif")

    if not os.path.isfile(path):
        return makejsonerror("Image doesn't exist"), 404

    return send_file(path, mimetype="image/gif")

portuse = 5613
logger.info(f"Running on port {portuse}")

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=portuse, threads = 8)