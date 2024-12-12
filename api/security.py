from aiosqlite import Connection
from fastapi import HTTPException
from db import get_user

# TODO: Continue implementing new auth system

async def hash_password(password: str):
    #temp
    return password
    ...

async def verify_password(plaintext_pass: str, hashed_password: str) -> bool:
    #temp
    return plaintext_pass == hashed_password

    ...

async def validate_user(session: Connection, username: str, password: str) -> int:

    if (user := await get_user(session, username)):
        if await verify_password(password, user[2]):
            return user[0]
        else:
            raise HTTPException(status_code=401, detail="Password incorrect")

    raise HTTPException(status_code=404, detail="User does not exist")
