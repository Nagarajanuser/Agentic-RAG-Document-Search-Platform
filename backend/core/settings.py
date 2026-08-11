from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = " Agentic RAG Document Search Platform - CrewAI"
    app_version: str = "2.0"
    debug: bool = False

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
