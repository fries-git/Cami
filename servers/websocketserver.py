import asyncio
from websockets.asyncio.server import serve
import json
from helperfuncs import validate, tokentoname

channels = [{"channelname":"open","password":""}]
channelnames = ["open"]

connected = set()
connectedauth = []
print(connectedauth)

def get_channel(name):
    for channel in channels:
        if channel["channelname"] == name:
            return channel
    return None

async def process(websocket):
    connected.add(websocket)
    connectedauth.add(websocket)
    try:
        async for message in websocket:
            try:
                message = json.loads(message)

            except json.JSONDecodeError:
                await websocket.send("Invalid JSON")
                continue
        
            cmd = message.get("cmd")     
            token = message.get("token")   
            password = message.get("password")

            if cmd == "send":
                body = message.get("body")
                channel = message.get("channel")
                if validate(token) and body and channel:
                    if channel in channels:
                        string = json.dumps({"cmd": cmd, "uid": validate(token), "body": body, "channel": channel})
                        print(f"User {tokentoname(token)} just sent: {body}")
                        for user in connected:
                            await user.send(string)
        
                    else:
                        await websocket.send("Channel doesn't exist.")
                        continue

                else:
                    await websocket.send("Token or body missing.")
                    continue

            # This code is sooo good :3

    finally:
        connected.remove(websocket)
        connectedauth.remove(websocket)

async def main():
    portuse = 5614
    print(f"Running on port: {portuse}")
    server = await serve(process, "localhost", 5614)
    await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())