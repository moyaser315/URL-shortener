from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ..schemes import scheme
from .. import utils,stats
from ..models import urlmodel,clicks
from ..models.database import get_db

router = APIRouter(tags=["Shorten Url"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_url(url: scheme.Url, db: Session = Depends(get_db)):
    orig_url = url.original_url
    check_url_scheme = utils.valid_url(orig_url)
    if not check_url_scheme:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Please enter valid URL!",
        )
    exist = (
        db.query(urlmodel.Urls).filter(urlmodel.Urls.original_url == orig_url).first()
    )
    if exist:
        print("url already exist")
        return {"new_url": f"localhost:8000/{exist.new_url}"}
    new_url = utils.create_new_url(orig_url)
    shortened = urlmodel.Urls(original_url=orig_url, new_url=new_url)
    db.add(shortened)
    db.commit()
    db.refresh(shortened)
    return {"new_url": f"localhost:8000/{shortened.new_url}"}


@router.get(
    "/{new_url}",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    response_class=RedirectResponse,
)
async def get_orig_url(new_url: str,request:Request, db: Session = Depends(get_db)):
    orig_url_q = db.query(urlmodel.Urls).filter(urlmodel.Urls.new_url == new_url)
    orig_url = orig_url_q.first()
    if not orig_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There is no such url"
        )
    orig_url.clicks_count += 1
    orig_url_q.update({"clicks_count": f"{orig_url.clicks_count}"})
    info = utils.parse_user_agent(request.headers['user-agent'])
    print(info)
    stats = clicks.Clicks(url_id = orig_url.id,
    os = info['os'],
    device = info['device'],
    browser = info['browser'],
    client_ip= f"{request.client.host}")
    orig_url = orig_url.original_url
    db.add(stats)
    db.commit()
    db.refresh(stats)
    return orig_url


@router.post("/stats")
async def get_url_stats(orig_url: scheme.Url, db: Session = Depends(get_db)):

    url = (
        db.query(urlmodel.Urls)
        .filter(urlmodel.Urls.original_url == orig_url.original_url)
        .first()
    )
    stats = db.query(clicks.Clicks).filter(url.id==clicks.Clicks.url_id).all()


    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This URL is not registered Yet",
        )

    return {'url':url, 'stats':stats}
