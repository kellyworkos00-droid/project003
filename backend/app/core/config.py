from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = Field(default="OpenERP-MVP")
    debug: bool = Field(default=True)
    secret_key: str = Field(default="dev-secret-key-change-me")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=60 * 24)

    # SQLite for local dev; switch to Postgres in production
    sqlalchemy_database_uri: str = Field(default="sqlite:///./data/app.db")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()