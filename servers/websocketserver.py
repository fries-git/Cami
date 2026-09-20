import asyncio
from websockets.asyncio.server import serve, broadcast
import json
import logger
from helperfuncs import tokentoname, validate, makejsonerror

connected_clients = set()

async def chat_handler(websocket):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            try:
                message = json.loads(message)
                token = message["token"]
                content = message["body"]
                if validate(token):
                    broadcast(connected_clients, f"{tokentoname(token)} - {content}")
                else:
                    await websocket.send(makejsonerror("Invalid token"))
            except Exception as e:
                logger.error(e)
    finally:
        connected_clients.remove(websocket)

async def main():
    async with serve(chat_handler, "localhost", 8765):
        print("Chat server running on ws://localhost:8765")
        await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())