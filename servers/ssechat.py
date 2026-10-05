import asyncio
import json

from quart import Quart, Response, request
from quart_cors import cors

from hypercorn.asyncio import serve
from hypercorn.config import Config

from helperfuncs import validate, tokentoname

app = Quart(__name__)
app = cors(app)

clients = set()


@app.get("/chat")
async def chat():
    queue = asyncio.Queue()
    clients.add(queue)

    async def generate():
        try:
            while True:
                try:
                    data = await asyncio.wait_for(queue.get(), timeout=20)
                    yield f"data: {json.dumps(data)}\n\n"
                except asyncio.TimeoutError:
                    yield ": keepalive\n\n"
        finally:
            clients.discard(queue)

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache"}
    )


@app.post("/send")
async def send():
    data = await request.get_json()

    token = data.get("token")
    message = data.get("message")

    if not token:
        return {"cmd": "error", "message": "Missing token"}, 400

    if not message:
        return {"cmd": "error", "message": "Missing message"}, 400

    userid = validate(token)

    if not userid:
        return {"cmd": "error", "message": "Invalid token"}, 401

    for queue in clients.copy():
        await queue.put({
            "cmd": "message",
            "userid": userid,
            "username": tokentoname(token),
            "message": message
        })

    return {
        "cmd": "success",
        "message": "Message sent"
    }


if __name__ == "__main__":
    config = Config()
    config.bind = ["0.0.0.0:5615"]
    config.loglevel = "critical"

    print("Hello SSE")
    asyncio.run(serve(app, config))