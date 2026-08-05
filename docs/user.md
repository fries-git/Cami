# User
GET /user `{"user":"<str username or userid>"}`\
On Success: Returns user bio, account #, and fries (currency) as json obj with code `200`.\
On Failure: Returns error code `404` if user not found.
