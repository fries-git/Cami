import hashlib

def hash(password):
    return(hashlib.sha512(password.encode()).hexdigest())

# This doesn't need to be a seperate file anymore it just used to use a different type that was bulky and bad so I made a seperate thing. Not gonna bother changing it.
