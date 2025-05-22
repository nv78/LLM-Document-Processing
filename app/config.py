import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_API_KEY: str
    LLM_MODEL: str = Field("gpt-3.5-turbo", env="LLM_MODEL")
    EMBED_MODEL: str = Field("text-embedding-3-small", env="EMBED_MODEL")

    class Config:
        env_file = ".env"

settings = Settings()