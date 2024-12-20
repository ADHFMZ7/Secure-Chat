from fastapi import APIRouter, WebSocketDisconnect, WebSocketException, WebSocket, Depends
from typing import Annotated, Dict

from models import Message, ChatCreation
from db import get_db, create_chat, add_user_to_chat, get_users_in_chat, create_message
from security import ws_get_user
from connections import ConnectionManager

router = APIRouter()

#TODO: 
#   - implement messaging broadcast to clients in chat room

conns = ConnectionManager()

@router.websocket("/chat")
async def connect(websocket: WebSocket, db = Depends(get_db), user = Depends(ws_get_user)):

    if user['username'] in conns.connections:
        return
   
    await websocket.accept()
    print(f"User {user['username']} connected")
    print(user['user_id'])
    conns.add_connection(websocket, int(user['user_id']))

    try:

        while True:
            payload = await websocket.receive_json()
            print(payload)

            # Probably use a better validation method for this later
            if 'type' in payload:
              
                match payload['type']:
                   
                    case 'create_chat':
                        body = ChatCreation(**payload['body'])  
                        chat_id = await create_chat(db) 
                        
                        for user_id in body.user_ids:
                            await add_user_to_chat(db, user_id, chat_id)
                            if (user_conn := conns.get_user_connection(user_id)):
                                await user_conn.send_json("Youre in new chat with id " + str(chat_id) + "!")
                                
                    case 'send_message': 
                        body = Message(**payload['body'])
                      
                        await create_message(db, **body.model_dump()) 
                      
                        for user in await get_users_in_chat(db, body.chat_id):
                            if (user_conn := conns.get_user_connection(user['user_id'])):
                                await user_conn.send_json(f"Received message \'{body.content}\' from user with id {body.sender_id}")
                                        
                    case default:
                        await websocket.send_json({"Message": "Invalid message type"}) 
                
            else:
                # invalid message
                return

    except (WebSocketDisconnect,  WebSocketException):
        conns.remove_connection(user['username'])
        print(f"User {user['username']} disconnected")
        await websocket.close()
        return