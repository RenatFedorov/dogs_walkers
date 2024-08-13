from uuid import UUID
from pydantic import BaseModel


class IDModel(BaseModel):
    id: UUID


class DogModel(BaseModel):
    apartment: int
    name: str
    breed: str


class DogReturnModel(IDModel, DogModel):
    pass
