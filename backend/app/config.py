from typing import Optional
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    AnyUrl,
    BeforeValidator,
    Field,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./app/)
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    DB_DRIVER: str
    DB_HOST: str
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_PORT: str | None = None
    DB_PATH: str | None = None

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        host = f"/{self.DB_HOST}" if self.DB_DRIVER == "sqlite" else self.DB_HOST

        return str(
            MultiHostUrl.build(
                scheme=self.DB_DRIVER,
                username=self.DB_USER,
                password=self.DB_PASSWORD,
                host=host,
                port=self.DB_PORT,
                path=self.DB_PATH,
            )
        )


settings = Settings()
