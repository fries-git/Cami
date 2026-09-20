from tinydb import TinyDB, Query
import os
import secrets
import time
import logger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   

def update(param, condition):
    db = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "users.json"))
    db.update(param, condition)
    db.close()

def login(result, username):
    tokendb = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "tokens.json"))
    Token = Query()

    userid = result[0]["userid"]
    tokendb.remove(Token.userid == userid)

    token = secrets.token_hex(32)
    unix_time = int(time.time())

    tokendb.insert({"timestamp": unix_time, "token": token, "userid": userid})
    tokendb.close()
    logger.info(f"{username} has just logged in!")
    return {"token": token}

def socialsearch(query, type):
    db = TinyDB(os.path.join(BASE_DIR, "dbs", "social", "posts.json"))
    post = Query()
    data = db.search(post[type].test(lambda x: query.lower() in x.lower()))
    db.close()
    return data
    
def search(param):
    db = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "users.json"))
    data = db.search(param)
    db.close()
    return data

def register(uid, registername, registerpassword, usernum):
    tokendb = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "tokens.json"))
    token = secrets.token_hex(32)
    unix_time = int(time.time())
    db = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "users.json"))
    usernum = len(db) + 1
    tokendb.insert({"timestamp": unix_time, "token": token, "userid": uid})
    logger.register(f"{registername} has registered an account! They are user number: {usernum}.")
    db.insert({'username': registername, 'displayname': registername, 'password': registerpassword, 'usernum': usernum, 'bio': f'Hello! I am {registername}, and I have not yet setup my bio!', 'avatardeco': None, 'fries': 0, 'userid': uid})
    db.close()
    tokendb.close()
    return makejsonsuccess(token), 200   

def makejsonerror(input):
    return {"cmd": "error", "message": input}

def makejsonsuccess(input):
    return {"cmd": "success", "message": input}

def dispnamefromrealname(username):
    User = Query()
    db = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "users.json"))
    result = db.search(User.username == username)
    db.close()
    if result:
        return result[0]["displayname"]

    return None

def getlength(filename):
    path = os.path.join(BASE_DIR, "channels", filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            line_count = sum(1 for line in file)
        return (line_count)
    else:
        return (None)

def save_to_file(data, filename):
    path = os.path.join(BASE_DIR, "channels", filename)

    with open(path, "a", encoding="utf-8") as file:
        file.write(str(data) + "\n")

def edit_user_param(token, field, value):
    userid = validate(token)
    db = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "users.json"))
    
    if not userid:
        db.close()
        return False, "Invalid token"

    User = Query()
    result = db.search(User.userid == userid)

    if not result:
        db.close()
        return False, "User not found"

    db.update({field: value}, User.userid == userid)
    db.close()
    return True, "Updated successfully"

def usernametoid(username):
    User = Query()
    db = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "users.json"))
    result = db.search(User.username == username)

    if result:
        db.close()
        return result[0]["userid"]
    db.close()
    return None

def validate(token):
    Token = Query()
    tokendb = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "tokens.json"))
    result = tokendb.search(Token.token == token)

    if result:
        tokendb.close()
        return result[0]["userid"]
    tokendb.close()
    return False

def useridtoname(uid):
    db = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "users.json"))
    User = Query()
    result = db.search(User.userid == uid)

    if result:
        db.close()
        return result[0]["username"]
    db.close()
    return False

def tokentoname(token):
    Token = Query()
    tokendb = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "tokens.json"))
    result = tokendb.search(Token.token == token)

    if result:
        uid = result[0]["userid"]
        tokendb.close()
        return useridtoname(uid)
    tokendb.close()
    return False