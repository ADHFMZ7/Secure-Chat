from fastapi import APIRouter, Form, HTTPException, Depends, Response
from typing import Annotated
from db import get_user, create_user, get_session_username, create_session, delete_session
from dependencies import get_current_user, get_db
from aiosqlite import Connection

from security import validate_user

router = APIRouter()

@router.post("/login")
async def login(username: Annotated[str, Form()], 
                password: Annotated[str, Form()], 
                db: Connection = Depends(get_db)):
    """
    Endpoint for user login. Returns an oauth2 token if successful.

    Input:
        - username
        - password

    Output:
        - access_token
        - token_type
    """

    user_id = validate_user(db, username, password)

    # TODO: change this later
    if (session := await get_session_username(db, username)):
        print(f"session {session[0]} already existed")
        # User already has a session
        # load it and create a new cookie
        raise HTTPException(status_code=400, detail="Session already exists")

    # create new session 
    session_id = await create_session(db, user_id)
    print("Created new session:", session_id)

    return {"access_token": session_id, 
            "token_type": "bearer"}


@router.post("/register")
async def register(username: Annotated[str, Form()], password: Annotated[str, Form()], db = Depends(get_db)):

    if not (user := await create_user(db, username, password)):
        # User not registered properly.
        raise HTTPException(status_code=400, detail="error registering user")

    return {"id": user[0]}

@router.get("/logout")
async def logout(response: Response, user = Depends(get_current_user), db = Depends(get_db)):
   
    if not user:
        raise HTTPException(status_code=400, detail="User not found") 
   
    session_id = await get_session_username(user[1]) 
    await delete_session(db, session_id) 
    await delete_session()
    response.delete_cookie("session_id")
    return {"message": "logged out"}

@router.get("/protected")
async def test_protected(user = Depends(get_current_user)):
    print("successfully authenticated")
    print(user)
    return user
