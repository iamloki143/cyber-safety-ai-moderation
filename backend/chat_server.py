from fastapi import WebSocket
from backend.moderation import moderate_text

connections = []

async def handle_chat(websocket: WebSocket):

    await websocket.accept()
    connections.append(websocket)

    while True:

        message = await websocket.receive_text()

        result = moderate_text(message)

        if result["status"] == "blocked":

            await websocket.send_text(
                f"⚠ Message blocked: {result['reason']}"
            )

        else:

            for connection in connections:
                await connection.send_text(message)