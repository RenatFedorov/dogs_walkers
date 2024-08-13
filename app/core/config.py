from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from dotenv import load_dotenv

load_dotenv(".env.example")


class FastApiSettings(BaseSettings):
    project_name: str
    project_summary: str
    root_path: str

    model_config = SettingsConfigDict(env_prefix="fastapi_")


class DBSettings(BaseSettings):
    postgres_dsn: str


class TestSettings(BaseSettings):
    dogs_url: str
    walkers_url: str
    orders_url: str
    database: str

    model_config = SettingsConfigDict(env_prefix="test_")


class AppSettings(BaseSettings):
    fast_api: FastApiSettings = FastApiSettings()
    db: DBSettings = DBSettings()


settings = AppSettings()
test_settings = TestSettings()

TORTOISE_ORM = {
    "connections": {"default": settings.db.postgres_dsn},
    "apps": {
        "models": {
            "models": ["database.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
