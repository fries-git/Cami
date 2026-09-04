# Change Password
POST /changepass `{"oldpass":"<str>","newpass":"<str>","token":"<str>"}`\
On Success: Returns code `200`.\
On Failure: Returns code `403` with `Password too short (4 char minimum)` or `Old password incorrect`. However it can also return `401` with `Invalid token`
