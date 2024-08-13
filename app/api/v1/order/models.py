from datetime import datetime
from typing import Annotated
from uuid import UUID
from pydantic import (
    BaseModel,
    field_validator,
    Field,
)
from api.v1.walker.models import (
    DogWalkerReturnModel,
)
from api.v1.dog.models import DogReturnModel
from database.models import OrderStatus

MIN_HOUR = 7
MAX_HOUR = 22
VALID_MINUTES = {0, 30}


class IDModel(BaseModel):
    id: UUID


class WalkTime(BaseModel):
    walk_at: Annotated[datetime, Field(validate_default=True)]

    @field_validator("walk_at")
    @classmethod
    def validate_date(cls, walk_at: datetime) -> datetime:
        walk_at = walk_at.replace(tzinfo=None, second=0, microsecond=0)
        if walk_at < datetime.now():
            raise ValueError("Date should be valid value starting from today")
        if walk_at.hour not in range(MIN_HOUR, MAX_HOUR + 1):
            raise ValueError("Hour should be positive integer from 7 to 22")
        if walk_at.minute not in VALID_MINUTES:
            raise ValueError("Minutes should be 30 or 00")
        return walk_at


class OrderUpdateModel(BaseModel):
    dog: UUID
    walker: UUID
    status: OrderStatus


class NewOrder(WalkTime, OrderUpdateModel):
    pass


class OrderReturnModel(IDModel):
    walk_at: datetime
    dog: DogReturnModel
    walker: DogWalkerReturnModel
    status: OrderStatus
