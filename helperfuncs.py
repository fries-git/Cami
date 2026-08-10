from tinydb import TinyDB, Query
def validate(token):
    Token = Query()
    tokendb = TinyDB("tokens.json")
    result = tokendb.search(Token.token == token)

    if result:
        return result[0]["userid"]

    return None

def useridtoname(uid):
    db = TinyDB('users.json')
    User = Query()
    result = db.search(User.userid == uid)
    return result[0]["username"]

def tokentoname(token):
    Token = Query()
    tokendb = TinyDB("tokens.json")
    result = tokendb.search(Token.token == token)

    if result:
        uid = result[0]["userid"]
        return useridtoname(uid)

    return None