from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    """
    Manages active websocket connections
    """

    def __init__(self):
        self.connections: Dict[int, WebSocket] = {}

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

    def get_active_users(self) -> List[int]:
        return list(self.connections.keys())

    def get_user_connection(self, user_id: int) -> WebSocket | None:
        return self.connections.get(user_id, None)

    async def broadcast_message(self, type: str, message: Dict):
        disconnected_users = []
        for user_id, connection in self.connections.items():
            try:
                await connection.send_json({"type": type, "body": message})
            except WebSocketDisconnect:
                disconnected_users.append(user_id)
            except Exception as e:
                print(f"Error sending message to user {user_id}: {e}")
        
        for user_id in disconnected_users:
            await self.remove_connection(user_id, "Unknown")

    async def handle_disconnect(self, user_id: int, username: str):
        if user_id in self.connections:
            await self.remove_connection(user_id, username)