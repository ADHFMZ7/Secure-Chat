from fastapi import APIRouter, HTTPException, WebSocket
from typing import Annotated
from db import get_user, get_session, create_user

router = APIRouter()

@router.websocket("/chat")
async def connect(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_json()
        await websocket.send_text(f"Message text was: {data}")