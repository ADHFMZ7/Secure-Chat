from fastapi import APIRouter, Form, HTTPException
from typing import Annotated
from db import get_user, get_session, create_user

router = APIRouter()


@router.post("/login")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    """
    Endpoint for user login.

    Input:
        - username
        - password

    Output:
        - session-id
    """

    # Database query to see if the username exists

    if not (user := get_user(username)):
        raise HTTPException(status_code=404, detail="User does not exist")
    
    if user.password != password:
        print("Incorrect password")
        raise HTTPException(status_code=401, detail="Password incorrect")

    if (session := get_session(user.username)):
        # Session already exists, return it
        # This should not be an error later, it should renew session
        raise HTTPException(status_code=400, detail="Session already exists")

    # create new session 
    session = "new_session"
    print("Created new session:", session)
    return {"session": session}


@router.post("/register")
async def register(username: Annotated[str, Form()], password: Annotated[str, Form()]):

    if not (user := create_user(username, password)):
        # User not registered properly.
        print("Error registering user")
        return

    return {"id": user.username}


