import datetime

from pydantic import BaseModel

class NewsCreate(BaseModel):
    title: str
    content: str
    is_published: bool =False
    author_id: int

    class Config:
        from_attributes = True

class NewsOut(NewsCreate):
    id: int
    published_at: datetime.datetime

    class Config:
        from_attributes = True