from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import base64
import os
from fastapi import APIRouter, HTTPException, Depends
from aiosqlite import Connection
from db import get_user, get_db

router = APIRouter()

@router.post("/initiate_chat")
async def initiate_chat(requester: str, recipient: str, db: Connection = Depends(get_db)):
    """
    Initiates a secure chat session between two users.

    Parameters:
        - requester: str - The username of the user initiating the chat.
        - recipient: str - The username of the user to chat with.

    Returns:
        - dict: Encrypted messages for both users.
    """
    # Fetch session keys for both users
    requester_data = await get_user(db, requester)
    recipient_data = await get_user(db, recipient)

    if not requester_data or not recipient_data:
        raise HTTPException(status_code=404, detail="User(s) not found")

    requester_session_key = requester_data[5]  # Assuming session key is stored in column 5
    recipient_session_key = recipient_data[5]

    # Generate a shared session key for both users
    shared_session_key = os.urandom(32)

    # Encrypt messages for both users
    requester_cipher = AES.new(requester_session_key.encode(), AES.MODE_CBC)
    recipient_cipher = AES.new(recipient_session_key.encode(), AES.MODE_CBC)

    message_for_requester = {
        "shared_key": base64.b64encode(requester_cipher.encrypt(pad(shared_session_key, AES.block_size))).decode(),
        "recipient": recipient
    }

    message_for_recipient = {
        "shared_key": base64.b64encode(recipient_cipher.encrypt(pad(shared_session_key, AES.block_size))).decode(),
        "requester": requester
    }

    return {"message_for_requester": message_for_requester, "message_for_recipient": message_for_recipient}

@router.post("/verify_chat")
async def verify_chat(nonce: str, shared_key: str):
    """
    Verifies a chat session with mutual authentication.

    Parameters:
        - nonce: str - A random value for authentication.
        - shared_key: str - The shared session key.

    Returns:
        - dict: Confirmation of successful authentication.
    """
    shared_key = base64.b64decode(shared_key)

    # Decrypt nonce and generate a response
    cipher = AES.new(shared_key, AES.MODE_CBC)
    decrypted_nonce = unpad(cipher.decrypt(base64.b64decode(nonce)), AES.block_size)

    # Generate a new nonce as a response
    response_nonce = os.urandom(16)
    encrypted_response = base64.b64encode(cipher.encrypt(pad(response_nonce, AES.block_size))).decode()

    return {"response_nonce": encrypted_response}