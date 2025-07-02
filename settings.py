from pydantic.v1 import BaseSettings
from dotenv import load_dotenv
import os


load_dotenv()

class Settings(BaseSettings):

    TG_BOT_KEY: str = os.getenv('TG_BOT_KEY')
    AI_API_KEY: str = os.getenv('AI_API_KEY')
    IS_TEST: bool = os.getenv('IS_TEST')
    AI_MISTRAL_API_KEY: str = os.getenv('AI_MISTRAL_API_KEY')

    class Config:
        env_file = '.env'


settings = Settings()
