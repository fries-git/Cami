import hashlib

def hash(password):
    return(hashlib.sha256(password.encode()).hexdigest())