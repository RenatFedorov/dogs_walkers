from typing import Callable, AsyncGenerator
from core.config import test_settings
from pytest_asyncio import fixture
from httpx import AsyncClient, ASGITransport
from tortoise import Tortoise
import os
from main import app


@fixture(scope="session")
async def init_db() -> AsyncGenerator:
    """Initial database connection"""
    await Tortoise.init(
        db_url=f"sqlite://{test_settings.database}",
        modules={"models": ["database.models"]},
        _create_db=True,
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()
    if os.path.exists(test_settings.database):
        os.remove(test_settings.database)


@fixture
async def client(init_db) -> AsyncGenerator:
    async with AsyncClient(
        transport=ASGITransport(app=app),  # type: ignore
        base_url="http://test",
    ) as client:
        yield client


@fixture
async def get_response(
    client: AsyncClient,
) -> Callable:
    async def inner(
        method: str,
        url: str,
        query_data: dict | None = None,
        json_data: dict | None = None,
    ) -> tuple[dict, int, dict | None]:
        without_data: dict = {
            "GET": client.get,
            "DELETE": client.delete,
        }
        with_data: dict = {
            "POST": client.post,
            "PUT": client.put,
        }

        if method.upper() not in {*with_data.keys(), *without_data.keys()}:
            raise ValueError(f"Unsupported HTTP method: {method}")

        if method.upper() == "DELETE":
            response = await without_data[method.upper()](url, params=query_data)
            return response.status_code

        if method.upper() == "PUT":
            response = await with_data[method.upper()](
                url,
                params=query_data,
                json=json_data,
            )
            return response.status_code

        if method.upper() == "POST":
            response = await with_data[method.upper()](
                url,
                params=query_data,
                json=json_data,
            )
            return (
                response.json(),
                response.status_code,
                response.headers,
            )
        response = await without_data[method.upper()](url, params=query_data)
        return (
            response.json(),
            response.status_code,
            response.headers,
        )

    return inner
