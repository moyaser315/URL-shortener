from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from models import urlmodel
from models.database import engine, get_db
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
    return {"message": "hello, World!"}


@app.post("/", status_code=status.HTTP_201_CREATED)
def create_url(url: scheme.Url, db: Session = Depends(get_db)):
    n_u = url.original_url

    exist = db.query(urlmodel.Urls).filter(urlmodel.Urls.original_url == n_u).first()
    if exist:
        print("url already exist")
        return {"new_url": f"localhost:8000/{exist.new_url}"}
    new_url = utils.create_new_url(n_u)
    shortened = urlmodel.Urls(original_url=n_u, new_url=new_url)
    db.add(shortened)
    db.commit()
    db.refresh(shortened)
    return {"new_url": f"localhost:8000/{shortened.new_url}"}


@app.get(
    "/{new_url}",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    response_class=RedirectResponse,
)
async def get_orig_url(new_url: str, db: Session = Depends(get_db)):
    orig_url_q = db.query(urlmodel.Urls).filter(urlmodel.Urls.new_url == new_url)
    orig_url = orig_url_q.first()
    if not orig_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There is no such url"
        )
    orig_url.clicks += 1

    orig_url_q.update({"clicks": f"{orig_url.clicks}"})
    orig_url = orig_url.original_url
    db.commit()
    return orig_url


@app.post("/stats", response_model=scheme.UrlStats)
async def get_url_stats(orig_url: scheme.Url, db: Session = Depends(get_db)):

    url = (
        db.query(urlmodel.Urls)
        .filter(urlmodel.Urls.original_url == orig_url.original_url)
        .first()
    )

    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This URL is not registered Yet",
        )
    return url
