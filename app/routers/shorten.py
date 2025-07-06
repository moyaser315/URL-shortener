from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..schemes import scheme
from .. import utils,stats
from ..models import urlmodel,clicks
from ..models.database import get_db

router = APIRouter(tags=["Shorten Url"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_url(url: scheme.Url, db: AsyncSession = Depends(get_db)):
    orig_url = url.original_url
    check_url_scheme = utils.valid_url(orig_url)
    if not check_url_scheme:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Please enter valid URL!",
        )
    result = await db.execute(select(urlmodel.Urls).where(urlmodel.Urls.original_url == orig_url))
    exist = result.scalars().first()
    if exist:
        print("url already exist")
        return {"new_url": f"localhost:8000/{exist.new_url}"}
    new_url = utils.create_new_url(orig_url)
    shortened = urlmodel.Urls(original_url=orig_url, new_url=new_url)
    db.add(shortened)
    await db.commit()
    await db.refresh(shortened)
    return {"new_url": f"localhost:8000/{shortened.new_url}"}


@router.get(
    "/{new_url}",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    response_class=RedirectResponse,
)
async def get_orig_url(new_url: str, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(urlmodel.Urls).where(urlmodel.Urls.new_url == new_url))
    orig_url = result.scalars().first()
    if not orig_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There is no such url"
        )
    orig_url.clicks_count += 1
    # Update clicks_count
    await db.commit()
    info = utils.parse_user_agent(request.headers['user-agent'])
    print(info)
    stats_obj = clicks.Clicks(
        url_id=orig_url.id,
        os=info['os'],
        device=info['device'],
        browser=info['browser'],
        client_ip=f"{request.client.host}"
    )
    db.add(stats_obj)
    await db.commit()
    await db.refresh(stats_obj)
    return orig_url.original_url


@router.post("/stats")
async def get_url_stats(orig_url: scheme.Url, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(urlmodel.Urls).where(urlmodel.Urls.original_url == orig_url.original_url))
    url = result.scalars().first()
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This URL is not registered Yet",
        )
    result_clicks = await db.execute(select(clicks.Clicks).where(clicks.Clicks.url_id == url.id))
    stat = result_clicks.scalars().all()
    s = [i.__dict__ for i in stat]
    res = stats.analyze(s, url.id)

    response = dict(res)
    response["original_url"] = url.original_url
    response["new_url"] = url.new_url
    response["craeted_at"] = str(url.craeted_at) if hasattr(url, 'craeted_at') else (str(url.created_at) if hasattr(url, 'created_at') else None)
    response["clicks"] = url.clicks_count if hasattr(url, 'clicks_count') else len(s)
    return response
