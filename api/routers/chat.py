from fastapi import APIRouter, WebSocketException, WebSocket, Depends
from typing import Annotated, Dict
# from db import get_user, get_session, create_user 
from models import Message
from dependencies import get_db

router = APIRouter()

#TODO: 
#   - Make the websocket require a valid session
#   - implement messaging broadcast to clients in chat room

@router.websocket("/chat")
async def connect(websocket: WebSocket, db = Depends(get_db)):
    await websocket.accept()

    # while True:
    #     data = await websocket.receive_json()
    #     await websocket.send_text(f"Message text was: {data}")
   
    while True:
        payload = await websocket.receive_json()


        # TODO: handle errors when the payload is not a valid message
        message = Message(**payload)

        # for user in users_in(message.chat_id):
        #     # TODO: Change this to id later
        #     socket = active_connections[user.username]
        #
        #     print(f"Sent message to {user.username} at {message.timestamp}")
        #
        #     await socket.send_json(message)
