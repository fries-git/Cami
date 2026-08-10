import asyncio
from websockets.asyncio.server import serve
import json
from helperfuncs import validate, tokentoname

channels = []
passwords = []

def addchannel(name, password):
    channels.append(f"{name}[]")
    passwords.append(password)
    print(f"New channel added named: {name} with the password: {password}")

async def process(websocket):
    try:
        async for message in websocket:
            await websocket.send(message)

async def main():
    portuse = 5614
    print(f"Running on port: {portuse}")
    server = await serve(process, "localhost", 5614)
    await server.serve_forever()

if __name__ == "__main__":
    
    asyncio.run(main())
