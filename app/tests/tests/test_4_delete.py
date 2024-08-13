from fastapi import status
import pytest

from core.config import test_settings
from tests.test_data.test_data_dog import (
    fake_dog_data,
)
from tests.test_data.test_data_order import (
    fake_order_data,
)
from tests.test_data.test_data_walker import (
    fake_walker_data,
)


@pytest.mark.parametrize(
    "dog",
    [
        (fake_dog_data[0]),
        (fake_dog_data[1]),
        (fake_dog_data[2]),
    ],
)
@pytest.mark.asyncio
async def test_delete_dog_success(get_response, dog):
    dog_id = dog.get("id")
    status_code = await get_response(
        "DELETE",
        f"{test_settings.dogs_url}{dog_id}/",
    )
    assert status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.parametrize(
    "walker",
    [
        (fake_walker_data[0]),
        (fake_walker_data[1]),
        (fake_walker_data[2]),
    ],
)
@pytest.mark.asyncio
async def test_delete_walker_success(get_response, walker):
    walker_id = walker.get("id")
    status_code = await get_response(
        "DELETE",
        f"{test_settings.walkers_url}{walker_id}/",
    )
    assert status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.parametrize(
    "order",
    [
        (fake_order_data[0]),
        (fake_order_data[1]),
        (fake_order_data[2]),
    ],
)
@pytest.mark.asyncio
async def test_delete_order_success(get_response, order):
    order_id = order.get("id")
    status_code = await get_response(
        "DELETE",
        f"{test_settings.orders_url}{order_id}/",
    )
    assert status_code == status.HTTP_204_NO_CONTENT
