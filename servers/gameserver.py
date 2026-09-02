import asyncio
from websockets.asyncio.server import serve
from helperfuncs import validate, useridtoname, dispnamefromrealname, tokentoname
import json

connected_users = set()

async def broadcast(message, ):
    if connected_users:
        await asyncio.gather(*(user.send(message) for user in connected_users),return_exceptions=True)

async def loop(websocket):
    connected_users.add(websocket)

    try:
        async for message in websocket:
            message = json.loads(message)
            token = message.get("token")
            validation = validate(token)
            if validation:
                msgtype = message.get("type")
                msg = message.get("msg")
                try:
                    name = tokentoname(token)
                except Exception as e:
                    pass
                
                if msgtype == "pos":
                    x = message.get("x")
                    y = message.get("y")
                    await broadcast(json.dumps({"type":"pos","x":x,"y":y,"userid":validation,"username":name}))

                if msgtype == "chat":
                    msg = message.get("msg")
                    await broadcast(json.dumps({"type":"chat","msg":msg,"userid":validation,"username":name}))
            else:
                await websocket.send(json.dumps({"type":"error","error":"Invalid token."}))
    
    except Exception as e:
        print(e)

    finally:
        try:
            await broadcast(json.dumps({"type":"disconnect","userid":validate(token),"username":name}))
        except:
            pass
        connected_users.discard(websocket)
                 
portuse = 5616

async def main():
    server = await serve(loop, "localhost", portuse)
    print (f"Running on port {portuse}")
    await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())