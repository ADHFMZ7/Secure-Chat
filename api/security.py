from aiosqlite import Connection
from fastapi import HTTPException
from db import get_user

# TODO: Continue implementing new auth system

def hash_password(password: str):
    ...

def verify_password(plaintext_pass: str, hashed_password: str) -> bool:
    ...

def validate_user(session: Connection, username: str, password: str) -> int:

    if (user := get_user(session, username)):
        if verify_password(password, user[2]):
            return user[0]
        else:
            raise HTTPException(status_code=401, detail="Password incorrect")

    raise HTTPException(status_code=404, detail="User does not exist")