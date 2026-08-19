from tinydb import TinyDB, Query
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   

def getlength(filename):
    path = os.path.join(BASE_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            line_count = sum(1 for line in file)
        return (line_count)
    else:
        return (None)

def save_to_file(data, filename):
    path = os.path.join(BASE_DIR, filename)

    with open(path, "a", encoding="utf-8") as file:
        file.write(str(data) + "\n")

def usernametoid(username):
    User = Query()
    db = TinyDB(os.path.join(BASE_DIR, "users.json"))
    result = db.search(User.username == username)

    if result:
        return result[0]["userid"]

    return None

def validate(token):
    Token = Query()
    tokendb = TinyDB(os.path.join(BASE_DIR, "tokens.json"))
    result = tokendb.search(Token.token == token)

    if result:
        return result[0]["userid"]

    return False

def useridtoname(uid):
    db = TinyDB(os.path.join(BASE_DIR, "users.json"))
    User = Query()
    result = db.search(User.userid == uid)

    if result:
        return result[0]["username"]

    return False

def tokentoname(token):
    Token = Query()
    tokendb = TinyDB(os.path.join(BASE_DIR, "tokens.json"))
    result = tokendb.search(Token.token == token)

    if result:
        uid = result[0]["userid"]
        return useridtoname(uid)

    return False