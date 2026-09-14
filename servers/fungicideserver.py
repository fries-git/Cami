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

    userid = None
    name = None

    try:
        async for message in websocket:
            message = json.loads(message)
            token = message.get("token")
            validation = validate(token)

            if validation:
                userid = validation
                name = tokentoname(token)

                msgtype = message.get("type")
                msg = message.get("msg")

                if msgtype == "pos":
                    x = message.get("x")
                    y = message.get("y")
                    room = message.get("room")

                    await broadcast(json.dumps({"type": "pos","x": x,"y": y,"room": room,"userid": userid,"username": name}))
                if msgtype == "join":
                    await broadcast(json.dumps({"type": "join","username": name}))
                    print(f"{name} has joined!")

            else:
                await websocket.send(json.dumps({
                    "type": "error",
                    "error": "Invalid token."
                }))

    except Exception as e:
        print(e)

    finally:
        connected_users.discard(websocket)

        if userid and name:
            await broadcast(json.dumps({"type": "disconnect","userid": userid,"username": name}))
            print(f"{name} has disconnected.")
                 
portuse = 5616

async def main():
    server = await serve(loop, "localhost", portuse)
    print (f"Running on port {portuse}")
    await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())