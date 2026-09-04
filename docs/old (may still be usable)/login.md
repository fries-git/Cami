# Login
POST /login `{"username":"<str>","password":"<str>"}`\
On Success: Returns User ID in body with code `201`.\
On Failure: Returns code `404`. (Account with username and password does not exist.)
