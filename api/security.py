from aiosqlite import Connection
from fastapi import HTTPException, Security, Depends, WebSocketException, status
from fastapi.security import OAuth2PasswordBearer
from db import get_user, get_session, get_user_by_session, get_db
import hashlib
import hmac

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

async def verify_password(plaintext_password: str, hashed_password: str) -> bool:
    return hmac.compare_digest(hash_password(plaintext_password), hashed_password)

async def validate_user(session: Connection, username: str, password: str) -> int:

    if (user := await get_user(session, username)):
        if await verify_password(password, user['hashed_password']):
            return user['user_id']
        else:
            raise HTTPException(status_code=401, detail="Password incorrect")

    raise HTTPException(status_code=404, detail="User does not exist")

async def ws_get_user(db: Connection = Depends(get_db), token: str = None,):

    print("websocket sent token: ", token)
    session = await get_session(db, token)
    user = await get_user_by_session(db, token)

    if not session or not user:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    
    return user


async def get_authenticated_user(token: str = Security(oauth_scheme),
                                 db: Connection = Depends(get_db)):

    print("CONNECTED WITH SESSIONID:", token)

    session = await get_session(db, token)
    user = await get_user_by_session(db, token)

    if not session or not user:
        raise HTTPException(status_code=403, detail="No session found")
    
    return user