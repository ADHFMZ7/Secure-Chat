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
        self.connections[user_id].close()
        del self.connections[user_id]

    def get_active_connections(self):
        return self.connections

    def get_user_connection(self, user_id: int) -> WebSocket | None:
        return self.connections.get(user_id, None)

    def broadcast_message(self):
        pass