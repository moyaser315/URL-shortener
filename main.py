from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from models import urlmodel
from models.database import engine,get_db
from schemes import scheme
import utils

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

urlmodel.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message":"hello, World!"}


@app.post("/", status_code=status.HTTP_201_CREATED,response_model=scheme.NewUrl)
def get_url(url: scheme.Url, db:Session = Depends(get_db)):
    n_u = url.original_url
    print(type(n_u))
    exist = db.query(urlmodel.Urls).filter(urlmodel.Urls.original_url==n_u).first()
    if exist : 
       print('url already exist')
       return exist
    new_url = utils.create_new_url(n_u)
    shortened = urlmodel.Urls(original_url=n_u,new_url=new_url)
    db.add(shortened)
    db.commit()
    db.refresh(shortened)
    return shortened
