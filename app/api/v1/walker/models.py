from uuid import UUID
from pydantic import BaseModel


class IDModel(BaseModel):
    id: UUID


class DogWalkerModel(BaseModel):
    name: str
    surname: str
    active: bool = True


class DogWalkerReturnModel(IDModel, DogWalkerModel):
    pass
