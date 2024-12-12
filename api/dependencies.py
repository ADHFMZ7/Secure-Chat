from fastapi import Security, HTTPException
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from aiosqlite import connect, Row, Connection

from db import DATABASE_URL, get_session, get_user, get_user_by_session

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_db():
    """
    Fetches database session     
    """
    async with connect(DATABASE_URL) as db:
        db.row_factory = Row 
        yield db


async def get_current_user(session_id: str = Security(oauth_scheme),
                           db: Connection = Depends(get_db)):

    print("CONNECTED WITH SESSIONID:", session_id)

    session = await get_session(db, session_id)
    user = await get_user_by_session(db, session_id)

    if not session or not user:
        raise HTTPException(status_code=403, detail="No session found")
    
    return user
