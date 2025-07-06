from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import urlmodel, clicks
from .models.database import engine
from .routers import shorten
import asyncio

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(shorten.router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(urlmodel.Base.metadata.create_all)
        await conn.run_sync(clicks.Base.metadata.create_all)

@app.get("/")
def root():
    return {"message": "hello, World!"}
