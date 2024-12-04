from fastapi import APIRouter, Form, HTTPException, Depends, Response
from typing import Annotated
from db import get_user, create_user, get_session_username, create_session
from dependencies import get_current_user, get_db
from aiosqlite import Connection

router = APIRouter()

@router.post("/login")
async def login(response: Response,
                username: Annotated[str, Form()], 
                password: Annotated[str, Form()], 
                db: Connection = Depends(get_db)):
    """
    Endpoint for user login.

    Input:
        - username
        - password

    Output:
        - session-id
    """

    # Database query to see if the username exists
    if not (user := await get_user(db, username)):
        raise HTTPException(status_code=404, detail="User does not exist")

    if user[2] != password:
        print("Incorrect password")
        raise HTTPException(status_code=401, detail="Password incorrect")

    if (session := await get_session_username(db, username)):
        print(f"session {session[0]} already existed")
        # User already has a session
        # load it and create a new cookie
        raise HTTPException(status_code=400, detail="Session already exists")

    # create new session 
    session_id = username + "token"
    print("Created new session:", session)

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS,
        samesite="none",
        domain="localhost"
    )

    print(response.headers)

    return {"session_id": session_id}


@router.post("/register")
async def register(username: Annotated[str, Form()], password: Annotated[str, Form()], db = Depends(get_db)):

    if not (user := await create_user(db, username, password)):
        # User not registered properly.
        raise HTTPException(status_code=400, detail="error registering user")

    return {"id": user[0]}

@router.get("/protected")
async def test_protected(user = Depends(get_current_user)):
    print("successfully authenticated")
    return user
