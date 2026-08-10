# Live Chatting System  

The live chatting system is an sse connection. Essentially, you run a get request on the endpoint /livechat, and it is a constant feed of data, and you run posts on the same endpoint to chat.  
Post: `{"token": <str>, "body": <str>}`  
Recieve: `{"userid": <str>, "body": <str>, "timestamp": <unix timestamp>}`  