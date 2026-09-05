from tinydb import TinyDB, Query
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   

def update(param):
    db = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "users.json"))
    db.update(param)

def search(param):
    db = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "users.json"))
    db.search(param)

def register(uid, registername, registerpassword, usernum, db):
    db = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "users.json"))
    db.insert({'username': registername, 'displayname': registername, 'password': registerpassword, 'usernum': usernum, 'bio': f'Hello! I am {registername}, and I have not yet setup my bio!', 'avatardeco': None, 'fries': 0, 'userid': uid})

def makejsonerror(input):
    return {"cmd": "error", "message": input}

def makejsonsuccess(input):
    return {"cmd": "success", "message": input}

def dispnamefromrealname(username):
    User = Query()
    db = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "users.json"))
    result = db.search(User.username == username)

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
        return False, "Invalid token"

    User = Query()
    result = db.search(User.userid == userid)

    if not result:
        return False, "User not found"

    db.update({field: value}, User.userid == userid)

    return True, "Updated successfully"

def usernametoid(username):
    User = Query()
    db = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "users.json"))
    result = db.search(User.username == username)

    if result:
        return result[0]["userid"]

    return None

def validate(token):
    Token = Query()
    tokendb = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "tokens.json"))
    result = tokendb.search(Token.token == token)

    if result:
        return result[0]["userid"]

    return False

def useridtoname(uid):
    db = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "users.json"))
    User = Query()
    result = db.search(User.userid == uid)

    if result:
        return result[0]["username"]

    return False

def tokentoname(token):
    Token = Query()
    tokendb = TinyDB(os.path.join(BASE_DIR, "dbs", "userdata", "tokens.json"))
    result = tokendb.search(Token.token == token)

    if result:
        uid = result[0]["userid"]
        return useridtoname(uid)

    return False