from fastapi import APIRouter, WebSocketDisconnect, WebSocketException, WebSocket, Depends
from typing import Annotated, Dict

from models import Message, ChatCreation
from db import get_db, create_chat, add_user_to_chat, get_users_in_chat, create_message, get_chats_for_user, get_messages_for_chat
from security import ws_get_user, get_authenticated_user
from connections import ConnectionManager

router = APIRouter()
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
                       
                        if not chat_id:
                            await websocket.send_json({"Message": "Failed to create chat"})
                            return
                        
                        for user_id in body.user_ids: 
                           
                            # Check if user exists
                            
                            await add_user_to_chat(db, user_id, chat_id)
                            if (user_conn := conns.get_user_connection(user_id)):
                                await user_conn.send_json("Youre in new chat with id " + str(chat_id) + "!")
                                
                    case 'send_message': 
                        body = Message(**payload['body'])
                     
                        # Check if chat exists 
                      
                        # Check if user is in chat
                         
                        await create_message(db, **body.model_dump()) 
                      
                        for user in await get_users_in_chat(db, body.chat_id):
                            if (user_conn := conns.get_user_connection(user['user_id'])):
                                await user_conn.send_json(f"Received message \'{body.content}\' from user with id {body.sender_id}")
                          
                    case 'leave_chat':
                        pass 
                    case '':          
                        pass
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


@router.get("/chats")
async def get_chats(db = Depends(get_db),
                    user = Depends(get_authenticated_user)):
   
    chats = await get_chats_for_user(db, user['user_id'])
    chat_ids = [chat['chat_id'] for chat in chats] 
  
    responses = {}
   
    for c_id in chat_ids:
        responses[c_id] = await get_messages_for_chat(db, c_id)
        messages = await get_messages_for_chat(db, c_id)

        ms = []

        for message in sorted(messages, key=lambda x: x['timestamp']):
            ms.append({
                "sender_id": message['sent_by'],
                "chat_id": message['chat_id'],
                "content": message['content'],
                "timestamp": message['timestamp']
            })
        responses[c_id] = ms

    return responses

@router.get("/users")
async def get_connected_users(user = Depends(get_authenticated_user)):
    return conns.get_active_users()