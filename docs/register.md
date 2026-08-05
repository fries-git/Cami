# Register
POST /register {"username":"<str>","password":"<str>"}\
On Success: Returns User ID in body with code `201`.\
On Failure: Returns code `409`. (Account with name already made.)
