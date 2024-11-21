from fastapi import APIRouter, Form, HTTPException
from typing import Annotated
from db import get_user, get_session, create_user

router = APIRouter()
