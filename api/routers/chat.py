from fastapi import APIRouter, HTTPException, WebSocket
from typing import Annotated
from db import get_user, get_session, create_user
from models import Message

router = APIRouter()


#TODO: 
#   - Make the websocket require a valid session
#   - implement messaging broadcast to clients in chat room

@router.websocket("/chat")
async def connect(websocket: WebSocket):
    await websocket.accept()

    # while True:
    #     data = await websocket.receive_json()
    #     await websocket.send_text(f"Message text was: {data}")
   

    while True:
        payload = await websocket.receive_json()
       
        # TODO: handle errors when the payload is not a valid message
        message = Message(**payload)
       
         
        
        