# WebSocket Server
## Send Message
WebSocket `{"type":"send","channel":"<str>","password":"<str>","msg":"<str>","token":"<str>"}`
On Success: Broadcasts `{"type":"newmsg","userid":"<str>","message":"<str>"}` to all users in the channel.
On Failure: Sends `Incorrect password` if the channel password is incorrect. However it can also fail if the token is invalid.
  
## Join Channel
WebSocket `{"type":"joinchannel","channel":"<str>","password":"<str>"}`
On Success: Adds the user to the specified channel.
On Failure: Sends `Incorrect password` if the channel password is incorrect. If the channel does not exist, nothing is returned.
  
## Automatic Channel Join
On Connection: The user is automatically added to the `general` channel.
  
## Disconnect
On Disconnect: The user is removed from every channel they are currently in.