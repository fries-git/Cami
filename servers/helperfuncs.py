from tinydb import TinyDB, Query
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   

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