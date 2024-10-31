from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from fastapi import HTTPException

from news_service.models import News
from news_service.schemas import NewsCreate, NewsOut


class NewsServcice:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def create(self, news: NewsCreate):
        try:
            new_news = News(**news.model_dump())
            self._db.add(new_news)

            await self._db.commit()
            await self._db.refresh(new_news)

            return NewsOut.from_orm(news)
        except SQLAlchemyError as e:
            await self._db.rollback()
            raise HTTPException(status_code=500, detail=f'Error while creating new news - {e}')
