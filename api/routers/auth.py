from fastapi import APIRouter, Form, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from aiosqlite import Connection
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import secrets
from db import get_user, create_user, get_session_username, create_session
from dependencies import get_current_user, get_db
from aiosqlite import Connection
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import secrets

router = APIRouter()

# Load KDC's public key once
with open("kdc_public.pem", "rb") as pub_key_file:
    kdc_public_key = RSA.import_key(pub_key_file.read())

# Load KDC's private key once
with open("kdc_private.pem", "rb") as priv_key_file:
    kdc_private_key = RSA.import_key(priv_key_file.read())
kdc_cipher = PKCS1_OAEP.new(kdc_private_key)


@router.post("/register")
async def register(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    master_key: Annotated[str, Form()],
    db=Depends(get_db)
):
    """
    Register a new user with username, password, and master key.
    """
    # Encrypt master key using KDC's public key
    kdc_cipher_public = PKCS1_OAEP.new(kdc_public_key)
    encrypted_master_key = kdc_cipher_public.encrypt(master_key.encode())

    # Save encrypted master key in the database (avoid file storage)
    if not (user := await create_user(db, username, password, encrypted_master_key)):
        raise HTTPException(status_code=400, detail="Error registering user")

    return {"id": user[0]}


@router.post("/login")
async def login(
    response: Response,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: Connection = Depends(get_db)
):
    """
    Log in a user and establish a session.
    """
    # Check if user exists
    if not (user := await get_user(db, username)):
        raise HTTPException(status_code=404, detail="User does not exist")

    if user[2] != password:
        raise HTTPException(status_code=401, detail="Password incorrect")

    # Check if a session already exists
    if (session := await get_session_username(db, username)):
        raise HTTPException(status_code=400, detail="Session already exists")

    # Decrypt the master key
    encrypted_master_key = user[4]  # Assuming encrypted master key is stored in the database
    decrypted_master_key = kdc_cipher.decrypt(encrypted_master_key).decode()

    # Create a secure session ID
    session_id = secrets.token_hex(32)
    await create_session(db, username, session_id)

    # Set session ID in secure cookie
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=True,  # True for production with HTTPS
        samesite="Strict",  
    )

    return {"session_id": session_id}


@router.get("/protected")
async def test_protected(user=Depends(get_current_user)):
    """
    Protected endpoint to test authentication.
    """
    return {"message": "Successfully authenticated", "user": user}
