from fastapi import FastAPI, Form
from typing import Annotated
from db import get_user, get_session

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/login")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()], ):
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
          
        # Username does not exist error
        return
    
    if user.password != password:
        # Incorrect password error
        return

    if (session := get_session(user.username)):
        # Session already exists, return it
        return session

    # create new session 
    session = "new_session"

    return {"session": session}


@app.get("/register")
async def register():
    id = 0
    return {"id": id}

