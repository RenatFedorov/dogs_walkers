import pytest
from fastapi import status

from core.config import test_settings
from tests.test_data.test_data_walker import (
    basic_response,
    fake_walker_data,
    fake_incorrect_walker_data,
)


@pytest.mark.asyncio
async def test_get_walkers_without_result(
    get_response,
):
    body, status_code, _ = await get_response("GET", test_settings.walkers_url)
    assert status_code == status.HTTP_200_OK
    assert basic_response == body


@pytest.mark.parametrize(
    "json_data, index",
    [
        (fake_walker_data[0], 0),
        (fake_walker_data[1], 1),
        (fake_walker_data[2], 2),
    ],
)
@pytest.mark.asyncio
async def test_create_walker_success(
    get_response,
    json_data: dict,
    index: int,
):
    body, status_code, _ = await get_response(
        "POST",
        f"{test_settings.walkers_url}",
        json_data=json_data,
    )
    fake_walker_data[index]["id"] = body.get("id")
    assert status_code == status.HTTP_201_CREATED
    assert "id" in body


@pytest.mark.asyncio
async def test_get_walkers_with_result(
    get_response,
):
    body, status_code, _ = await get_response("GET", test_settings.walkers_url)
    assert status_code == status.HTTP_200_OK
    awaiting_resp = basic_response
    awaiting_resp["total_pages"] = 1
    awaiting_resp["total_result"] = 3
    assert body["total_pages"] == awaiting_resp["total_pages"]
    assert body["total_result"] == awaiting_resp["total_result"]
    for row in fake_walker_data:
        assert row in body["result"]


@pytest.mark.parametrize(
    "json_data, expected_message",
    [
        (
            fake_incorrect_walker_data["1"],
            "Input should be a valid string",
        ),
        (
            fake_incorrect_walker_data["2"],
            "Input should be a valid string",
        ),
        (
            fake_incorrect_walker_data["3"],
            "Field required",
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_walker_error(
    get_response,
    json_data: dict,
    expected_message: dict,
):
    body, status_code, _ = await get_response(
        "POST",
        f"{test_settings.walkers_url}",
        json_data=json_data,
    )
    assert status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response_json: dict = body.get("detail")[0]
    assert response_json.get("msg") == expected_message


@pytest.mark.parametrize(
    "json_data, field, new_data",
    [
        (fake_walker_data[0], "name", "Supermen"),
        (
            fake_walker_data[1],
            "surname",
            "IronMan",
        ),
        (fake_walker_data[2], "active", False),
    ],
)
@pytest.mark.asyncio
async def test_update_walker_success(
    get_response,
    json_data: dict,
    field: str,
    new_data: str | int,
):
    body, status_code, _ = await get_response(
        "POST",
        f"{test_settings.walkers_url}",
        json_data=json_data,
    )
    dog_walkers_id: str = body.get("id")
    new_insert_data: dict = json_data
    new_insert_data[field] = new_data
    status_code = await get_response(
        "PUT",
        f"{test_settings.walkers_url}{dog_walkers_id}/",
        json_data=new_insert_data,
    )
    assert status_code == status.HTTP_200_OK
    body, status_code, _ = await get_response(
        "GET",
        f"{test_settings.walkers_url}{dog_walkers_id}/",
    )
    assert status_code == status.HTTP_200_OK
    assert "id" in body
    assert body.get(field) == new_data
