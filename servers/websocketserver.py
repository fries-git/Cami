import asyncio
from websockets.asyncio.server import serve
import json
from helperfuncs import validate, tokentoname

connected = set()

async def process(websocket):
    connected.add(websocket)

    try:
        async for message in websocket:
            try:
                message = json.loads(message)
            except json.JSONDecodeError:
                await websocket.send("Invalid JSON")
                continue
            cmd = message.get("cmd")                    
            token = message.get("token")
            body = message.get("body")
            channel = message.get("channel")

            if validate(token) and body:
                string = json.dumps({"uid": validate(token), "body": body, "channel":channel})
                print(f"User {tokentoname(token)} just sent: {body}")
                for user in connected:
                    await user.send(string)
            else:
                await websocket.send("Token or body missing.")

    finally:
        connected.remove(websocket)

async def main():
    portuse = 5614
    print(f"Running on port: {portuse}")
    server = await serve(process, "localhost", 5614)
    await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())