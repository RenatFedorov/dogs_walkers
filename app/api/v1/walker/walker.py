import uuid

from fastapi import APIRouter, status, Depends
from api.v1.walker.models import (
    DogWalkerReturnModel,
    DogWalkerModel,
    IDModel,
)
from models.paginated_params import (
    PaginatedParams,
    PaginationResponse,
)
from service.service import get_dog_walker_service


walker_router = APIRouter(
    prefix="/api/v1/dogs-walkers",
    tags=["dogs_walkers"],
)


@walker_router.get(
    "/",
    response_model=PaginationResponse,
    status_code=status.HTTP_200_OK,
    description="List of all dogs walkers",
)
async def get_dog_walkers(
    service=Depends(get_dog_walker_service),
    query_params: PaginatedParams = Depends(),
):
    return await service.get_all(query_params)


@walker_router.get(
    "/{dog_walker_id}/",
    response_model=DogWalkerReturnModel,
    status_code=status.HTTP_200_OK,
    description="Read a single dog walker",
)
async def get_dog_walker(
    dog_walker_id: uuid.UUID,
    service=Depends(get_dog_walker_service),
):
    return await service.get_single(dog_walker_id)


@walker_router.post(
    "/",
    response_model=IDModel,
    status_code=status.HTTP_201_CREATED,
    description="Create new dog walker",
)
async def create_dog_walker(
    dog_walker: DogWalkerModel,
    service=Depends(get_dog_walker_service),
) -> dict:
    return await service.create(dog_walker)


@walker_router.put(
    "/{dog_walker_id}/",
    status_code=status.HTTP_200_OK,
    description="Update dog walker",
)
async def update_dog_walker(
    dog_walker_id: uuid.UUID,
    dog_walker: DogWalkerModel,
    service=Depends(get_dog_walker_service),
):
    print(dog_walker)
    return await service.update(
        row_id=dog_walker_id,
        new_instance=dog_walker,
    )


@walker_router.delete(
    "/{dog_walker_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete dog walker",
)
async def delete_dog_walker(
    dog_walker_id: uuid.UUID,
    service=Depends(get_dog_walker_service),
):
    return await service.delete(row_id=dog_walker_id)
