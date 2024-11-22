from fastapi import APIRouter, Form, HTTPException, Depends, Response
from typing import Annotated
# from db import get_user, get_session, create_user, session_exists
from db import get_user, create_user
from dependencies import get_db
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

    # if (session := session_exists(user.username)):
    #     # Session already exists, return it
    #     # This should not be an error later, it should renew session
    #     raise HTTPException(status_code=400, detail="Session already exists")

    # create new session 
    session = "new_session"
    print("Created new session:", session)

    response.set_cookie

    return {"access_token": session,
            "token_type": "bearer"}


@router.post("/register")
async def register(username: Annotated[str, Form()], password: Annotated[str, Form()], db = Depends(get_db)):

    if not (user := await create_user(db, username, password)):
        # User not registered properly.
        raise HTTPException(status_code=400, detail="error registering user")

    return {"id": user[0]}
