from fastapi import WebSocket

class ConnectionManager:
    """
    Manages active websocket connections
    """

    def __init__(self):
        self.connections = {}

    def add_connection(self, ws: WebSocket, user_id: int):
        self.connections[user_id] = ws

    def remove_connection(self, user_id: int):
        if user_id in self.connections:
            del self.connections[user_id]

    def get_active_users(self):
        if len(self.connections) == 0:
            return []
        return list(self.connections.keys())

    def get_user_connection(self, user_id: int) -> WebSocket | None:
        return self.connections.get(user_id, None)

    def broadcast_message(self):
        pass