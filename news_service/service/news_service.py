
from sqlalchemy.orm import Session

from fastapi import HTTPException

from news_service.models import News
from news_service.schemas import NewsCreate, NewsOut


class NewsServcice:
    def __init__(self, db:Session):
        self._db = db

    def create(self, news: NewsCreate):
        try:
            news = News(**news.model_dump())
            self._db.add(news)
            self._db.commit()

            return NewsOut.from_orm(news)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Error while creating new news - {e}')
