from dataclasses import dataclass
from datetime import datetime
from typing import List, Self
from pydantic import BaseModel

class User(BaseModel):
    # id: str
    username: str
    password: str


class Chat(BaseModel):
    id: str

class Message(BaseModel):
    sender_id: int #Foreign Key
    chat_id: int #Foreign Key
    content: str

class ChatCreation(BaseModel):
    user_ids: List[int]

