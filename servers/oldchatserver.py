import asyncio
from websockets.asyncio.server import serve
import json
import os
import requests
from dotenv import load_dotenv
from helperfuncs import validate, save_to_file, getlength, useridtoname, dispnamefromrealname
import uuid as u
import time

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

publicchannels = []
lockedchannels = []

webhook = os.getenv("webhook")
token = os.getenv("hooktoken")

channels = {}
passwords = {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.makedirs(os.path.join(BASE_DIR, "channels"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "dbs", "userdata"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "dbs", "social"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "uploads", "imagestorage"), exist_ok=True)

async def webhookpost(body, username):
    avatar = f"https://cami.barfpile.dev/userpfp/{username}"
    data = {
        "content": body,
        "username": username,
        "avatar_url": avatar
    }

    try:
        response = await asyncio.to_thread(
            requests.post,
            webhook,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=5,
        )

        if response.status_code in (200, 201, 204):
            print("Webhook sent successfully!")
        else:
            print(f"Failed to send webhook. Status code: {response.status_code}")

    except Exception as e:
        print(f"Webhook error: {e}")

def addchannel(channel, password, locked):
    channels[channel] = []
    passwords[channel] = password
    path = os.path.join(BASE_DIR, "channels", f"{channel}.json")
    with open(path, "a") as file:
        pass
    if locked and not password:
        publicchannels.append(channel)
        print(f"Added {channel} to public channels.")
    else:
        lockedchannels.append(channel)

def addusertochannel(ws, channel):
    if channel not in channels:
        return False

    if ws not in channels[channel]:
        channels[channel].append(ws)

    return True

addchannel("general", "", True)
addchannel("coding", "", True)
addchannel("off-topic", "", True)
addchannel("shitpost", "", True)
addchannel("friespersonal", "mcdonald", True)

async def echo(websocket):
    for channel in publicchannels:
        addusertochannel(websocket, channel)
    try:
        async for message in websocket:
            # The dreaded block... guh...
            try:
                message = json.loads(message)
            except json.decoder.JSONDecodeError as e:
                await websocket.send("Invalid JSON")
                break

            msgtype = message.get("type")
            channel = message.get("channel")
            msgid = message.get("msgid")
            channel = str(channel).lower()
            password = message.get("password")
            msg = message.get("msg")
            token = message.get("token")
            count = int(message.get("count") or 10)
            offset = int(message.get("offset") or 0)
            genid = str(u.uuid4())

            if msgtype:
                userid = validate(token)
                if userid:
                    if msgtype == "send":
                        if len(msg) <= 500:
                            if channel in channels:
                                if websocket in channels[channel]:
                                    if passwords[channel] != password:
                                        await websocket.send("Incorrect password")
                                        continue

                                    if userid:
                                        dispname = dispnamefromrealname(username)
                                        username = useridtoname(userid)
                                        content = json.dumps({"type": "newmsg", "userid": userid, "username": username, "displayname": dispname, "channel":channel, "message": msg, "msgid": genid, "time": time.time()})
                                        save_to_file(content, f"{channel}.json")
                                        print(f"{username} just said: {msg} in livechat. Channel: {channel}.")

                                        for ws in channels[channel]:
                                            try:
                                                await ws.send(content)
                                            except Exception as e:
                                                print("error:", e)
                                        if webhook:
                                            if not username == "Rotur Link":
                                                asyncio.create_task(webhookpost(msg, username))
                                    else:
                                        await ws.send("Invalid token. (Token resets whenever you login.)")
                        else:
                            await websocket.send("Message too long! (500 Char Limit)")

                    elif msgtype == "joinchannel":
                        if channel in channels:
                            if passwords[channel] != password:
                                await websocket.send("Incorrect password")
                                continue
                            print(f"{useridtoname(userid)} just joined {channel}.")
                            addusertochannel(websocket, channel)
                            username = useridtoname(userid)

                            content = json.dumps({
                                "type": "joinedchannel",
                                "userid": userid,
                                "username": username,
                                "channel": channel
                            })

                            for ws in channels[channel]:
                                try:
                                    await ws.send(content)
                                except Exception as e:
                                    print("error:", e)
                        else:
                            await websocket.send("Channel does not exist")

                    elif msgtype == "gethist":
                        histlist = []
                        path = os.path.join(BASE_DIR, "channels", f"{channel}.json")
                        with open(path, 'r', encoding='utf-8') as f:
                            histlist.append(json.dumps(f.readlines()[-count-offset:-offset if offset else None]))
                        await websocket.send(histlist)

                    elif msgtype == "gethistlen":
                        await websocket.send(json.dumps({"type": "histlen","count": getlength(f"{channel}.json")}))

                    elif msgtype == "deletemessage":
                        try:
                            path = os.path.join(BASE_DIR, "channels", f"{channel}.json")
                            with open(path, 'r', encoding='utf-8') as file:
                                data = [json.loads(line) for line in file if line.strip()]
                                message = next((item for item in data if item["msgid"] == msgid and item["userid"] == validate(token)), None)
                                if message:
                                    data.remove(message)
                            with open(path, "w", encoding="utf-8") as file:
                                for item in data:
                                    file.write(json.dumps(item) + "\n")
                            print(f"Deleted message {msgid}")
                            for ws in channels[channel]:
                                try:
                                    await ws.send(json.dumps({"type": "delmsg", "messageid": msgid}))
                                except Exception as e:
                                    await websocket.send(str(e))
                        except Exception as e:
                            await websocket.send(str(e))

                    elif msgtype == "getpublicchannels":
                        await websocket.send(json.dumps(publicchannels))

                    elif msgtype == "createchannel":
                        uid = validate(token)
                        if uid:
                            if channel in channels:
                                await websocket.send("Channel already exists")
                                continue

                            if not channel or len(channel) > 32:
                                await websocket.send("Invalid channel name")
                                continue

                            addchannel(channel, password, False)

                            addusertochannel(websocket, channel)

                            await websocket.send(json.dumps({
                                "type": "channelcreated",
                                "channel": channel
                            }))
                        else:
                            await websocket.send("Invalid token"), 401
                    
                else:
                    await websocket.send("Invalid token. (Token resets whenever you login.)")

            else:
                await websocket.send("Missing msgtype which is like critical information")
    finally:
        for channel, users in list(channels.items()):
            if websocket in users:
                users.remove(websocket)

            if not users and not channel in publicchannels and not channel in lockedchannels:
                del channels[channel]
                del passwords[channel]

                path = os.path.join(BASE_DIR, "channels" f"{channel}.json")

                if os.path.exists(path):
                    os.remove(path)

                print(f"Deleted empty channel: {channel}")

portuse = 5615

async def main():
    server = await serve(echo, "localhost", portuse)
    print (f"Running on port {portuse}")
    await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())