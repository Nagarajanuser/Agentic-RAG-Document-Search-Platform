from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "HR Policy RAG API - CrewAI"
    app_version: str = "2.0"
    debug: bool = False

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
