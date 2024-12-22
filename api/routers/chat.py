from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .models import ChatCreation, Message
from .database import get_db
from .auth import get_authenticated_user
from .connections import ConnectionManager
from .crud import create_chat, add_user_to_chat, create_message, get_users_in_chat, remove_user_from_chat, is_user_in_chat, get_chats, get_active_users

router = APIRouter()
conns = ConnectionManager()

@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db), user: dict = Depends(get_authenticated_user)):
    await conns.add_connection(websocket, int(user['user_id']), user['username'])
    try:
        while True:
            payload = await websocket.receive_json()
            print(payload)

            if 'type' in payload:
                match payload['type']:
                    case 'create_chat':
                        body = ChatCreation(**payload['body'])
                        chat_id = await create_chat(db, body.user_ids)
                        if not await is_user_in_chat(db, user['user_id'], chat_id):
                            await add_user_to_chat(db, user['user_id'], chat_id)
                        for user_id in body.user_ids:
                            if not await is_user_in_chat(db, user_id, chat_id):
                                await add_user_to_chat(db, user_id, chat_id)
                            if (user_conn := conns.get_user_connection(user_id)):
                                try:
                                    await user_conn.send_json({"type": "chat_created", 
                                                               "body": {"chat_id": chat_id}})
                                except Exception as e:
                                    print(f"Error sending message: {e}")
                    
                    case 'send_message':
                        body = Message(**payload['body'])
                        await create_message(db, **body.model_dump())
                        for user in await get_users_in_chat(db, body.chat_id):
                            if (user_conn := conns.get_user_connection(user['user_id'])):
                                try:
                                    await user_conn.send_json({"type": "message", 
                                                               "body": body.model_dump()})
                                except Exception as e:
                                    print(f"Error sending message: {e}")
                          
                    case 'leave_chat':
                        chat_id = payload['chat_id']
                        await remove_user_from_chat(db, user['user_id'], chat_id)
                        try:
                            await websocket.send_json({"type": "left_chat", 
                                                       "body": {"chat_id": chat_id, 
                                                                "user_id": user['user_id']}})
                        except Exception as e:
                            print(f"Error sending message: {e}")
                        print(f"User {user['username']} left chat {chat_id}")

    except WebSocketDisconnect:
        await conns.remove_connection(int(user['user_id']), user['username'])
    except Exception as e:
        print(f"Error: {e}")
        await conns.remove_connection(int(user['user_id']), user['username'])

@router.get("/chats", response_model=List[dict])
async def get_all_chats(db: Session = Depends(get_db), user: dict = Depends(get_authenticated_user)):
    try:
        return await get_chats(db, user['user_id'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users", response_model=List[dict])
async def get_all_active_users(db: Session = Depends(get_db), user: dict = Depends(get_authenticated_user)):
    try:
        return await get_active_users(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))