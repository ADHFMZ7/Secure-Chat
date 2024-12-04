from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, user, chat
from db import init_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_origins=["http://localhost:8000", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(chat.router)
