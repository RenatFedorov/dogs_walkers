import pytest
from fastapi import status
from core.config import test_settings
from tests.test_data.test_data_dog import (
    fake_dog_data,
    fake_incorrect_dog_data,
    basic_response,
)


@pytest.mark.asyncio
async def test_get_dogs_without_result(
    get_response,
):
    body, status_code, _ = await get_response("GET", test_settings.dogs_url)
    assert status_code == status.HTTP_200_OK
    assert basic_response == body


@pytest.mark.parametrize(
    "json_data, index",
    [
        (fake_dog_data[0], 0),
        (fake_dog_data[1], 1),
        (fake_dog_data[2], 2),
    ],
)
@pytest.mark.asyncio
async def test_create_dog_success(
    get_response,
    json_data: dict,
    index,
):
    body, status_code, _ = await get_response(
        "POST",
        f"{test_settings.dogs_url}",
        json_data=json_data,
    )
    fake_dog_data[index]["id"] = body.get("id")
    assert status_code == status.HTTP_201_CREATED
    assert "id" in body
    assert fake_dog_data[index].get("id") == body.get("id")


@pytest.mark.asyncio
async def test_get_dogs_with_result(get_response):
    body, status_code, _ = await get_response("GET", test_settings.dogs_url)
    assert status_code == status.HTTP_200_OK
    awaiting_resp = basic_response
    awaiting_resp["total_pages"] = 1
    awaiting_resp["total_result"] = 3
    assert body["total_pages"] == awaiting_resp["total_pages"]
    assert body["total_result"] == awaiting_resp["total_result"]
    for row in fake_dog_data:
        assert row in body["result"]


@pytest.mark.parametrize(
    "json_data, expected_message",
    [
        (
            fake_incorrect_dog_data["1"],
            "Input should be a valid integer, unable to parse string as an integer",
        ),
        (
            fake_incorrect_dog_data["2"],
            "Input should be a valid string",
        ),
        (
            fake_incorrect_dog_data["3"],
            "Input should be a valid string",
        ),
        (
            fake_incorrect_dog_data["4"],
            "Field required",
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_dog_error(
    get_response,
    json_data: dict,
    expected_message: dict,
):
    body, status_code, _ = await get_response(
        "POST",
        f"{test_settings.dogs_url}",
        json_data=json_data,
    )
    assert status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_json: dict = body.get("detail")[0]
    assert response_json.get("msg") == expected_message


@pytest.mark.parametrize(
    "json_data, field, new_data",
    [
        (fake_dog_data[0], "apartment", 15),
        (fake_dog_data[1], "name", "Rex"),
        (fake_dog_data[2], "breed", "Dalmatian"),
    ],
)
@pytest.mark.asyncio
async def test_update_dog_success(
    get_response,
    json_data: dict,
    field: str,
    new_data: str | int,
):
    body, status_code, _ = await get_response(
        "POST",
        f"{test_settings.dogs_url}",
        json_data=json_data,
    )
    dog_id: str = body.get("id")
    new_insert_data: dict = json_data
    new_insert_data[field] = new_data
    status_code = await get_response(
        "PUT",
        f"{test_settings.dogs_url}{dog_id}/",
        json_data=new_insert_data,
    )
    assert status_code == status.HTTP_200_OK
    body, status_code, _ = await get_response(
        "GET",
        f"{test_settings.dogs_url}{dog_id}/",
    )
    assert status_code == status.HTTP_200_OK
    assert body.get(field) == new_data
