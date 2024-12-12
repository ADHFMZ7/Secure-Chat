from aiosqlite import Connection
from fastapi import HTTPException
from db import get_user


def hash_password(password: str):
    # TODO: Implement real hashing algorithm
    return password

async def verify_password(plaintext_password: str, hashed_password: str) -> bool:
    # TODO: Implement real hash verification
    return hash_password(plaintext_password) == hashed_password

async def validate_user(session: Connection, username: str, password: str) -> int:

    if (user := await get_user(session, username)):
        if await verify_password(password, user['hashed_password']):
            return user['user_id']
        else:
            raise HTTPException(status_code=401, detail="Password incorrect")

    raise HTTPException(status_code=404, detail="User does not exist")
