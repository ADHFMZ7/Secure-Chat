from fastapi import APIRouter, Form, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from aiosqlite import Connection

from db import create_user, get_session_username, create_session, delete_session, get_db
from security import validate_user, hash_password, get_authenticated_user

router = APIRouter()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
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

    username, password = form_data.username, form_data.password
    user_id = await validate_user(db, username, password)

    if (session := await get_session_username(db, username)):
        print(f"session {session['session_id']} already existed")
        await delete_session(db, session['session_id'])

    # create new session 
    session_id = await create_session(db, user_id)
    print("Created new session:", session_id)


    return {"access_token": session_id, 
            "token_type": "bearer"}


@router.post("/register")
async def register(username: Annotated[str, Form()], 
                   password: Annotated[str, Form()], 
                   db = Depends(get_db)):

    hashed_password = hash_password(password)

    if not (user := await create_user(db, username, hashed_password)):
        # User not registered properly.
        raise HTTPException(status_code=400, detail="error registering user")

    return {"id": user['user_id']}



@router.get("/logout")
async def logout(user = Depends(get_authenticated_user), db = Depends(get_db)):
    print(user) 
   
    if not (session := await get_session_username(db, user['username'])):
        print('session does not exist')
        return {"message": "logged out"}

    await delete_session(db, session['session_id']) 
    return {"message": "logged out"}

@router.get("/protected")
async def test_protected(user = Depends(get_authenticated_user)):
    print("successfully authenticated")
    print(user)
    return user
