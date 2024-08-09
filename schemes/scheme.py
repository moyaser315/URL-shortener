from pydantic import BaseModel, ConfigDict


class Url(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    original_url = True
    new_url = True
