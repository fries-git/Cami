# WebSocket Server

## Send Message
WebSocket `{"type":"send","channel":"<str>","password":"<str>","msg":"<str>","token":"<str>"}`\
On Success: Saves the message and broadcasts `{"type":"newmsg","userid":"<str>","username":"<str>","displayname":"<str>","channel":"<str>","message":"<str>","msgid":"<str>","time":"<float>"}` to all users in the channel.\
`msgid` is a randomly generated UUID. `time` is the current Unix timestamp.\
On Failure: Sends `Incorrect password` if the channel password is incorrect. It can also fail if the token is invalid, the user has not joined the channel, or the message is over 500 characters.\
  
## Join Channel
WebSocket `{"type":"joinchannel","channel":"<str>","password":"<str>","token":"<str>"}`\
On Success: Adds the user to the specified channel and broadcasts `{"type":"joinedchannel","userid":"<str>","username":"<str>","channel":"<str>"}` to all users in the channel.\
On Failure: Sends `Incorrect password` if the channel password is incorrect. Sends `Channel does not exist` if the channel does not exist.\
  
## Get History
WebSocket `{"type":"gethist","channel":"<str>","count":"<int>","offset":"<int>","token":"<str>"}`\
On Success: Returns the requested messages stored in the channel's history file. `count` specifies the number of messages and `offset` specifies how many messages to skip from the end.\
`count` defaults to `10` and `offset` defaults to `0` if they are not provided.\
  
## Get History Length
WebSocket `{"type":"gethistlen","channel":"<str>","token":"<str>"}`\
On Success: Returns `{"type":"histlen","count":"<int>"}` containing the number of messages currently stored in the channel.\
  
## Delete Message
WebSocket `{"type":"deletemessage","channel":"<str>","msgid":"<str>","token":"<str>"}`\
On Success: Deletes the specified message from the channel's history file and broadcasts `{"type":"delmsg","messageid":"<str>"}` to all users in the channel.\
On Failure: The message is not deleted if it does not exist or does not belong to the user making the request.\
  
## Get Public Channels
WebSocket `{"type":"getpublicchannels","token":"<str>"}`\
On Success: Returns a JSON array containing all public channels.\
The default public channels are `general`, `coding`, `off-topic`, and `shitpost`.\
  
## Create Channel
WebSocket `{"type":"createchannel","channel":"<str>","password":"<str>","token":"<str>"}`\
On Success: Creates the channel, creates its history file, adds the user to it, and sends `{"type":"channelcreated","channel":"<str>"}`.\
Newly created channels are private and are not added to the public channel list.\
Channel names are converted to lowercase.\
On Failure: Sends `Channel already exists` if the channel already exists, or `Invalid channel name` if the channel name is empty or longer than 32 characters.\
  
## Automatic Channel Join
On Connection: The user is automatically added to every public channel.\
The default public channels are `general`, `coding`, `off-topic`, and `shitpost`.\
  
## Default Channels
The server creates the following channels when it starts: `general`, `coding`, `off-topic`, `shitpost`, and `friespersonal`.\
`friespersonal` is a private/password-protected channel.\
  
## Channel Passwords
Public channels have no password.\
Password-protected channels require the correct password when joining.\
The password must also be supplied when sending messages to a password-protected channel.\
  
## Disconnect
On Disconnect: The user is removed from every channel they are currently in.\
If a non-public channel becomes empty, the channel, its password, and its history file are deleted.\
Public and other built-in channels are not deleted when they become empty.\
  
## Authentication
On Request: The `token` is validated before processing the request.\
On Failure: Sends `Invalid token. (Token resets whenever you login.)`\
  
## Channel History
Each channel has its own history file named `<channel>.json`.\
Messages are stored as JSON objects, one message per line.\
  
## Message Limit
Messages are limited to 500 characters.\
On Failure: Sends `Message too long! (500 Char Limit)` if the message exceeds 500 characters.\
  
## Channel Name Limit
Channel names must be 32 characters or fewer.\
Channel names are converted to lowercase before being processed.\
  
## Invalid JSON
On Failure: Sends `Invalid JSON` if the received WebSocket message cannot be parsed as JSON, then closes the connection.\
  
## Missing Message Type
WebSocket `{"token":"<str>"}`\
On Failure: Sends `Missing msgtype which is like critical information`.\
  
## Channel Does Not Exist
On Failure: Sends `Channel does not exist` when attempting to join a channel that is not present in the server's channel list.\
  
## Channel Already Exists
On Failure: Sends `Channel already exists` when attempting to create a channel that already exists.\
  
## Invalid Channel Name
On Failure: Sends `Invalid channel name` when creating a channel with an empty name or a name longer than 32 characters.\
  
## Invalid Token
On Failure: Sends `Invalid token. (Token resets whenever you login.)` when the supplied token cannot be validated.\
  
## Incorrect Password
On Failure: Sends `Incorrect password` when the password supplied for a channel does not match the stored channel password.