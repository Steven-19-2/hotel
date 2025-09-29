from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        text = json.dumps(message)
        disconnected = []
        for conn in self.active_connections:
            try:
                await conn.send_text(text)
            except WebSocketDisconnect:
                disconnected.append(conn)
        for conn in disconnected:
            self.disconnect(conn)

manager = ConnectionManager()

@app.websocket("/ws/bookings")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()  # Echo or ping if desired
            await websocket.send_text(f"server received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Example usage: broadcast when a booking is created
# from somewhere in your app:
# await manager.broadcast({"type": "booking_created", "booking_id": 123})
