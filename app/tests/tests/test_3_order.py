from fastapi import status
import pytest
from core.config import test_settings
from tests.test_data.test_data_dog import (
    fake_dog_data,
)
from tests.test_data.test_data_order import (
    basic_response,
    fake_order_data,
    fake_incorrect_order_data,
)
from tests.test_data.test_data_walker import (
    fake_walker_data,
)


@pytest.mark.asyncio
async def test_get_dogs_without_result(
    get_response,
):
    body, status_code, _ = await get_response("GET", test_settings.orders_url)
    assert status_code == status.HTTP_200_OK
    assert basic_response == body


@pytest.mark.parametrize(
    "json_order_data, json_dog_data, json_walker_data, index",
    [
        (
            fake_order_data[0],
            fake_dog_data[0],
            fake_walker_data[0],
            0,
        ),
        (
            fake_order_data[1],
            fake_dog_data[1],
            fake_walker_data[0],
            1,
        ),
        (
            fake_order_data[2],
            fake_dog_data[2],
            fake_walker_data[0],
            2,
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_order_success(
    get_response,
    json_order_data: dict,
    json_dog_data: dict,
    json_walker_data: dict,
    index: int,
):
    fake_order_data[index]["dog"] = json_dog_data.get("id")
    fake_order_data[index]["walker"] = json_walker_data.get("id")
    body, status_code, _ = await get_response(
        "POST",
        f"{test_settings.orders_url}",
        json_data=json_order_data,
    )
    fake_order_data[index]["id"] = body.get("id")
    assert body.get("id") == fake_order_data[index]["id"]
    assert status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_get_orders_with_result(
    get_response,
):
    body, status_code, _ = await get_response("GET", test_settings.orders_url)
    assert status_code == status.HTTP_200_OK
    awaiting_resp = basic_response
    awaiting_resp["total_pages"] = 1
    awaiting_resp["total_result"] = 3
    assert body["total_pages"] == awaiting_resp["total_pages"]
    assert body["total_result"] == awaiting_resp["total_result"]
    for row, row_data in enumerate(fake_order_data):
        assert row_data.get("id") in body["result"][row].get("id")


@pytest.mark.parametrize(
    "json_data, expected_message",
    [
        (
            fake_incorrect_order_data["1"],
            "Value error, Date should be valid value starting from today",
        ),
        (
            fake_incorrect_order_data["2"],
            "Value error, Hour should be positive integer from 7 to 22",
        ),
        (
            fake_incorrect_order_data["3"],
            "Value error, Hour should be positive integer from 7 to 22",
        ),
        (
            fake_incorrect_order_data["4"],
            "Input should be 'Запланирована', 'В процессе', 'Завершена' or 'Отменена'",
        ),
        (
            fake_incorrect_order_data["5"],
            "Value error, Minutes should be 30 or 00",
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_order_error(
    get_response,
    json_data: dict,
    expected_message: dict,
):
    body, status_code, _ = await get_response(
        "POST",
        f"{test_settings.orders_url}",
        json_data=json_data,
    )
    assert status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_json: dict = body.get("detail")[0]
    assert response_json.get("msg") == expected_message


@pytest.mark.parametrize(
    "json_data, dog, walker, walk_time, message",
    [
        (
            fake_order_data[0],
            fake_dog_data[0],
            fake_walker_data[0],
            "2030-01-12 21:30:10",
            "IntegrityError: UNIQUE constraint failed: orders.walk_at, orders.dog_id",
        ),
        (
            fake_order_data[0],
            fake_dog_data[1],
            fake_walker_data[0],
            "2030-01-12 21:30:10",
            "IntegrityError: UNIQUE constraint failed: orders.walk_at, orders.walker_id",
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_order_conflict(
    get_response,
    json_data: dict,
    dog: dict,
    walker: dict,
    walk_time: str,
    message: str,
):
    json_data["dog"] = dog.get("id")
    json_data["walker"] = walker.get("id")
    json_data["walk_at"] = walk_time
    body, status_code, _ = await get_response(
        "POST",
        f"{test_settings.orders_url}",
        json_data=json_data,
    )
    assert status_code == status.HTTP_409_CONFLICT
    assert body.get("detail") == message


@pytest.mark.parametrize(
    "json_data, dog, walker, walk_time",
    [
        (
            fake_order_data[0],
            fake_dog_data[1],
            fake_walker_data[2],
            "2030-01-12 11:30:10",
        ),
        (
            fake_order_data[1],
            fake_dog_data[2],
            fake_walker_data[1],
            "3030-01-12 21:30:10",
        ),
        (
            fake_order_data[2],
            fake_dog_data[2],
            fake_walker_data[1],
            "2030-01-12 17:30:10",
        ),
    ],
)
@pytest.mark.asyncio
async def test_update_order(
    get_response,
    json_data: dict,
    dog: dict,
    walker: dict,
    walk_time: str,
):
    json_data["dog"] = dog.get("id")
    json_data["walker"] = walker.get("id")
    json_data["walk_at"] = walk_time
    order_id = json_data.get("id")
    status_code = await get_response(
        "PUT",
        f"{test_settings.orders_url}{order_id}/",
        json_data=json_data,
    )
    assert status_code == status.HTTP_200_OK
