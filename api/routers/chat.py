from fastapi import APIRouter, WebSocketDisconnect, WebSocketException, WebSocket, Depends
from typing import Annotated, Dict

from models import Message, ChatCreation
from db import get_db, create_chat, add_user_to_chat, get_users_in_chat, create_message, get_chats_for_user, get_messages_for_chat, remove_user_from_chat, get_user_by_id
from security import ws_get_user, get_authenticated_user
from connections import ConnectionManager

router = APIRouter()
conns = ConnectionManager()

async def broadcast_to_chat(db, chat_id: int, message: str):
    users = await get_users_in_chat(db, chat_id)
    for user in users:
        if (user_conn := conns.get_user_connection(user['user_id'])):
            await user_conn.send_json({"type": "notification", "message": message})

@router.websocket("/chat")
async def connect(websocket: WebSocket, db = Depends(get_db), user = Depends(ws_get_user)):

    if user['username'] in conns.connections:
        return
   
    print(f"User {user['username']} connected")
    await conns.add_connection(websocket, int(user['user_id']), user['username'])

    try:
        # Notify all users in the chat that a new user has connected

        while True:
            payload = await websocket.receive_json()
            print(payload)

            # Probably use a better validation method for this later
            if 'type' in payload:
              
                match payload['type']:
                    case 'create_chat':
                        body = ChatCreation(**payload['body'])  
                        chat_id = await create_chat(db, body.user_ids)
                        for user_id in body.user_ids: 
                            if (user_conn := conns.get_user_connection(user_id)):
                                await user_conn.send_json({"type": "chat_created", 
                                                           "body": {"chat_id": chat_id}})
                                                       
                    
                    case 'send_message': 
                        body = Message(**payload['body'])
                        # Check if chat exists 
                        # Check if user is in chat
                        await create_message(db, **body.model_dump()) 
                        for ruser in await get_users_in_chat(db, body.chat_id):
                            if (user_conn := conns.get_user_connection(ruser['user_id'])):
                                await user_conn.send_json({"type": "message", 
                                                              "body": body.model_dump()
                                                              })
                          
                    case 'leave_chat':
                        chat_id = payload['chat_id']
                        await remove_user_from_chat(db, user['user_id'], chat_id)
                        await websocket.send_json({"type": "left_chat", 
                                                    "body": {"chat_id": chat_id, 
                                                             "user_id": user['user_id']}}) 
                        print(f"User {user['username']} left chat {chat_id}")
                   
                    case default:
                        await websocket.send_json({"Message": "Invalid message type"}) 
               
            else:
                # invalid message
                return

    except WebSocketDisconnect:
        print(user)
        await conns.remove_connection(int(user['user_id']), user['username'])
    except Exception as e:
        print(f"Error: {e}")
        await conns.remove_connection(int(user['user_id']), user['username'])

@router.get("/chats")
async def get_chats(db = Depends(get_db),
                    user = Depends(get_authenticated_user)):
   
    chats = await get_chats_for_user(db, user['user_id'])
    chat_ids = [chat['chat_id'] for chat in chats] 
  
    responses = {}
   
    for c_id in chat_ids:
        messages = await get_messages_for_chat(db, c_id)
        users_in_chat = await get_users_in_chat(db, c_id)

        ms = []
        users_list = []

        for message in sorted(messages, key=lambda x: x['timestamp']):
            sender = await get_user_by_id(db, message['sent_by'])
            ms.append({
                "sender_id": message['sent_by'],
                "sender_name": sender['username'],
                "chat_id": message['chat_id'],
                "content": message['content'],
                "timestamp": message['timestamp']
            })

        for user in users_in_chat:
            user_details = await get_user_by_id(db, user['user_id'])
            users_list.append({
                "user_id": user['user_id'],
                "username": user_details['username']
            })

        responses[c_id] = {
            "messages": ms,
            "users": users_list
        }

    return responses

@router.get("/users")
async def get_connected_users(user = Depends(get_authenticated_user), db = Depends(get_db)):
    users = {}
    for user_id in conns.get_active_users():
        if user_id == user['user_id']:
            continue
        user = await get_user_by_id(db, user_id)
        users[user['user_id']] = user['username']
    return users