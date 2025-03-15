from pydantic_settings import BaseSettings
import logging
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    def get_db_url(self):
        try:
            return f"sqlite+aiosqlite:///db.sqlite3"
        except Exception as e:
            logging.error(e)
            raise


settings = Settings()
