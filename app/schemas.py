from pydantic import BaseModel, HttpUrl


class LinkCreate(BaseModel):
    url: HttpUrl


class LinkOut(BaseModel):
    code: str
    url: str
    clicks: int
