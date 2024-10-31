from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class DBSettings(BaseSettings):
    DB_USERNAME: str
    DB_PORT: int
    DB_HOST: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self) -> str:
        # "postgresql://<username>:<password>@<host>:<port>/<database_name>"
        return f'postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    class Config:
        env_file = '.env'



settings = DBSettings()

if __name__ == '__main__':
    print(settings.DATABASE_URL_asyncpg)
