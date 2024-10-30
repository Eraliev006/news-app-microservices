from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    DB_USERNAME: str
    DB_PORT: int
    DB_HOST: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self) -> str:
        return ''
