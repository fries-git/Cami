from tinydb import TinyDB, Query

def validate(token):
    Token = Query()
    tokendb = TinyDB("tokens.json")
    result = tokendb.search(Token.token == token)

    if result:
        return result[0]["userid"]

    return None
