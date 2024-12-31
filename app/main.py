from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import urlmodel,clicks
from .models.database import engine
from .routers import shorten

urlmodel.Base.metadata.create_all(bind=engine)
clicks.Base.metadata.create_all(bind=engine)
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


@app.get("/")
def root():
    return {"message": "hello, World!"}
