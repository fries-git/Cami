import asyncio
from websockets.asyncio.server import serve
import json
import os

from helperfuncs import validate, save_to_file, getlength, useridtoname

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  

channels = {}
passwords = {}

def addchannel(channel, password):
    channels[channel] = []
    passwords[channel] = password

def addusertochannel(ws, channel):
    if channel not in channels:
        return False

    if ws not in channels[channel]:
        channels[channel].append(ws)

    return True

addchannel("general", "")

async def echo(websocket):
    addusertochannel(websocket, "general")
    try:
        async for message in websocket:
            message = json.loads(message)
            msgtype = message.get("type")
            channel = message.get("channel")
            password = message.get("password")
            msg = message.get("msg")
            token = message.get("token")
            count = message.get("count")
            offset = message.get("offset")

            if msgtype:
                userid = validate(token)
                if userid:
                    if msgtype == "send":
                        if channel in channels:
                            if websocket in channels[channel]:
                                if passwords[channel] != password:
                                    await websocket.send("Incorrect password")
                                    continue

                                if userid:
                                    username = useridtoname(userid)
                                    content = json.dumps({"type": "newmsg", "userid": userid, "username": username, "message": msg})
                                    save_to_file(content, "history.json")
                                    print(f"{username} just said: {msg} in livechat.")
                                    for ws in channels[channel]:
                                        try:
                                            await ws.send(content)
                                        except Exception as e:
                                            print("error:", e)
                                else:
                                    await ws.send("Invalid token. (Token resets whenever you login.)")

                    elif msgtype == "joinchannel":
                        if channel in channels:
                            if passwords[channel] != password:
                                await websocket.send("Incorrect password")
                                continue

                            addusertochannel(websocket, channel)

                    elif msgtype == "gethist":
                        histlist = []
                        path = os.path.join(BASE_DIR,"history.json")
                        with open(path, 'r', encoding='utf-8') as f:
                            histlist.append(json.dumps(f.readlines()[-count:]))
                        await websocket.send(histlist)

                    elif msgtype == "gethistlen":
                        await websocket.send(str(getlength("history.json")))
                    
                else:
                    await websocket.send("Invalid token. (Token resets whenever you login.)")

            else:
                await websocket.send("Missing msgtype which is like critical information")
    finally:
        for users in channels.values():
            if websocket in users:
                users.remove(websocket)

portuse = 5615

async def main():
    server = await serve(echo, "localhost", portuse)
    print (f"Running on port {portuse}")
    await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())