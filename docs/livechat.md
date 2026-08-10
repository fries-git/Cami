# Live Chatting System  

The live chatting system is a lightweight chatting system with Cami as a backend for logins and user management. This uses a single websocket connection, and as such, is relatively simple.  
First, connect to the websocket. Next, simply post `{"cmd":"post","token":"<str>","body":"<str>","channel":"<str>"}` and if valid, the message will get broadcast to all users!  
When you recieve a message it will be in the format: `{"uid":"<str>","body":"<str>"}` which you can then run a get request on `https://serveraddress/user?user=uidvalue`