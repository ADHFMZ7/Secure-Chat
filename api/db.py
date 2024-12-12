from aiosqlite import Connection, Row, connect, IntegrityError
from typing import Iterable
from models import User
from uuid import uuid4
# from random import randint

DATABASE_URL = "main.db"

async def get_user(db: Connection, username: str) -> Row | None:

    async with db.execute("SELECT * FROM User WHERE username = ?", (username,)) as cursor:
        user = await cursor.fetchone()
        return user

async def get_user_by_session(db: Connection, session_id: str) -> Row | None:

    async with db.execute("""SELECT User.* FROM User 
                             WHERE User.user_id = (
                                    SELECT user_id FROM Session 
                                    WHERE session_id = ?)""", (session_id,)) as cursor:
        user = await cursor.fetchone()
        return user

async def create_user(db: Connection, username: str, hashed_password: str) -> Row | None:
    # TODO: 
    # - Check if username already exists
    # - Return user

    # Make sure username doesnt already exist
    if await get_user(db, username):
        return None

    try:
        await db.execute(
            "INSERT INTO User (username, hashed_password) VALUES (?, ?)", 
            (username, hashed_password)
        )
        await db.commit()
    except IntegrityError:
        return None
   
    return await get_user(db, username)
    

async def users_in(db: Connection, chat_id: int) -> Iterable[Row]:
    """
    Gets all users that are members of a chat

    Input:
    - chat_id

    Output:
    - [User]
    """
    async with db.execute("""
    SELECT username FROM User
    JOIN InChat ON User.user_id = InChat.user_id
    WHERE chat_id = ?
    """, (chat_id,)) as cursor:
        return await cursor.fetchall()


async def create_session(db:Connection, user_id: int):

    session_id = str(uuid4())

    async with db.execute("INSERT INTO Session (session_id, user_id) VALUES (?, ?)", (session_id, user_id,)) as cursor:
        
        await db.commit()
        return session_id


async def delete_session(db: Connection, session_id: int):
    async with db.execute("DELETE FROM Session WHERE session_id = ?", (session_id,)) as cursor:
        await db.commit()
        return cursor.rowcount
    
    return 0

# # Change this when sessions are figured out.
async def get_session(db: Connection, session_id: str) -> Row | None:

    async with db.execute("SELECT * FROM Session WHERE session_id = ?", (session_id,)) as cursor:
        session = await cursor.fetchone()
        # logging maybe?
        return session 

async def get_session_username(db: Connection, username: str) -> Row | None:
    query = """
        SELECT Session.*, User.username 
        FROM Session
        JOIN User ON Session.user_id = User.user_id
        WHERE User.username = ?
    """

    async with db.execute(query, (username,)) as cursor:
        session = await cursor.fetchone()
        # logging maybe?
        return session


# def session_exists(username: str):
#     for _, sesh in sessions.items():
#         if sesh == username:
#             return True
#     return False


# def user_in(chat_id: str):
#     # Get a list of all usernames that are a part of the chat
#     pass


async def init_db():
    async with connect(DATABASE_URL) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS User (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS Chat (
            chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS InChat (
            user_id INTEGER,
            chat_id INTEGER,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, chat_id),
            FOREIGN KEY (user_id) REFERENCES User(user_id),
            FOREIGN KEY (chat_id) REFERENCES Chat(chat_id)
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS Friendship (
            P1 INTEGER,
            P2 INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (P1, P2),
            FOREIGN KEY (P1) REFERENCES User(user_id),
            FOREIGN KEY (P2) REFERENCES User(user_id)
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS Message (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sent_by INTEGER,
            chat_id INTEGER,
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_read BOOLEAN DEFAULT 0,
            FOREIGN KEY (sent_by) REFERENCES User(user_id),
            FOREIGN KEY (chat_id) REFERENCES Chat(chat_id)
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS Session (
            session_id CHAR(36) PRIMARY KEY,
            user_id INTEGER,
            last_seen TIMESTAMP,
            ip_address TEXT,
            FOREIGN KEY (user_id) REFERENCES User(user_id)
        )
        """)

        await db.commit()
        print("Database initialized successfully!")
