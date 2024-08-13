from fastapi import FastAPI, status
from contextlib import asynccontextmanager

from tortoise import Tortoise

from core.logger import LOGGING
from core.config import settings
from logging import config as logging_config
from api.v1.order.order import order_router
from api.v1.dog.dog_router import dogs_router
from api.v1.walker.walker import walker_router


@asynccontextmanager
async def lifespan(_):
    logging_config.dictConfig(LOGGING)
    await Tortoise.init(
        db_url=settings.db.postgres_dsn,
        modules={"models": ["database.models"]},
    )
    yield

    await Tortoise.close_connections()


app = FastAPI(
    title=settings.fast_api.project_name,
    summary=settings.fast_api.project_summary,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    version="0.1",
    lifespan=lifespan,
)


app.include_router(order_router)
app.include_router(dogs_router)
app.include_router(walker_router)


@app.get("/healthcheck", status_code=status.HTTP_200_OK, include_in_schema=False)
async def health():
    return status.HTTP_200_OK
