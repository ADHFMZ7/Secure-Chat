from fastapi import WebSocket

class ConnectionManager:
    """
    Manages active websocket connections
    """

    def __init__(self):
        self.connections = {}

    async def add_connection(self, ws: WebSocket, user_id: int):
        self.connections[user_id] = ws
        print(f"Added connection for user {user_id}") 
        await self.broadcast_message("went-online", {"user_id": user_id})

    async def remove_connection(self, user_id: int):
        print(f"Removed connection for user {user_id}")
        if user_id in self.connections:
            del self.connections[user_id]
      
        await self.broadcast_message("went-offline", {"user_id": user_id}) 
        

    def get_active_users(self):
        if len(self.connections) == 0:
            return []
        return list(self.connections.keys())

    def get_user_connection(self, user_id: int) -> WebSocket | None:
        return self.connections.get(user_id, None)

    async def broadcast_message(self, type, message):
        for connection in self.connections.values():
            await connection.send_json({"type": type, "body": message})