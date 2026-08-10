# POST /social  
Post with `token` and `message` like: `{"token":"<str>","message":"<str>"}`   
Returns success and message id.  
Posts the message
  
Post with `token`, `messageid`, and `newmessage` (W.I.P.)  
Returns success and message id.   
Edits the message.  
  
# GET /social  
`/social?count=<int>&offset=<int>` - Gives you n posts with n offset up to twenty at a time.  
So to get 20 latest posts, `/social?count=20&offset=0` or `/social?count=20`  
To get the 20 after the first 20, so posts 21-40: `/social?count=20&offset=20`  
  
Then searching. `/social?count=<int>&search=<str>` (W.I.P.)  
I don't know yet if I want: Search returns any with the param in username or body, just the body, or different params.  
  
Also get a message by id: `/social?id=<str>` (`<str>` being messageid) (W.I.P.)
