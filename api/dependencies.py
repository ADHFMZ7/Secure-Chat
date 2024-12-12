from fastapi import Security, HTTPException
from fastapi.param_functions import Depends
from fastapi.security import APIKeyCookie
from aiosqlite import connect, Row, Connection
from db import DATABASE_URL, get_session, get_user

cookie = APIKeyCookie(name="session_id", auto_error=False)

async def get_db():
    """
    Fetches database session     
    """
    
    async with connect(DATABASE_URL) as db:
        db.row_factory = Row 
        yield db

async def get_current_user(session_id: str = Security(cookie),
                           db: Connection = Depends(get_db)):

    print("received session id:", session_id)

    session = await get_session(db, session_id)

    print("Session received:", session)

    if not session:
        raise HTTPException(status_code=403, detail="Invalid or missing session cookie")

    username = session[1] # Whatever field username is
    print("Username:", username)

    return get_user(db, username)
