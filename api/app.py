from fastapi import FastAPI, Form
from typing import Annotated
from db import get_user, get_session, create_user

app = FastAPI()

# TODO: add error handling

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/login")
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
        print("User does not exist")
        # Username does not exist error
        return
    
    if user.password != password:
        print("Incorrect password")
        # Incorrect password error
        return

    if (session := get_session(user.username)):
        # Session already exists, return it
        print("Session already exists")
        return session

    # create new session 
    session = "new_session"
    print("Created new session:", session)
    return {"session": session}


@app.post("/register")
async def register(username: Annotated[str, Form()], password: Annotated[str, Form()]):

    if not (user := create_user(username, password)):
        # User not registered properly.
        print("Error registering user")
        return

    return {"id": user.username}
