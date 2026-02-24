# env.py
import typing

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(".env.bak")
load_dotenv(".env.local", override=True)


class Env(BaseSettings):
    APP_NAME: str = "FastApi-Thynne"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DATABASE_URL: str = Field(default="")
    GRAPHQL_ACCESS_TOKEN: str | None = Field(default=None)
    APP_ENV: str = Field(default="development")
    RUNNING_FROM_BAT: bool = Field(default=False)
    model_config = SettingsConfigDict(extra="ignore")


_env = Env()


def __getattr__(name: str) -> typing.Any:  # noqa: ANN401
    return getattr(_env, name)
