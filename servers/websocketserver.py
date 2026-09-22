import asyncio
from websockets.asyncio.server import serve, broadcast
import json
import logger
from helperfuncs import tokentoname, validate, makejsonerror, makejsonsuccess

connected_clients = set()

async def chat_handler(websocket):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            try:
                message = json.loads(message)
            except json.JSONDecodeError:
                await websocket.send(json.dumps(makejsonerror("Invalid JSON")))
                continue
            try:
                token = message["token"]
                content = message["body"]
                if validate(token):
                    data = {"username":tokentoname(token), "body":content}
                    broadcast(connected_clients, json.dumps(makejsonsuccess(data)))
                else:
                    await websocket.send(json.dumps(makejsonerror("Invalid token")))
            except Exception as e:
                e = str(e)
                await websocket.send(json.dumps(makejsonerror(e)))
                logger.error(e)
    finally:
        connected_clients.remove(websocket)

async def main():
    portuse = 5615

    async with serve(chat_handler, "localhost", portuse):
        logger.info(f"Running on port {portuse}")
        await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())