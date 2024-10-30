import datetime

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from news_service.db import Base


class News(Base):
    __tablename__ = 'news'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str]
    published_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    is_published: Mapped[bool] = mapped_column(default=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self) -> str:
        return f"News(id={self.id}, title={self.title}, published_at={self.published_at})"
