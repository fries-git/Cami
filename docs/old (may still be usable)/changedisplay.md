# Change Display Name
POST /changedisplay `{"displayname":"<str>","token":"<str>"}`\
On Success: Returns `{"cmd": "success", "displayname": <new display name>}` in body with code `201`.\
On Failure: Returns code `404`. (Account with username and password does not exist.)
