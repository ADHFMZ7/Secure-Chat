from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    """
    Manages active websocket connections
    """

    def __init__(self):
        self.connections = {}

    async def add_connection(self, ws: WebSocket, user_id: int, username: str):
        await ws.accept()
        self.connections[user_id] = ws
        print(f"Added connection for user {user_id}") 
        await self.broadcast_message("went-online", {"user_id": user_id, "username": username})

    async def remove_connection(self, user_id: int, username: str):
        print(f"Removed connection for user {user_id}")
        if user_id in self.connections:
            del self.connections[user_id]
            await self.broadcast_message("went-offline", {"user_id": user_id, "username": username}) 
        

    def get_active_users(self):
        if len(self.connections) == 0:
            return []
        return list(self.connections.keys())

    def get_user_connection(self, user_id: int) -> WebSocket | None:
        return self.connections.get(user_id, None)

    async def broadcast_message(self, type: str, message: Dict):
        for connection in self.active_connections.values():
            try:
                await connection.send_json({"type": type, "body": message})
            except Exception as e:
                print(f"Error sending message: {e}")