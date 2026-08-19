# WebSocket Server

## Send Message
WebSocket `{"type":"send","channel":"<str>","password":"<str>","msg":"<str>","token":"<str>"}`\
On Success: Saves the message and broadcasts `{"type":"newmsg","userid":"<str>","username":"<str>","channel":"<str>","message":"<str>","msgid":"<str>","time":"<float>"}` to all users in the channel.\
On Failure: Sends `Incorrect password` if the channel password is incorrect. It can also fail if the token is invalid or the message is over 500 characters.\
  
## Join Channel
WebSocket `{"type":"joinchannel","channel":"<str>","password":"<str>","token":"<str>"}`\
On Success: Adds the user to the specified channel and sends `{"type":"joinedchannel","channel":"<str>"}`.\
On Failure: Sends `Incorrect password` if the channel password is incorrect. Sends `Channel does not exist` if the channel does not exist.\
  
## Get History
WebSocket `{"type":"gethist","channel":"<str>","count":"<int>","token":"<str>"}`\
On Success: Returns the last `<count>` messages stored in the channel's history file.\
  
## Get History Length
WebSocket `{"type":"gethistlen","channel":"<str>","token":"<str>"}`\
On Success: Returns the number of messages currently stored in the channel.\
  
## Delete Message
WebSocket `{"type":"deletemessage","channel":"<str>","msgid":"<str>","token":"<str>"}`\
On Success: Deletes the specified message and broadcasts `{"type":"delmsg","messageid":"<str>"}` to all users in the channel.\
On Failure: The message is not deleted if it does not belong to the user making the request.\
  
## Get Public Channels
WebSocket `{"type":"getpublicchannels","token":"<str>"}`\
On Success: Returns a JSON array containing all public channels.\
  
## Create Channel
WebSocket `{"type":"createchannel","channel":"<str>","password":"<str>","token":"<str>"}`\
On Success: Creates the channel, adds the user to it, and sends `{"type":"channelcreated","channel":"<str>"}`.\
On Failure: Sends `Channel already exists` if the channel already exists, or `Invalid channel name` if the channel name is empty or longer than 32 characters.\
  
## Automatic Channel Join
On Connection: The user is automatically added to every public channel.\
  
## Disconnect
On Disconnect: The user is removed from every channel they are currently in.\
If a non-public channel becomes empty, the channel, its password, and its history file are deleted.\
  
## Authentication
On Request: The `token` is validated before processing the request.\
On Failure: Sends `Invalid token. (Token resets whenever you login.)`\
  
## Missing Message Type
WebSocket `{"token":"<str>"}`\
On Failure: Sends `Missing msgtype which is like critical information`.