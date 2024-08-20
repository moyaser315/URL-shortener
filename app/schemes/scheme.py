from pydantic import BaseModel, ConfigDict
import datetime


class Url(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    original_url: str


class NewUrl(Url):
    new_url: str
    craeted_at: datetime.datetime


class UrlStats(NewUrl):
    clicks: int
