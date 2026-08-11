import asyncio
from websockets.asyncio.server import serve
import json
from helperfuncs import validate, tokentoname

channels = {}

def addchannel(name, password):
    channels[name] = {
        "password": password,
        "clients": []
    }
    print(f"New channel added named: {name}")

def addtochannel(name, ws):
    channels[name].append(ws)

async def process(websocket):
    try:
        async for message in websocket:
            data = json.loads(message)
            if data:
                cmd = data["cmd"]
                if cmd:
                    if cmd == "send":
                        channel = data["channel"]
                        if channel:
                            if channel in channels:
                                for ws in channels[channel]:
                                    await ws.send(message)
                    elif cmd == "join":
                        channel = data["channel"]
                        password = data["password"]

                        if channel and password:

            else:
                await websocket.send("No valid data passed.")

    except Exception as e: 
        print(f"Connection error: {e}") 

    finally:
        for clients in channels.values():
            if websocket in clients: 
                clients.remove(websocket)

async def main():
    portuse = 5614
    print(f"Running on port: {portuse}")
    server = await serve(process, "localhost", 5614)
    await server.serve_forever()

if __name__ == "__main__":
    addchannel("general", "")
    asyncio.run(main())
