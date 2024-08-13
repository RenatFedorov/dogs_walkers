from typing import Union

from fastapi import Query
from pydantic import BaseModel
from api.v1.walker.models import (
    DogWalkerReturnModel,
)
from api.v1.dog.models import DogReturnModel
from api.v1.order.order import OrderReturnModel


class PaginatedParams:
    def __init__(
        self,
        page: int = Query(1, description="Page number"),
        size: int = Query(
            10,
            description="Number of records per page",
        ),
    ):
        self.page = page
        self.size = size


RESULT_TYPE = list[
    Union[
        DogReturnModel,
        OrderReturnModel,
        DogWalkerReturnModel,
    ]
]


class PaginationResponse(BaseModel):
    page_number: int
    size: int
    total_pages: int
    total_result: int
    result: RESULT_TYPE
