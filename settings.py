from pydantic.v1 import BaseSettings
from dotenv import load_dotenv
import os


load_dotenv()

class Settings(BaseSettings):

    TG_BOT_KEY = os.getenv('TG_BOT_KEY')
    AI_API_KEY = os.getenv('AI_API_KEY')

    class Config:
        env_file = '.env'


settings = Settings()
