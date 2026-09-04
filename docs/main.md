# CAMI API Documentation

-# Just so we're clear, these are AI-Generated right now, give me a day.

## Register
POST /register `{"username":"<str>","password":"<str>"}`\
On Success: Returns authentication token in body with code `200`.\
On Failure: Returns code `403`. (Username/password must be between 4 and 32 characters.)\
On Failure: Returns code `409`. (Username is already in use.)

## Login
POST /login `{"username":"<str>","password":"<str>"}`\
On Success: Returns authentication token in body with code `200`.\
On Failure: Returns code `404`. (Account with username and password does not exist.)

## Logout
POST /logout `{"token":"<str>"}`\
On Success: Returns `"Logged out"` with code `200`.\
On Failure: Returns code `400`. (Token was not provided.)

## Get User
GET /user/<name>\
`<name>` can be either a username or user ID.\
On Success: Returns user information in body with code `200`.\
On Failure: Returns code `404`. (User does not exist.)

## Get Users
GET /users\
On Success: Returns an array containing all usernames with code `200`.

## Update Bio
POST /updatebio `{"token":"<str>","newbio":"<str>"}`\
On Success: Returns the new bio in body with code `200`.\
On Failure: Returns code `401`. (Invalid token.)\
On Failure: Returns code `422`. (Bio is longer than 200 characters.)

## Change Username
POST /changename?token=<str> `{"username":"<str>"}`\
On Success: Returns confirmation message in body with code `200`.\
On Failure: Returns code `401`. (Invalid token.)\
On Failure: Returns code `403`. (Username is shorter than 4 characters.)\
On Failure: Returns code `409`. (Username is already taken.)

## Change Display Name
POST /changedisplay `{"token":"<str>","displayname":"<str>"}`\
On Success: Returns the new display name in body with code `200`.\
On Failure: Returns code `401`. (Invalid token.)\
On Failure: Returns code `403`. (Display name is shorter than 4 characters.)\
On Failure: Returns code `404`. (User does not exist.)

## Change Password
POST /changepass?token=<str> `{"oldpass":"<str>","newpass":"<str>"}`\
On Success: Returns `"Updated password."` with code `200`.\
On Failure: Returns code `401`. (Invalid token.)\
On Failure: Returns code `403`. (Old password is incorrect.)\
On Failure: Returns code `403`. (New password is shorter than 4 characters.)

## Create Social Post
POST /social `{"token":"<str>","message":"<str>"}`\
On Success: Returns the created post in body with code `200`.\
On Failure: Returns code `401`. (Invalid token.)\
On Failure: Returns code `400`. (Message is shorter than 10 characters or longer than 200 characters.)

## Get Social Posts
GET /social?count=<int>&offset=<int>\
`count` specifies the number of posts to return.\
`offset` specifies the number of newest posts to skip and defaults to `0`.\
On Success: Returns an array of posts in body with code `200`.\
On Failure: Returns code `204`. (No posts were found.)\
On Failure: Returns code `400`. (No count query was provided.)

## Set Profile Picture
POST /setpfp\
Content-Type: `multipart/form-data`\
Form Data: `token=<str>` and `image=<file>`\
On Success: Returns `"Uploaded"` with code `201`.\
On Failure: Returns code `400`. (Token is missing.)\
On Failure: Returns code `400`. (No image was uploaded.)\
On Failure: Returns code `401`. (Invalid token.)\
The uploaded image is cropped to a square and resized to `128x128` before being saved.

## Get Profile Picture
GET /userpfp/<username>\
`<username>` can be either a username or user ID.\
On Success: Returns the user's profile picture as a PNG with code `200`.\
If the user has no profile picture, the default profile picture is returned.\
On Failure: Returns code `404`. (User does not exist.)

## Get Avatar Decoration
GET /pfpdeco/<filename>\
On Success: Returns the avatar decoration as a PNG with code `200`.\
On Failure: Returns code `404`. (Image does not exist.)

## Set Avatar Decoration
POST /pfpdeco/<filename>\
Form Data: `token=<str>`\
On Success: Returns the decoration filename in body.\
On Failure: Returns an error for an invalid token.

## Home
GET /\
On Success: Returns the CAMI web interface from `main.html` with code `200`.

## Authentication

Authenticated endpoints require a valid authentication token.

Tokens are returned by `/register` and `/login`.

Example:

`{"token":"abcdef123456..."}`

## User Object

A user object contains:

`username` - The user's unique username.\
`displayname` - The user's display name.\
`avatardeco` - The user's avatar decoration.\
`userid` - The user's unique UUID.\
`bio` - The user's biography.\
`usernum` - The user's account number.\
`fries` - The user's fries count.

## Social Post Object

A social post contains:

`message` - The contents of the post.\
`timestamp` - Unix timestamp of when the post was created.\
`userid` - The ID of the user who created the post.\
`postid` - The unique ID of the post.

## HTTP Status Codes

`200` - Request successful.\
`201` - Resource successfully created/uploaded.\
`204` - No content found.\
`400` - Bad request.\
`401` - Invalid authentication token.\
`403` - Request was rejected because of an input restriction.\
`404` - Requested resource/account was not found.\
`409` - Request conflicts with an existing resource.\
`422` - Request was valid but the supplied data was unacceptable.