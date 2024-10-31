
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update

from fastapi import HTTPException

from news_service.db import settings
from news_service.models import News
from news_service.schemas import NewsCreate, NewsOut


class NewsService:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def create(self, news: NewsCreate) -> NewsOut:
        try:
            new_news = News(**news.model_dump())
            self._db.add(new_news)

            await self._db.commit()
            await self._db.refresh(new_news)

            return NewsOut.from_attributes(new_news)
        except SQLAlchemyError as e:
            await self._db.rollback()
            raise HTTPException(status_code=500, detail=f'Error while creating new news - {e}')

    async def get_all_news(self) -> list[NewsOut]:
        try:
            result = await self._db.execute(select(News))
            news_list = result.scalars().all()

            return [NewsOut.from_attributes(x) for x in news_list]
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f'Error while getting news - {e}')


    async def __get_news(self, news_id: int):
        try:
            news = await self._db.get(News, news_id)
            return news
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f'Error while getting news with id - {news_id}')

    async def get_news_by_id(self, news_id:int) -> NewsOut:
            news = await self.__get_news(news_id)
            return NewsOut.from_attributes(news)

    async def delete_news_by_id(self, news_id: int) -> None:
        try:
            news = await self.__get_news(news_id)

            if news is None:
                raise HTTPException(status_code=404, detail="News not found")

            await self._db.delete(news)

            await self._db.commit()

        except SQLAlchemyError as e:
            await self._db.rollback()
            raise HTTPException(status_code=500, detail=f'Error while deleting news - {e}')


    async def update_news(self, news: NewsCreate,news_id: int) -> NewsOut:
        existing_news = await self.__get_news(news_id)
        if existing_news is None:
            raise HTTPException(status_code=404, detail=f'News with id {news_id} not existing')

        stmt = update(News).where(News.id == news_id).values(news.model_dump(exclude_unset=True))

        try:
            await self._db.execute(stmt)
            await self._db.commit()

            updated_news = await self.__get_news(news_id)
            return NewsOut.from_attributes(updated_news)
        except SQLAlchemyError as e:
            await self._db.rollback()
            raise HTTPException(status_code=500, detail=f'Error while updating news - {e}')

